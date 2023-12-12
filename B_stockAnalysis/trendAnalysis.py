import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt

def get_stock_data(ticker, period):
    stock_data = yf.Ticker(ticker).history(period=period)
    return stock_data

def analyze_trend(data):
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()

    if data['SMA_50'].iloc[-1] > data['SMA_200'].iloc[-1]:
        return 'bullish'
    else:
        return 'bearish'


def plot_stock_data(data, current_trend, monthly_trend, yearly_trend):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['SMA_50'], label='50-day SMA', color='orange')
    plt.plot(data['SMA_200'], label='200-day SMA', color='green')
    
    plt.title('Stock Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    # Add trend annotations
    plt.annotate(f'Current Trend: {current_trend}', 
                 xy=(data.index[-1], data['Close'].iloc[-1]),
                 xytext=(-20, 20),
                 textcoords='offset points',
                 fontsize=10,
                 fontweight='bold',
                 color='purple')

    plt.annotate(f'1-Month Trend: {monthly_trend}', 
                 xy=(data.index[-1], data['Close'].iloc[-1] - 10),  # Adjusting vertical position
                 xytext=(-20, 20),
                 textcoords='offset points',
                 fontsize=10,
                 fontweight='bold',
                 color='blue')  

    plt.annotate(f'Yearly Trend: {yearly_trend}', 
                 xy=(data.index[-1], data['Close'].iloc[-1] - 20),  # Adjusting vertical position
                 xytext=(-20, 20),
                 textcoords='offset points',
                 fontsize=10,
                 fontweight='bold',
                 color='red')  

    plt.show()


def trend(stock):
    print(stock)
    if stock=='HDFCBANK':
        ticker = 'HDFCBANK.NS'
    elif stock=="BANKNIFTY":
        ticker = '^NSEBANK'
    else:
        print("Enter Correct Stock Symbol")
        return
    
    one_month_data = get_stock_data(ticker, '1mo')
    one_month_trend = analyze_trend(one_month_data)

    yearly_data = get_stock_data(ticker, '1y')
    yearly_trend = analyze_trend(yearly_data)

    print(f"1-Month Trend for {ticker} (Last 30 days): {one_month_trend}")
    print(f"Yearly Trend for {ticker} (Last 365 days): {yearly_trend}")

    # Plotting the stock data with current trend annotation
    plot_stock_data(yearly_data, yearly_trend, one_month_trend, yearly_trend)


# Example usage
