import yfinance as yf
from typing import Annotated
from semantic_kernel.functions import kernel_function

class Stock:
    """
    This class uses a scraper around Yahoo Finance to get the current price of a stock.
    This was chosen since there is no license needed, however, rate limiting may be an issue.
    https://github.com/ranaroussi/yfinance
    """

    @kernel_function(
        name="get_stock_price",
        description="Get the current stock price of a company in USD. This method only takes in a ticker name. For example, when a customer asks 'What is the price of Microsoft?'",
    )
    def get_stock_price(self, ticker: str) -> Annotated[str, "the output is a string"]:
        """
        Get the current stock price for a given ticker symbol.

        Parameters:
        ticker (str): The ticker symbol of the stock.

        Returns:
        str: The current stock price as a string.
        """
        company = yf.Ticker(ticker)
        info = company.info
        return str(info.get('currentPrice'))