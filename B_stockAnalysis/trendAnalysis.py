def analyze_trend(stock):
    import yfinance as yf
    import matplotlib.pyplot as plt

    # Replace 'AAPL' with the ticker symbol of the stock you want to analyze
    ticker = stock

    # Fetch data from Yahoo Finance
    stock_data = yf.download(ticker, start='2023-01-01', end='2023-12-31')

    # Calculate moving averages
    short_window = 10
    long_window = 50

    stock_data['Short_MA'] = stock_data['Close'].rolling(window=short_window).mean()
    stock_data['Long_MA'] = stock_data['Close'].rolling(window=long_window).mean()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label='Close Price')
    plt.plot(stock_data['Short_MA'], label='Short MA (10-day)')
    plt.plot(stock_data['Long_MA'], label='Long MA (50-day)')
    plt.title(f'{ticker} Stock Price with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    # Determine the trend based on moving average crossovers
    if stock_data['Short_MA'].iloc[-1] > stock_data['Long_MA'].iloc[-1]:
        trend = "Bullish Trend"
        color = 'green'
    elif stock_data['Short_MA'].iloc[-1] < stock_data['Long_MA'].iloc[-1]:
        trend = "Bearish Trend"
        color = 'red'
    else:
        trend = "Indecisive Trend"
        color = 'black'

    # Annotate the current trend on the plot
    plt.text(stock_data.index[-1], stock_data['Close'].iloc[-1], trend, fontsize=12, ha='right', color=color)

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
    analyze_trend(ticker)

