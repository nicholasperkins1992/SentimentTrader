import yfinance as yf

msft = yf.Ticker("MSFT")

info = msft.info

current_price = info.get('currentPrice')

print(f"Current price of MSFT: {current_price}")
