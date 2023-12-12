import json

def call_button_clicked():
    from neo_api_client import NeoAPI
    import json
    with open('E_tokens\kotakToken.json', 'r') as file:
        token_data = json.load(file)

    key = token_data.get("consumer_key")
    secret=token_data.get("consumer_secret")
    email=token_data.get("mobilenumber")
    paswd=token_data.get("password")
    otp=token_data.get("OTP")

    trade_client = NeoAPI(consumer_key=key, consumer_secret=secret, 
                    environment='prod', on_message=None, on_error=None, on_close=None, on_open=None)
    trade_client.login(mobilenumber=email, password=paswd)
    trade_client.session_2fa(OTP=otp)


    from NorenRestApiPy.NorenApi import  NorenApi
    import pyotp

    class ShoonyaApiPy(NorenApi):
        def __init__(self):
            NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
            global api
            api = self

    Shonya = ShoonyaApiPy()

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


    ret = Shonya.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)

    # Shonya.place_order(buy_or_sell='B', product_type='C',exchange='NSE', tradingsymbol='RPOWER-EQ', quantity=1, discloseqty=1,price_type='MKT', price=0, trigger_price=None ,retention='DAY', remarks='Buy order')

    trade_client.place_order(exchange_segment="nse_cm", product="NRML", price="", order_type="MKT", quantity="1", validity="DAY", trading_symbol="RPOWER-EQ",
                       transaction_type="B", amo="NO", disclosed_quantity="0", market_protection="0", pf="N",
                       trigger_price="0", tag=None)
    print("Call executed")


def put_button_clicked():
    from neo_api_client import NeoAPI
    import json
    with open('E_tokens\kotakToken.json', 'r') as file:
        token_data = json.load(file)

    key = token_data.get("consumer_key")
    secret=token_data.get("consumer_secret")
    email=token_data.get("mobilenumber")
    paswd=token_data.get("password")
    otp=token_data.get("OTP")

    trade_client = NeoAPI(consumer_key=key, consumer_secret=secret, 
                    environment='prod', on_message=None, on_error=None, on_close=None, on_open=None)
    trade_client.login(mobilenumber=email, password=paswd)
    trade_client.session_2fa(OTP=otp)

    from NorenRestApiPy.NorenApi import  NorenApi
    import pyotp

    class ShoonyaApiPy(NorenApi):
        def __init__(self):
            NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
            global api
            api = self

    Shonya = ShoonyaApiPy()

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


    ret = Shonya.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)

    # Shonya.place_order(buy_or_sell='S', product_type='C',exchange='NSE', tradingsymbol='RPOWER-EQ', quantity=1, discloseqty=1,price_type='MKT', price=0, trigger_price=None ,retention='DAY', remarks='Buy order')

    trade_client.place_order(exchange_segment="nse_cm", product="NRML", price="", order_type="MKT", quantity="1", validity="DAY", trading_symbol="RPOWER-EQ",
                       transaction_type="S", amo="NO", disclosed_quantity="0", market_protection="0", pf="N",
                       trigger_price="0", tag=None)
    print("Put executed")