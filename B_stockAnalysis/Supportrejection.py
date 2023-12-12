import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_yearly_stock_data(ticker, year):
    stock_data = yf.Ticker(ticker).history(period=f"{year}y")
    return stock_data

def fibonacci_retracement(data):
    high = data['High'].max()
    low = data['Low'].min()
    
    fib_levels = [high, high - (0.236 * (high - low)), high - (0.382 * (high - low)), high - (0.5 * (high - low))]
    
    return fib_levels

def identify_support_and_rejection(data, fib_levels, bullish):
    if bullish:
        support_level = fib_levels[2]  # 0.5 Fibonacci level
        rejection_level = fib_levels[3]  # Upper level
    else:
        support_level = fib_levels[3]  # Upper level
        rejection_level = fib_levels[2]  # 0.5 Fibonacci level
    
    support_dates = []
    rejection_dates = []
    
    for index, row in data.iterrows():
        if row['Low'] < support_level and row['Close'] > support_level:
            support_dates.append(index)
        elif row['High'] > rejection_level and row['Close'] < rejection_level:
            rejection_dates.append(index)
    
    return support_dates, rejection_dates

def plot_fibonacci_retracement(data, fib_levels, support_dates, rejection_dates, title):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label='Close Price', color='blue')
    
    for level in fib_levels:
        plt.axhline(level, color='red', linestyle='--')
    
    plt.scatter(support_dates, data.loc[support_dates]['Low'], color='green', marker='^', label='Support Level')
    plt.scatter(rejection_dates, data.loc[rejection_dates]['High'], color='purple', marker='v', label='Rejection Level')
    
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def levelfind(stock,bull):
    print(stock)
    if stock=='HDFCBANK':
        ticker = 'HDFCBANK.NS'
    elif stock =="BANKNIFTY":
        ticker = '^NSEBANK'
    else:
        print("Enter correct ticket")
    year = 1
    
    stock_data = get_yearly_stock_data(ticker, year)
    fib_levels = fibonacci_retracement(stock_data)
    if bull=="Bullish":
        bullish = True  #########################################
    else:
        bullish=False
        
    support_dates, rejection_dates = identify_support_and_rejection(stock_data, fib_levels, bullish)
    
    plot_fibonacci_retracement(stock_data, fib_levels, support_dates, rejection_dates, 'Yearly Fibonacci Retracement Analysis')
