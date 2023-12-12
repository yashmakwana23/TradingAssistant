import time
import json
import sys
import threading
sys.path.append(".")  
import subprocess

def UpdatecurrentPosDetails():
    from neo_api_client import NeoAPI
    from C_alerts.SendDiscordMessage import PosdcMessage

    def on_message(message):
        print(message)

    from neo_api_client import NeoAPI
    with open('E_tokens\kotakToken.json', 'r') as file:
        token_data = json.load(file)

    key = token_data.get("consumer_key")
    secret=token_data.get("consumer_secret")
    email=token_data.get("mobilenumber")
    paswd=token_data.get("password")
    otp=token_data.get("OTP")

    client = NeoAPI(consumer_key=key, consumer_secret=secret, 
                    environment='prod', on_message=on_message, on_error=None, on_close=None, on_open=None)
    client.login(mobilenumber=email, password=paswd)
    client.session_2fa(OTP=otp)

    i=1
    Pricelist={}
    DCValue=""
    try:
        Posdata=client.positions()
        NoPos=len(Posdata['data'])

        for a in range(NoPos):
            TradeStatus=int(Posdata['data'][a]['flBuyQty'])-int(Posdata['data'][a]['flSellQty'])
            PnL=float(Posdata['data'][a]['sellAmt'])-float(Posdata['data'][a]['buyAmt'])
            TSegment=Posdata['data'][a]['exSeg']
            Token=Posdata['data'][a]['tok']            
            Symbl=Posdata['data'][a]['trdSym']
            Tmultiplier=int(Posdata['data'][a]['multiplier']    ) 
            TlotSz=int(Posdata['data'][a]['lotSz']    ) 
            Pricelist[a]=[TradeStatus,PnL,TSegment,Token,Symbl,TlotSz,Tmultiplier]       
        for a in Pricelist:
            data=Pricelist.get(a)
            if data[0]==0:
                DCValue=DCValue+ str(f'Closed: {data[4]} | PnL: {data[1]} \n') 
        
            else:
                inst_tokens = [{"instrument_token": str(data[3]), "exchange_segment": data[2]}]
                updatedprice=client.quotes(instrument_tokens=inst_tokens, quote_type="ltp", isIndex=False)
                currentvalue=float(updatedprice['message'][0]['ltp'])
                data1=float(Posdata['data'][a]['buyAmt'])-float(Posdata['data'][a]['sellAmt'])
                oldbuyingprice=float(data1)/int(data[0]*data[5]*data[6]) 
                DCValue=DCValue+str(f'Active: {data[4]} | PnL: {(currentvalue-oldbuyingprice)*data[5]*data[6]} \n')
    except Exception as e:
        print("Exception when calling PositionsApi->positions: %s\n" % e)
    PosdcMessage(DCValue,"1166470394719518790")
    return(DCValue)   
    # 

def runsscript(Durs,Mins):
    Dur = Durs
    Min = Mins
    i = Dur/Min
    print(i)
    while i >0:
        print(UpdatecurrentPosDetails())

        time.sleep(60*Min)
        i=i-1

if __name__ == "__main__":
    runsscript(60,5)