import dao
import pandas as pd
from datetime import datetime

def buy_stock(symbol, price_per_share, quantity):
    cash_balance = dao.get_remaining_cash()
    if cash_balance is None:
        raise Exception("No cash balance available.")
    
    total_cost = price_per_share * quantity
    
    if cash_balance < total_cost:
        raise Exception(f"Insufficient cash to buy {quantity} shares of {symbol}.")
    
    new_cash_balance = cash_balance - total_cost
    dao.save_cash_position(new_cash_balance)
    
    dao.save_stock_position(symbol, quantity, price_per_share)
    
    print(f"Successfully bought {quantity} shares of {symbol} at ${price_per_share:.2f} each.")
    print(f"New cash balance: ${new_cash_balance:.2f}")


def sell_stock(symbol, quantity):
    stock_data = dao.get_stock_position(symbol)
    
    if stock_data is None or stock_data.empty:
        raise Exception(f"No shares of {symbol} available to sell.")
    
    total_quantity_held = stock_data['quantity'].sum()
    
    if total_quantity_held < quantity:
        raise Exception(f"Not enough shares of {symbol} to sell. You only have {total_quantity_held} shares.")
    
    #first buy first sell, TODO: add sell specific share
    stock_data = stock_data.sort_values(by='trading_date') 
    
    remaining_quantity = quantity
    total_revenue = 0
    
    updated_rows = []
    
    for index, row in stock_data.iterrows():
        available_quantity = row['quantity']
        
        if available_quantity >= remaining_quantity:
            sell_quantity = remaining_quantity
            remaining_quantity = 0
        else:
            sell_quantity = available_quantity
            remaining_quantity -= sell_quantity
        
        total_revenue += sell_quantity * row['buying_price']
        
        if available_quantity > sell_quantity:
            updated_rows.append({
                'trading_date': row['trading_date'],
                'symbol': row['symbol'],
                'quantity': available_quantity - sell_quantity,
                'buying_price': row['buying_price']
            })
        
        if remaining_quantity == 0:
            break
    
    # update stock CSV
    updated_df = pd.DataFrame(updated_rows)
    dao.save_stock_position(symbol, updated_df)
    
    # update cash CSV
    cash_balance = dao.get_remaining_cash()
    new_cash_balance = cash_balance + total_revenue
    dao.save_cash_position(new_cash_balance)
    
    print(f"Successfully sold {quantity} shares of {symbol}.")
    print(f"New cash balance: ${new_cash_balance:.2f}")

def get_current_shares_held(symbol):
    stock_data = dao.get_stock_position(symbol)
    
    if stock_data is None or stock_data.empty:
        return 0, 0.0
    
    total_quantity = stock_data['quantity'].sum()
    total_value = (stock_data['quantity'] * stock_data['buying_price']).sum()
    average_price = total_value / total_quantity if total_quantity > 0 else 0.0
    
    return total_quantity, average_price

def get_current_cash_balance():
    return dao.get_remaining_cash()