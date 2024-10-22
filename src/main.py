from dotenv import load_dotenv
from Services.bing_news import search_bing_news

load_dotenv()
print(search_bing_news('Microsoft'))
