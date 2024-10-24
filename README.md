# SentimentTrader
ChatGPT-StockAnalyzer leverages ChatGPT for sentiment analysis to generate informed buy and sell signals for stock trading based on current market trends.

## How to Run
To run the project, follow these steps:

### Prerequisites
- Ensure you have Docker installed on your machine.
- An Azure Open AI service Deployed
- Bing Search v7 Service Deployed 

### Running in a Dev Container
1. Open the project in a development environment that supports dev containers, such as Visual Studio Code.
2. When prompted, reopen the project in a container(Ctrl + Shift + P -> Dev Container: Rebuild and Reopen in Container).
3. The container will build and start automatically, the container will automatically install all reuired python packages

### Setting Up Environment Variables
1. Create a `.env` file in the root directory of the project based off .env samples.
2. Fill out the `.env` file with the necessary environment variables. For example:
    ```plaintext
    BING_SEARCH_API_KEY=Your_Api_Key
    AzureAi_Deployment_Name=Your_deployment_name
    ZUREAI_ENDPOINT=Your_AzureAi_Endpoint
    ```

### Starting the Application
1. Once the container is running and the `.env` file is set up, you can start the application by running:
    ```bash
    python main.py
    ```
2. The application should now be running, to perform automatic stock trading ask the bot 'Perform automated trading.'
