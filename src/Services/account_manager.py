import os
import pandas as pd
from datetime import datetime
from typing import Annotated
from Services import DAO
from semantic_kernel.functions import kernel_function

CASH_POSITION_FILE = os.getenv("CASH_POSITION_FILE")
STOCK_POSITION_FILE = os.getenv("STOCK_POSITION_FILE")

class AccountManager: 
    
    def __init__(self):
        pass
    
    @kernel_function(
        name="deposit_cash",
        description="Deposit a specified amount of cash into the account, updating the cash balance in the CSV file."
    )
    def deposit_cash(self, amount: float):
        """
        Deposit cash into the account and update the cash position CSV.

        Parameters:
        amount (float): The amount of money to deposit. Must be a positive value.
        
        Raises:
        ValueError: If the amount is non-positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        if not os.path.exists(CASH_POSITION_FILE):
            DAO.init_cash_position()
        try:
            df = DAO.get_remaining_cash
            current_balance = df['cash_balance'].iloc[-1]
        except (FileNotFoundError, IndexError):
            current_balance = 0
        
        new_balance = current_balance + amount
        DAO.save_cash_position(new_balance)
        
        print(f"Deposited ${amount:.2f} into the account. New balance: ${new_balance:.2f}")


    @kernel_function(
        name="withdraw_cash",
        description="Withdraw a specified amount of cash from the account, updating the cash balance in the CSV file."
    )
    def withdraw_cash(self, amount: float):
        """
        Withdraw cash from the account and update the cash position CSV.

        Parameters:
        amount (float): The amount of money to withdraw. Must be a positive value.
        
        Raises:
        ValueError: If the amount is non-positive.
        Exception: If the account has insufficient funds.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        try:
            df = pd.read_csv(CASH_POSITION_FILE)
            current_balance = df['cash_balance'].iloc[-1]
        except (FileNotFoundError, IndexError):
            raise Exception("No cash balance available.")
        
        if current_balance < amount:
            raise Exception(f"Insufficient funds to withdraw ${amount:.2f}. Current balance: ${current_balance:.2f}")
        
        new_balance = current_balance - amount
        data = {'date': [pd.Timestamp.now().strftime('%Y-%m-%d')], 'cash_balance': [new_balance]}
        df_new = pd.DataFrame(data)
        df_new.to_csv(CASH_POSITION_FILE, mode='a', header=False, index=False)
        
        print(f"Withdrew ${amount:.2f} from the account. New balance: ${new_balance:.2f}")