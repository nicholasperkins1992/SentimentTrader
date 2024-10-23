from dotenv import load_dotenv
from SentimentTraderAgent import AzureOpenAIClient
from Services.bing_news import search_bing_news

load_dotenv()

azure_client = AzureOpenAIClient(endpoint="https://ai-daschollai303201498064.openai.azure.com/openai/")

while True:
        # Take input from the user
        user_input = input("Enter your message (type 'EXIT' to quit): ")
        
        # Check if the user wants to exit
        if user_input.upper() == "EXIT":
            print("Exiting the program.")
            break
        
        # Call the call_openai method with the user input
        response = azure_client.call_openai(user_input)
        
        # Print the response
        print(response)