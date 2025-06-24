"""
azure_config.py

This module loads and manages Azure-related configuration for the Chatbot AI Azure project.
It uses environment variables (from a .env file or system environment) to securely store
credentials and endpoints for Azure OpenAI and Azure Text Analytics services.

Usage:
    from config.azure_config import AzureConfig

    # Access configuration values:
    endpoint = AzureConfig.AZURE_OPENAI_ENDPOINT
    api_key = AzureConfig.AZURE_OPENAI_API_KEY

Environment Variables Required:
    - AZURE_OPENAI_ENDPOINT:      Endpoint URL for Azure OpenAI service
    - AZURE_OPENAI_API_KEY:       API key for Azure OpenAI service
    - AZURE_OPENAI_DEPLOYMENT_NAME: Deployment name for Azure OpenAI model
    - AZURE_OPENAI_API_VERSION:   (Optional) API version for Azure OpenAI (default: 2023-05-15)
    - AZURE_AI_ENDPOINT:          Endpoint URL for Azure Text Analytics service
    - AZURE_AI_API_KEY:           API key for Azure Text Analytics service
    - SECRET_KEY:                 Secret key for Flask session security

How it works:
    - Loads environment variables using python-dotenv (from a .env file if present).
    - Provides a class AzureConfig with class attributes for each configuration value.
    - Logs and raises an error if any required variable is missing.

Example .env file:
    AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
    AZURE_OPENAI_API_KEY=your-openai-api-key
    AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
    AZURE_OPENAI_API_VERSION=2023-05-15
    AZURE_AI_ENDPOINT=https://your-cognitive-resource.cognitiveservices.azure.com/
    AZURE_AI_API_KEY=your-text-analytics-api-key
    SECRET_KEY=your-flask-secret-key

"""

import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file if present
load_dotenv()

class AzureConfig:
    """
    AzureConfig loads Azure service credentials and endpoints from environment variables.
    All attributes are class-level and can be accessed as AzureConfig.ATTRIBUTE_NAME.
    """
    try:
        # Azure OpenAI configuration
        AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
        AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
        AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
        AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2023-05-15')

        # Azure Text Analytics configuration
        AZURE_AI_ENDPOINT = os.getenv('AZURE_AI_ENDPOINT')
        AZURE_AI_API_KEY = os.getenv('AZURE_AI_API_KEY')

        # Flask secret key
        SECRET_KEY = os.getenv('SECRET_KEY')

        # Optionally, you can add validation here to ensure all variables are set
        # Example:
        # assert AZURE_OPENAI_ENDPOINT, "AZURE_OPENAI_ENDPOINT is not set"
        # assert AZURE_OPENAI_API_KEY, "AZURE_OPENAI_API_KEY is not set"
        # ... (repeat for other variables as needed)

    except Exception as e:
        logging.error(f"Missing environment variable: {str(e)}")
        raise