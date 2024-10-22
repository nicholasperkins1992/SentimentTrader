import os
from azure.cognitiveservices.search.newssearch import NewsSearchClient
from msrest.authentication import CognitiveServicesCredentials

def search_bing_news(search_term):
    endpoint = "https://api.bing.microsoft.com"
    subscription_key = os.getenv("BING_SEARCH_API_KEY")

    client = NewsSearchClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key))
    client.config.base_url = '{Endpoint}/v7.0' # Api is broken as far back as 2020, this is a workaround
    news_result = client.news.search(query=search_term, market="en-us", count=10)
    # Hoping GPT can open websites, if not we may need to download the HTML and send that to GPT
    return news_result.value
    
