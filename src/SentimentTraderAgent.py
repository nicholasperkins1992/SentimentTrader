from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
)
from Services.stock import Stock
from Services.trader import Trader
from Services.bing_news import BingNews
from Services.account_manager import AccountManager
from Prompts import Recomend_Stonks

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
        
        # Add the plugins
        self.kernel.add_plugin(
            Stock(),
            plugin_name="Stock",
        )
        
        self.kernel.add_plugin(
            BingNews(),
            plugin_name="BingNews",
        )

        self.kernel.add_plugin(
            Trader(),
            plugin_name="Trader",
        )

        self.kernel.add_plugin(
            AccountManager(),
            plugin_name="AccountManager",
        )
        
        # Kernel settings
        self.execution_settings = OpenAIChatPromptExecutionSettings(
            service_id="chat",
            max_tokens=4096,
            temperature=0.7,
            top_p=0.8,
            function_choice_behavior="auto",
        )
    

        # Create a history of the conversation
        self.history = ChatHistory()
        #Add the prompt to the history
        self.history.add_system_message(Recomend_Stonks)
        
    def Execute_Agent(self, message: str):
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

        self.history.add_message(result)
        return str(result)