import json
import pandas as pd
from datetime import datetime
from Services import DAO
from Services.stock import Stock
from typing import Annotated
from semantic_kernel.functions import kernel_function

class Trader: 
    
    stock_instance = Stock()

    @kernel_function(
        name="buy_stock",
        description="Purchase stock based on stock ticker symbol, trading price and quantity, for example 'Buy 10 shares of Apple at $150 each.'",
    )
    def buy_stock(self, 
        symbol: str, 
        quantity: Annotated[int, "quantity of stock"],)-> Annotated[bool, "the output is a boolean, true if successful"]:
        """
        record stock purchase action based on stock ticker symbol, trading price and quantity 

        Parameters:
        symble (str): The ticker symbol of the stock.
        price_per_share (float): trading price of the stock.
        quantity (int): trading quatity

        Returns:
        none.
        """
        cash_balance = DAO.get_remaining_cash()
        if cash_balance is None:
            raise Exception("No cash balance available.")
        
        price_per_share = float(self.stock_instance.get_stock_price(symbol))

        total_cost = price_per_share * quantity
        
        if cash_balance < total_cost:
            raise Exception(f"Insufficient cash to buy {quantity} shares of {symbol}.")
        
        new_cash_balance = cash_balance - total_cost
        DAO.save_cash_position(new_cash_balance)
        
        DAO.save_stock_position(symbol, quantity, price_per_share)
        
        return True
        
        # print(f"Successfully bought {quantity} shares of {symbol} at ${price_per_share:.2f} each.")
        # print(f"New cash balance: ${new_cash_balance:.2f}")


    @kernel_function(
        name="sell_stock",
        description="Sell stock based on stock ticker symbol, quantity and selling price, for example 'Sell 10 shares of Apple at $150 each.'",
    )
    def sell_stock(self, symbol: str, quantityToSell: int)-> Annotated[bool, "the output is a boolean, true if successful"]:
        """
        Sell the specified quantity of stock using FIFO (first in, first out) principle.

        Parameters:
        symbol (str): The stock symbol (e.g., "AAPL").
        quantityToSell (int): The number of shares to sell.
        sellingPrice (float): The price per share at which the stock is sold.

        Raises:
        Exception: If there are not enough shares available to sell.
        """
        # Step 1: Check if enough stock is available
        stock_positions = DAO.get_stock_position(symbol)

        total_quantity = stock_positions['quantity'].sum()

        if total_quantity < quantityToSell:
            raise Exception(f"Not enough {symbol} shares to sell. Available: {total_quantity}, Required: {quantityToSell}")

        # Step 2: Sell stocks based on FIFO (earliest purchases first)
        shares_to_sell = quantityToSell
        for position in stock_positions.itertuples(index=True, name='Pandas'):
            if shares_to_sell <= 0:
                break

            # Get the current lot information
            trading_date = position.trading_date
            quantity = position.quantity
            buying_price = position.buying_price

            if quantity > shares_to_sell:
                # Partial sale from this lot, reduce the quantity
                new_quantity = quantity - shares_to_sell
                DAO.update_stock_position(trading_date, symbol, new_quantity, buying_price)  # Update the CSV for this lot
                shares_to_sell = 0
            else:
                # Fully sell this lot, delete the row from CSV
                DAO.delete_stock_position(trading_date, symbol)  # Delete this lot from CSV
                shares_to_sell -= quantity

        # Step 3: Update cash position CSV by adding the sale proceeds
        sellingPrice = float(self.stock_instance.get_stock_price(symbol))
        sale_proceeds = quantityToSell * sellingPrice

        current_cash = DAO.get_remaining_cash()  # Get the current cash balance
        new_cash_position = current_cash + sale_proceeds
        DAO.save_cash_position(new_cash_position)
        
        return True

        # print(f"Sold {quantityToSell} shares of {symbol} at ${sellingPrice:.2f} per share. Cash position updated.")
        
    @kernel_function(
        name="get_current_shares_held",
        description="Get the current number of shares held for a stock by ticker symbol, for example 'How many shares of Apple do I have?'",
    )
    def get_current_shares_held(self, symbol: str)-> Annotated[str, "the output is a string of json data"]:
        stock_data = DAO.get_stock_position(symbol)
        
        if stock_data is None or stock_data.empty:
            # print(f"You have 0 shares of {symbol} stock, average acquisition price is 0.0")
            return
    
        total_quantity = stock_data['quantity'].sum()
        total_value = (stock_data['quantity'] * stock_data['buying_price']).sum()
        average_price = total_value / total_quantity if total_quantity > 0 else 0.0
        
        data = {
            "total_quantity": total_quantity,
            "symbol": symbol,
            "average_price": round(average_price, 2)
        }
        return json.dumps(data)
    
        # print(f"You have {total_quantity} shares of {symbol} stock, average acquisition price is {average_price:.2f}")

    @kernel_function(
        name="show_all_stock_positions",
        description="Display all stock positions held by the user.",
    )
    def show_all_stock_positions(self)-> Annotated[str, "the output is a string of json data"]:
        stock_data = DAO.get_all_stocks()

        if stock_data is None or stock_data.empty:
            # print("You have no stock holdings.")
            return

        grouped_data = stock_data.groupby('symbol').agg({
            'quantity': 'sum',
            'buying_price': lambda x: (x * stock_data.loc[x.index, 'quantity']).sum() / stock_data.loc[x.index, 'quantity'].sum()
        })

        data = []

        for symbol, row in grouped_data.iterrows():
            entry = {
                "symbol": symbol,
                "total_quantity": row['quantity'],
                "average_price": row['buying_price']
            }
            data.append(entry)

        json_data = json.dumps(data)
        
        return json_data
