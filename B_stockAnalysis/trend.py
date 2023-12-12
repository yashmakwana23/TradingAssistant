import yfinance as yf
import pandas_ta as ta

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

if __name__ == '__main__':
    ticker = '^NSEBANK'
    
    one_month_data = get_stock_data(ticker, '1mo')
    one_month_trend = analyze_trend(one_month_data)

    yearly_data = get_stock_data(ticker, '1y')
    yearly_trend = analyze_trend(yearly_data)

    print(f"1-Month Trend for {ticker}: {one_month_trend}")
    print(f"Yearly Trend for {ticker}: {yearly_trend}")
