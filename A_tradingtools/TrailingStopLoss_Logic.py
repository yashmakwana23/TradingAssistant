global price
global qty
global Stoplossamount

import random

def get_stock_price():
    # Simulate getting stock price
    return round(random.uniform(95, 150), 2)


price = get_stock_price()
# print(f"The current stock price is: {price}")



qty=10
price=100
Losspercent= 0.1
CapLoss=qty*price*Losspercent
Stoplossamount=round(((qty*price)-CapLoss)/qty) #Trigger Sell Price 
# print('StopLoss: ',Stoplossamount)

for a in range(10):
    currentprice=get_stock_price()
    print("*** Round ",a," ***")
    print(f'Current stockprice: {currentprice}')

    con1=currentprice*qty
    con2=Stoplossamount*qty
    con3=price*qty
    print("Set Stoploss: ",Stoplossamount," | ","Buy Price: ",price)
 
    if (con1-con2 > con3*0.2):
        Stoplossamount=round(Stoplossamount+price*0.1)
        print("New StopLoss: ",Stoplossamount ,"\n")
    else:
        if Stoplossamount>currentprice:
            print("\n StopLoss Hit: Position Exit")
            exit()
        else:
            print("No Changes \n")