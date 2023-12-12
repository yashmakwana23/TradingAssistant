
def autoTrailingSL(buyPrice,temprice,StopLoss,placedorderid,Tqty,exSeg,tok,stopLoss_percentage):
    temprice,StopLoss,buyPrice,Tqty,placedorderid,stopLoss_percentage=temprice,StopLoss,buyPrice,Tqty,placedorderid,stopLoss_percentage
    from neo_api_client import NeoAPI
    
    def on_message(message):
        global temprice,StopLoss,buyPrice,Tqty,placedorderid,stopLoss_percentage
        try:
            currentPrice=round(float(message[0]['ltp']),2)
            print(f'currentPrice:{currentPrice} SL:{StopLoss} TP:{temprice} Bool:{currentPrice-StopLoss>=temprice*0.2}')
            if stopLoss_percentage==0.15:
                Tper,Pper=0.2,0.1
            else:
                Tper,Pper=0.1,0.05
            if currentPrice-StopLoss>=temprice*Tper:
                StopLoss=round(float(StopLoss+(buyPrice*Pper)),1)
                temprice=round(float(temprice + (buyPrice*Pper)),1)
                moddata=client.modify_order(order_id = str(placedorderid), price = str(StopLoss), quantity =  str(Tqty), trigger_price = str(StopLoss), validity = "DAY", order_type = "SL", amo = "")
                print(moddata)
        except Exception as e:
             print("Exception when calling Live Data->positions: %s\n" % e)

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

    inst_tokens = [{"instrument_token": int(tok), "exchange_segment": exSeg}] #HDFC

    try:
        client.subscribe(instrument_tokens=inst_tokens)
    except Exception as e:
        print("Exception while connection to socket->socket: %s\n" % e)

from neo_api_client import NeoAPI
import json
with open('E_tokens\kotakToken.json', 'r') as file:
    token_data = json.load(file)

key = token_data.get("consumer_key")
secret=token_data.get("consumer_secret")
email=token_data.get("mobilenumber")
paswd=token_data.get("password")
otp=token_data.get("OTP")

client = NeoAPI(consumer_key=key, consumer_secret=secret, 
                environment='prod', on_message=None, on_error=None, on_close=None, on_open=None)
client.login(mobilenumber=email, password=paswd)
client.session_2fa(OTP=otp)

try:
    # Gathering all Details
    allPositions = client.positions()
    tradeHistory = client.trade_report()

    # Initialization of Lists and Dictionaries
    activePosition = {}
    PositionNames,activeTradeHistory = [],[]

    # Accessing first position data
    for Pos in allPositions['data']:
        FLB,FLS=int(Pos['flBuyQty']),int(Pos['flSellQty'])
        if FLB-FLS != 0:
            activePosition[Pos['trdSym']] = Pos
            PositionNames.append(Pos['trdSym'])
    print(PositionNames)
    if len(PositionNames)>1:
        Trade=input("For which trade you want to enable?:\t")
    else:
        Trade=0
    # Finds avg tradeValue of active transactions
    for sym in PositionNames:
        if int(Trade)==PositionNames.index(sym):
            Scount, Bcount, Bqty, Sqty, Sprice, Bprice = 0, 0, 0, 0, 0, 0
            buyPrice, Tqty, temprice, StopLoss, Ttpe = 0, 0, 0, None, None
            tradehistorylist=tradeHistory['data']
            tradehistorylist.reverse()
            for orders in tradehistorylist:
                if sym == orders['trdSym']:
                    if orders['trnsTp'] == 'B':
                        Bqty += int(orders['fldQty'])
                        Bprice += round(float(orders['avgPrc']), 2)
                        Bcount += 1
                    else:
                        Sqty += int(orders['fldQty'])
                        Sprice += round(float(orders['avgPrc']), 2)
                        Scount += 1
                    if Bqty == Sqty:
                        print("Resting")
                        Scount, Bcount, Bqty, Sqty, Sprice, Bprice = 0, 0, 0, 0, 0, 0

            if Sqty != Bqty:
                if Bqty > Sqty: buyPrice,Tqty,Ttpe = Bprice / Bcount,Bqty - Sqty,'B'
                else:           buyPrice,Tqty,Ttpe = Bprice / Bcount,Sqty - Bqty,'S'

                temprice = buyPrice

                if buyPrice>250:
                    stopLoss_percentage = 0.05
                else:
                    stopLoss_percentage=0.15
                StopLoss = round(float(buyPrice * (1 - stopLoss_percentage)),1)
                tradedetails = activePosition.get(sym)
                print(sym,buyPrice,Tqty)
                try:
                    # Place an Order
                    orderdetails = client.place_order(
                        exchange_segment=tradedetails['exSeg'],
                        product=tradedetails['prod'],
                        price=str(StopLoss),
                        order_type="SL",
                        quantity=str(Tqty),
                        validity="DAY",
                        trading_symbol=tradedetails['trdSym'],
                        transaction_type="S",
                        amo="NO",
                        disclosed_quantity="0",market_protection="0",pf="N",
                        trigger_price=StopLoss,
                        tag=None
                    )
                    placedorderid = orderdetails['nOrdNo']
                    autoTrailingSL(buyPrice,temprice,StopLoss,placedorderid,Tqty,tradedetails['exSeg'],tradedetails['tok'],stopLoss_percentage)
                    print(placedorderid)
                except Exception as e:
                    print("Exception when calling OrderApi->place_order: %s\n" % e)

                print("Placing Order Completed")

except Exception as e:
    print("Exception when calling PositionsApi->positions: %s\n" % e)

