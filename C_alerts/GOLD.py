from neo_api_client import NeoAPI
from SendDiscordMessage import dcMessage
def on_message(message):
    try:
        sltp=message[0]["ltp"]
        print(sltp)
        dcMessage(sltp,1166470364306612304)
    except:
        pass
    # print(message)


def on_error(message):
    result = message
    print('[OnError]: ', result)
    
def on_open(message):
    print('[OnOpen]: ', message)
    
def on_close(message):
    print('[OnClose]: ', message)

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

#259487 Feb24

inst_tokens = [{"instrument_token": 257739, "exchange_segment": "nse_cm"}]

try:
    client.subscribe(instrument_tokens=inst_tokens)
    print("test")
    # data=client.quotes(instrument_tokens=inst_tokens)

except Exception as e:
    print("Exception when calling Scrip Master Api->scrip_master: %s\n" % e)


