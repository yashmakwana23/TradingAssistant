import pandas_ta as ta
from NorenRestApiPy.NorenApi import  NorenApi
import pandas as pd
import pyotp
import math
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import json

class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
        global api
        api = self

api = ShoonyaApiPy()

with open('E_tokens\shoonya.json', 'r') as file:
    token_data = json.load(file)

Shoonyatoken = token_data.get("token")
shoontauser=token_data.get("user")
email=token_data.get("app_key")
paswd=token_data.get("pwd")
opvc=token_data.get("vc")
shoonta=token_data.get("imei")

token = Shoonyatoken
otp = pyotp.TOTP(token).now()
user        = shoontauser
pwd       = paswd
factor2     = otp
vc          = opvc
app_key     = email
imei        = shoonta

ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)

info=api.get_limits()
print(info)
i=2


#converter from numpy to float

def float64 (a):
    val = np.float64(a)
    pyval = val.item()
    return pyval 

def float32 (a):
    val = np.float32(a)
    pyval = val.item()
    return pyval


def get_time_series(exchange, token, days, interval):
    # Get the current date and time
    now = datetime.now()

    # Set the time to midnight
    now = now.replace(hour=9, minute=0, second=0, microsecond=0)

    # Subtract days
    prev_day = now - timedelta(days=days)

    # Get the timestamp for the previous day
    prev_day_timestamp = prev_day.timestamp()

    # Use the prev_day_timestamp in your api call
    ret = api.get_time_price_series(exchange=exchange, token=token, starttime=prev_day_timestamp, interval=interval)
    if ret:
        return pd.DataFrame(ret)
    else:
        print("No Data for the given exchange, token, days and interval")

while i>1:

    #current time

    def get_current_time():
        current_time = datetime.now()
        time_str = current_time.strftime('%H%M%S')
        return int(time_str)    
    current_time = get_current_time()


    #Calculating SuperTrend

    def supertrend(exchange, token, days, interval, ATR, Multi):
        # Get the time series data
        df = get_time_series(exchange, token, days, interval)
        df = df.sort_index(ascending=False)
        df[['into','intl','intc','inth']] = df[['into','intl','intc','inth']].apply(pd.to_numeric)
        #df[['into','intl','intc','inth']]
        sti = ta.supertrend(df['inth'], df['intl'], df['intc'], length=ATR, multiplier=Multi)
        sti = sti.sort_index(ascending=True)
        
        
        sti['super_trend'] = sti[['SUPERT_20_2.0']]
        result = pd.concat([df, sti], axis=1)
        results = result.sort_index(ascending=True).rename(columns={'SUPERTd_20_2.0': 'signal', 'SUPERTl_20_2.0': 'S_UPT','SUPERTs_20_2.0': 'S_DT'})
        results[['into','inth','intl','intc','SUPERT_20_2.0','signal']]=results[['into','inth','intl','intc','SUPERT_20_2.0','signal']].apply(pd.to_numeric)
        return results[['time','into','inth','intl','intc','signal','SUPERT_20_2.0','S_UPT','S_DT']]


    #exchange, token, days, interval, ATR, Multi
    df = supertrend('NSE', '1333', 4, 10, 20, 2)
    df = df.set_index('time')
    df = df.sort_index(ascending=True)

    # LTP = current price

    ret1= api.get_quotes(exchange='NSE', token='1333')
    LTP = ret1['lp']
    LTP = float(LTP)

    


    #data sorting and close data of every 10min interval candle

    data = get_time_series('NSE',"1333",4,10)
    data= data.rename(columns={'intc':'close'})
    data=data.sort_values(by='time', ascending=True)



    #Calculate SMA20 
    sma20 = data.ta.sma(20)

    #Calculating Bollinger Bands

    data = data.drop(columns=['stat'])
    data = data.drop(columns=['time'])

    rstd = data.rolling(window=20).std()
    print(rstd)



    #Organising Previous Candle Data into relevent variables

    sig=df["signal"].iloc[-1]
    sig=float32(sig)

    low=df["intl"].iloc[-1]
    low=float64(low)
    
    high=df["inth"].iloc[-1]
    high=float64(high)

    op=df["into"].iloc[-1]
    op=float64(op)

    close=df["intc"].iloc[-1]
    close=float64(close)

    sma20v=sma20.iloc[-1]
    sma20v=float64(sma20v)
    

    Candle_Size= high-low
    

    
    
    q=3
    # q=300/round((Candle_Size*1000),4)
    #quantity 

    #LONG TP AND SL 

    Buy_tp= round(high+(Candle_Size*2),4)
    Buy_Sl = low-0.0025


    #SHORT TP AND SL 

    Sell_tp= round(low-(Candle_Size*2),4)
    Sell_Sl= high+0.0025  


 #Entry and Exit conditions

    if 100000 < get_current_time() < 153000:


     #BB Break Strategy



     #Retracement Strategy

        if sig==1 and sma20v>=low and op>=sma20v and close>=op and high<=LTP:
            Order_Entry = api.place_order(buy_or_sell='B', product_type='I',exchange='CDS', tradingsymbol='USDINR28MAR23F', quantity=q, discloseqty=q,price_type='MKT', price=0, trigger_price=None ,retention='DAY', remarks='Buy order')
            Order_SL = api.place_order(buy_or_sell='S', product_type='I',exchange='CDS', tradingsymbol='USDINR28MAR23F', quantity=q, discloseqty=q,price_type='SL-LMT', price=Buy_Sl, trigger_price=Buy_Sl,retention='DAY', remarks='SL order')
            Order_Tp = api.place_order(buy_or_sell='S', product_type='I',exchange='CDS', tradingsymbol='USDINR28MAR23F', quantity=q, discloseqty=q,price_type='LMT', price=Buy_tp, trigger_price= None,retention='DAY', remarks='TP order')
            break


        elif sig==-1 and sma20v<=high and op<=sma20v and close<=op and low>=LTP:
            Order_Entry = api.place_order(buy_or_sell='S', product_type='I',exchange='CDS', tradingsymbol='USDINR28MAR23F', quantity=q, discloseqty=q,price_type='MKT', price=0, trigger_price=None ,retention='DAY', remarks='Buy order')
            Order_SL = api.place_order(buy_or_sell='B', product_type='I',exchange='CDS', tradingsymbol='USDINR28MAR23F', quantity=q, discloseqty=q,price_type='SL-LMT', price=Sell_Sl, trigger_price=Sell_Sl,retention='DAY', remarks='SL order')
            Order_Tp = api.place_order(buy_or_sell='B', product_type='I',exchange='CDS', tradingsymbol='USDINR28MAR23F', quantity=q, discloseqty=q,price_type='LMT', price=Buy_tp, trigger_price= None,retention='DAY', remarks='TP order')
            break




    #Just for checking whether the loop is running correctly
    


#Order Details

ret = api.get_trade_book()
print('Order executed : ',ret['stat'])
print('Buy/Sell : ',ret['trantype'])
print('Quantity : ',ret['fillshares'])
print('Price : ',ret['avgprc'])
print(info)
api.logout()



