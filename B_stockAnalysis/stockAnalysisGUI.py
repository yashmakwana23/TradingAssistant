import tkinter as tk
from tkinter import ttk
import sys
import threading
sys.path.append(".")  
import subprocess

def PricePrediction():
    subprocess.Popen(['python','B_stockAnalysis\Prediction\PricePredictionClose.py']) 

def TrendAnalysis(stockName):
    from B_stockAnalysis.trendAnalysis import trend
    sname=stockName.get()
    threading.Thread(target=trend,args=(sname,)).start()

def setup_action(level_name_store,level_trend_store):
    from B_stockAnalysis.Supportrejection import levelfind
    stockName = level_name_store.get()
    stockTrend = level_trend_store.get()
    print(stockName," : ",stockTrend)
    threading.Thread(target=levelfind,args=(stockName, stockTrend)).start()

def go_back(root):
    from main import mainGui  # Adjust the import statement
    print("Main Page Opening")
    for widget in root.winfo_children():
        widget.destroy()
    mainGui(root)


# Create the main window
def taGui(root):

    # root = tk.Tk()
    root.title("Trading App")
    root.geometry("800x300")
    root.configure(bg='#f0f0f0')


    ##\** Price Prediction Section 1 **/#
    prediction_Frame = ttk.Frame(root, borderwidth=2, relief="solid")
    prediction_Frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    #->heading of section1
    heading1 = ttk.Label(prediction_Frame, text="Price Prediction", font=("Arial", 16, "bold"))
    heading1.pack(pady=(10, 5))
    #->Dropdown Menu
    Prediction_Stock_options = ["BANKNIFTY", "HDFCBANK", "Stock 3"]
    Selected_Stock_Prediction = tk.StringVar()
    Prediction_dropdown = ttk.Combobox(prediction_Frame, values=Prediction_Stock_options, textvariable=Selected_Stock_Prediction)
    Prediction_dropdown.pack(pady=(5, 10))
    #->Price Prediction Button
    Prediction_button_buy = ttk.Button(prediction_Frame, text="Submit", command=PricePrediction)
    Prediction_button_buy.pack(pady=(5, 5))
    

    ##\** Trend Analysis Section 2 **/##
    stockTrend_Frame = ttk.Frame(root, borderwidth=2, relief="solid")
    stockTrend_Frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    #->heading of section2
    heading2 = ttk.Label(stockTrend_Frame, text="Trend Analysis", font=("Arial", 16, "bold"))
    heading2.pack(pady=(10, 5))
    #->Dropdown Menu
    trend_options = ["BANKNIFTY", "HDFCBANK", "Stock 3"]
    trend_var = tk.StringVar()
    trend_dropdown = ttk.Combobox(stockTrend_Frame, values=trend_options, textvariable=trend_var)
    trend_dropdown.pack(pady=(5, 10))
    
    #->Trend Button  
    trend_button_start = ttk.Button(stockTrend_Frame, text="Submit", command=lambda:TrendAnalysis(trend_var))
    trend_button_start.pack(pady=(5, 5))


    ##\** Level Identifcation Section 3 **/##
    levels_frame3 = ttk.Frame(root, borderwidth=2, relief="solid")
    levels_frame3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    #->heading of section3
    heading3 = ttk.Label(levels_frame3, text="Support Levels", font=("Arial", 16, "bold"))
    heading3.pack(pady=(10, 5))
    #->Dropdown Menu
    level_stock_name = ["BANKNIFTY", "HDFCBANK", "Stock 3"]
    level_name_store = tk.StringVar()
    level_stock_dropdown = ttk.Combobox(levels_frame3, values=level_stock_name, textvariable=level_name_store)
    level_stock_dropdown.pack(pady=(5, 10))
    #->Dropdown Menu II
    level_trend = ["Bullish", "Bearish"]
    level_trend_store = tk.StringVar()
    level_stock_dropdown2 = ttk.Combobox(levels_frame3, values=level_trend, textvariable=level_trend_store)
    level_stock_dropdown2.pack(pady=(5, 10))
    #-> Levels Button
    level_setup_button = ttk.Button(levels_frame3, text="Submit", command=lambda:setup_action(level_name_store,level_trend_store))
    level_setup_button.pack(pady=(5, 10))

    #backbutton
    back_button = ttk.Button(root, text="Back", command=lambda:go_back(root))
    back_button.grid(row=1, column=2, pady=(10, 10), sticky="se")


    # Configure grid weights for equal sizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    # Run the main loop
    root.mainloop()
    
if __name__ == "__main__":
    root = tk.Tk()
    taGui(root)