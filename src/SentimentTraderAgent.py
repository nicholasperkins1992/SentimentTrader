from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI  
import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
)

from Services.stock import Stock

class AzureOpenAIClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.credential = DefaultAzureCredential()
        self.token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
        
        # Initialize the kernel
        self.kernel = Kernel()

        # Add Azure OpenAI chat completion
        
        self.chat_completion = AzureChatCompletion(
            deployment_name="ip-gpt-4o",
            ad_token_provider=self.token_provider,
            base_url=endpoint,
        )
        
        self.kernel.add_service(self.chat_completion)
        
        self.kernel.add_plugin(
            Stock(),
            plugin_name="Stock",
        )
        
        # Enable planning
        self.execution_settings = OpenAIChatPromptExecutionSettings(
            service_id="chat",
            max_tokens=2000,
            temperature=0.7,
            top_p=0.8,
            function_choice_behavior="auto",
        )
    

        # Create a history of the conversation
        self.history = ChatHistory()
    
        
        # self.client = AzureOpenAI(
        #     api_version="2024-08-01-preview",
        #     azure_endpoint=self.endpoint, #https://ai-daschollai303201498064.openai.azure.com
        #     azure_ad_token_provider=self.token_provider
        # )
        
    #     self.tools = [
    #     {
    #         "type": "function",
    #         "function": {
    #             "name": "get_stock_price",
    #             "description": "Get the current stock price of a company in USD, this method only takes in a ticker name. for example when a customer asks 'Where is the price of Microsoft'",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "ticker": {
    #                         "type": "string",
    #                         "description": "The ticker symbol of the company."
    #                     }
    #                 },
    #                 "required": ["ticker"],
    #                 "additionalProperties": False
    #             }
    #         }
    #     }
    # ]
        
    def call_openai(self, message: str):
        """
        Get the response from the AI.

        Parameters:
        message (str): The message to send to the AI.

        Returns:
        str: The response from the AI.
        """
        self.history.add_user_message(message)

        async def get_response():
            return await self.chat_completion.get_chat_message_content(
                chat_history=self.history,
                settings=self.execution_settings,
                kernel=self.kernel,
            )

        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            result = loop.run_until_complete(get_response())
        except RuntimeError as e:
            if str(e).startswith('There is no current event loop in thread'):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(get_response())
            else:
                raise

        # self.history.add_user_message(result)
        return str(result)