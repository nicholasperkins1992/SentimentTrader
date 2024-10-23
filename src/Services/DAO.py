import os
import pandas as pd
from datetime import datetime

CASH_POSITION_FILE = os.getenv("CASH_POSITION_FILE")
STOCK_POSITION_FILE = os.getenv("STOCK_POSITION_FILE")

def save_cash_position(cash_balance):
    data = {
        'date': [datetime.now().strftime('%Y-%m-%d')],
        'cash_balance': [cash_balance]
    }
    df = pd.DataFrame(data)
    df.to_csv(CASH_POSITION_FILE, mode='a', index=False, header=False)

def get_remaining_cash():
    try:
        cash_data = pd.read_csv(CASH_POSITION_FILE)
        return cash_data['cash_balance'].iloc[-1]
    except FileNotFoundError:
        return 0  

def save_stock_position(symbol, quantity, price):
    data = {
        'trading_date': [datetime.now().strftime('%Y-%m-%d')],
        'symbol': [symbol],
        'quantity': [quantity],
        'buying_price': [price]
    }
    df = pd.DataFrame(data)
    df.to_csv(STOCK_POSITION_FILE, mode='a', index=False, header=False)

def get_stock_position(symbol):
    try:
        stock_data = pd.read_csv(STOCK_POSITION_FILE)
        stock = stock_data[stock_data['symbol'] == symbol]
        if not stock.empty:
            return stock  
        else:
            return None
    except FileNotFoundError:
        return None

def get_all_stocks():
    try:
        stock_data = pd.read_csv(STOCK_POSITION_FILE)
        return stock_data  
    except FileNotFoundError:
        return pd.DataFrame()