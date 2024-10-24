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

 def update_stock_position(trading_date, symbol, new_quantity, buying_price):
    df = pd.read_csv(STOCK_POSITION_FILE)

    # Update the specific row where symbol and trading_date match
    df.loc[(df['trading_date'] == trading_date) & (df['symbol'] == symbol), 'quantity'] = new_quantity
    df.to_csv(STOCK_POSITION_FILE, index=False)

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
    
def delete_stock_position(trading_date, symbol):
    df = pd.read_csv(STOCK_POSITION_FILE)

    # Delete the row where symbol and trading_date match
    df = df[~((df['trading_date'] == trading_date) & (df['symbol'] == symbol))]
    df.to_csv(STOCK_POSITION_FILE, index=False)

def init_cash_position(self):
    if not os.path.exists(CASH_POSITION_FILE):
        data = {'date': [pd.Timestamp.now().strftime('%Y-%m-%d')], 'cash_balance': [0.00]}  # Initial balance $0
        df = pd.DataFrame(data)
        df.to_csv(CASH_POSITION_FILE, index=False)
        print(f"Initialized {CASH_POSITION_FILE} with $10,000 balance.")
    else:
        print(f"{CASH_POSITION_FILE} already exists.")

def init_stock_position(self):
    if not os.path.exists(STOCK_POSITION_FILE):
        data = {'trading_date': [], 'symbol': [], 'quantity': [], 'buying_price': []}
        df = pd.DataFrame(data)
        df.to_csv(STOCK_POSITION_FILE, index=False)
        print(f"Initialized {STOCK_POSITION_FILE} as an empty file.")
    else:
        print(f"{STOCK_POSITION_FILE} already exists.")