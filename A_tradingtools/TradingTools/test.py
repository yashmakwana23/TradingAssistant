# # import tkinter as tk
# # from tkinter import ttk
# # import pandas as pd

# # def get_selected_row_data():
# #     selected_value = combo_var.get()
# #     selected_row = df[df['Symbol'] == selected_value]
# #     print(selected_row)

# # root = tk.Tk()
# # root.title("Dropdown from Excel")

# # # Read the Excel file
# # df = pd.read_excel('TradingTools\stocklist.xlsx')

# # # Get the unique values from a specific column
# # values = df['Symbol'].unique()

# # combo_var = tk.StringVar()
# # combo = ttk.Combobox(root, textvariable=combo_var, values=values)
# # combo.pack(pady=10)

# # button = ttk.Button(root, text="Get Row Data", command=get_selected_row_data)
# # button.pack(pady=10)

# # root.mainloop()
# import pandas_ta as ta
# from NorenRestApiPy.NorenApi import  NorenApi
# import pandas as pd
# import pyotp
# import math
# from datetime import datetime, timedelta
# import numpy as np
# import matplotlib.pyplot as plt


# class ShoonyaApiPy(NorenApi):
#     def __init__(self):
#         NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
#         global api
#         api = self

# api = ShoonyaApiPy()

# token = 'PAJ46A35K6SNEB53J4U43IX522X33CP5'
# otp = pyotp.TOTP(token).now()
# user        = 'FA56947'
# pwd       = 'Xyp9x@001'
# factor2     = otp
# vc          = 'FA56947_U'
# app_key     = 'b1b10ff51c7f8c21b624e5e39e94b55d'
# imei        = 'abc1234'

# ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)

# info=api.get_limits()
# print(info)
# i=2


# #converter from numpy to float

# def float64 (a):
#     val = np.float64(a)
#     pyval = val.item()
#     return pyval 

# def float32 (a):
#     val = np.float32(a)
#     pyval = val.item()
#     return pyval


# def get_time_series(exchange, token, days, interval):
#     # Get the current date and time
#     now = datetime.now()

#     # Set the time to midnight
#     now = now.replace(hour=9, minute=0, second=0, microsecond=0)

#     # Subtract days
#     prev_day = now - timedelta(days=days)

#     # Get the timestamp for the previous day
#     prev_day_timestamp = prev_day.timestamp()

#     # Use the prev_day_timestamp in your api call
#     ret = api.get_time_price_series(exchange=exchange, token=token, starttime=prev_day_timestamp, interval=interval)
#     if ret:
#         return pd.DataFrame(ret)
#     else:
#         print("No Data for the given exchange, token, days and interval")

# data = get_time_series('NSE',"14366",4,10)
# print(data)