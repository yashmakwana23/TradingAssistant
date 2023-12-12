import time
import json
import sys
import threading
sys.path.append(".")  

def Updatedetails(StockName):
    from neo_api_client import NeoAPI
    from C_alerts.SendDiscordMessage import PosdcMessage


    def on_message(message):
        print("here def_onmessage",message)

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

    try:
        if StockName=='HDFCBANK':
            inst_tok="1333"
        elif StockName=='RELIANCE':
            inst_tok="2885"
        else:
            inst_tok="257739" #259487 Feb24
        # print(inst_tok,type(inst_tok))
        inst_tokens = [{"instrument_token": inst_tok, "exchange_segment": "nse_cm"}]
        # get LTP and Market Depth Data
        DCValue=client.quotes(instrument_tokens=inst_tokens, quote_type="ltp", isIndex=False)
        stockLTP=f"{DCValue['message'][0]['trading_symbol']} : {DCValue['message'][0]['ltp']}"
        
        print(DCValue)
    
    except Exception as e:
        print("Exception when calling PositionsApi->positions: %s\n" % e)
    PosdcMessage(stockLTP,"1166470364306612304")
    

    return(DCValue)   

def quotesscript(StockName):
    Dur = 60
    Min = 5
    i = Dur/Min
    print(i)
    while i >0:
        print(Updatedetails(StockName))

        time.sleep(60*Min)
        i=i-1

if __name__ == "__main__":
    quotesscript("RELIANCE")