import os
from azure.cognitiveservices.search.newssearch import NewsSearchClient
from msrest.authentication import CognitiveServicesCredentials
from typing import Annotated
from semantic_kernel.functions import kernel_function

class BingNews:
    """
    This class pulls the latest news from bing news, based on a search query.
    https://github.com/ranaroussi/yfinance
    """
    @kernel_function(
        name="get_current_news",
        description="Get the current headlines, description, and urls to articles related to a search term. This method only takes in a search term. For example, when a customer asks 'What is the news about Microsoft?'",
    )
    def get_current_news(self, search_term) -> Annotated[list, "the output is a list"]:
        """
        Fetches news articles related to the search term using Bing News Search API.

        Args:
            search_term (str): The term to search for in news articles.

        Returns:
            list: A list of news articles related to the search term.
        """
        endpoint = os.getenv("BING_SEARCH_ENDPOINT")
        subscription_key = os.getenv("BING_SEARCH_API_KEY")

        if not subscription_key:
            raise ValueError("BING_SEARCH_API_KEY environment variable is not set")
        
        if not endpoint:
            raise ValueError("BING_SEARCH_ENDPOINT environment variable is not set")

        try:
            client = NewsSearchClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key))
            client.config.base_url = '{Endpoint}/v7.0'  # Api is broken as far back as 2020, this is a workaround
            news_result = client.news.search(query=search_term, market="en-us", count=20)
            return news_result.value
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    
