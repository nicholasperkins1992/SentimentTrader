import yfinance as yf

# This uses a scarper around Yahoo Finance to get the current price of a stock, this was chosen since there is not licence needed, however rate limiting may be an issue.
# https://github.com/ranaroussi/yfinance
def get_stock_price(ticker):
    company = yf.Ticker(ticker)

    info = company.info

    return info.get('currentPrice')