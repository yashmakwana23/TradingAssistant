
def AUTOTSL(StopLoss,PositionNo):
    global price
    global qty
    def on_message(message):
        global Stoplossamount
        try:
            currentprice=float(message[0]["ltp"])
            print(currentprice)
            con1=currentprice*qty
            con2=Stoplossamount*qty
            con3=price*qty
            if (con1-con2 > con3*0.2):
                Stoplossamount=round(Stoplossamount+price*0.1)
                moddata=client.modify_order(order_id = str(placedorderid), price = str(Stoplossamount), quantity =  str(qty), trigger_price = str(Stoplossamount), validity = "DAY", order_type = "SL", amo = "")
                print(moddata)
            else:
                print("else")
        except:
            pass

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
                    environment='prod', on_message=on_message, on_error=None, on_close=None, on_open=None)
    client.login(mobilenumber=email, password=paswd)
    client.session_2fa(OTP=otp)


    #Getting active positions details
    try:
        pos_details=client.positions()


        Ourpos_details=pos_details['data'][int(PositionNo)]

    except Exception as e:
        print("Exception when calling PositionsApi->positions: %s\n" % e)
        print("Non Data Available")
        exit()
    
    qty=int(Ourpos_details['flBuyQty'])-int(Ourpos_details['flSellQty'])
    print(qty)
    if qty==0:
        print("No Position Active")
        exit()
    price=(float(Ourpos_details['buyAmt'])-float(Ourpos_details['sellAmt']))/qty

    #Stoploss calculate
    Losspercent= StopLoss
    CapLoss=qty*price*float(Losspercent)
    Stoplossamount=round(((qty*price)-CapLoss)/qty)
    print(Stoplossamount)
    #Placing stoploss
    try:
        # Place a Order
        orderdetails=client.place_order(exchange_segment=Ourpos_details['exSeg'], product=Ourpos_details['prod'], price=str(Stoplossamount), order_type="SL", quantity=str(qty), validity="DAY", trading_symbol=Ourpos_details['trdSym'],
                        transaction_type="S", amo="NO", disclosed_quantity="0", market_protection="0", pf="N",
                        trigger_price=Stoplossamount, tag=None)
        placedorderid=orderdetails['nOrdNo']
    except Exception as e:
        print("Exception when calling OrderApi->place_order: %s\n" % e)

    print("Placing Order Completed")

    inst_tokens = [{"instrument_token": Ourpos_details['tok'], "exchange_segment": Ourpos_details['exSeg']}]

    try:
        client.subscribe(instrument_tokens=inst_tokens)
    except Exception as e:
        print("Exception when calling Scrip Master Api->scrip_master: %s\n" % e)

