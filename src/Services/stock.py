import yfinance as yf
import requests
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
    
    # @kernel_function(
    #     name="get_text_from_url",
    #     description="Get the text content from a URL. This method only takes in a URL. For example, when a customer asks 'What is the content of this URL?'",
    # )
    # def get_text_from_url(self, url):
    #     """
    #     Fetches and returns the text content from the specified URL.

    #     Args:
    #         url (str): The URL from which to fetch the text content.

    #     Returns:
    #         str: The text content retrieved from the URL if the request is successful.
    #             If an error occurs, returns a string describing the error.
    #     """
    #     try:
    #         headers = {
    #             'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/W.X.Y.Z Safari/537.36'
    #         }
    #         response = requests.get(url, headers=headers)
    #         response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    #         return response.text
    #     except requests.exceptions.RequestException as e:
    #         return f"An error occurred: {e}"