from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI  

class AzureOpenAIClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.credential = DefaultAzureCredential()
        self.token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
        
        self.client = AzureOpenAI(
            api_version="2024-08-01-preview",
            azure_endpoint=self.endpoint, #https://ai-daschollai303201498064.openai.azure.com
            azure_ad_token_provider=self.token_provider
        )
        
    def call_openai(self, message: str):
        response = self.client.chat.completions.create(
        model="ip-gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": message
            }
        ]
        )
        return response.choices[0].message.content