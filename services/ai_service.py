"""
ai_service.py

This module provides the main AI service class for the Chatbot AI Azure project.
It integrates with Azure OpenAI and Azure Text Analytics to analyze user-submitted text,
detecting potential scams, hoaxes, and online gambling promotions. The service supports
multi-language input and returns structured analysis results including category, explanation,
risk indicators, sentiment, and detected language.

Classes:
    - CekFaktaAIService: Main service class for text analysis.

Key Methods:
    - analyze_text(text): Analyze input text and return structured results.
    - _get_sentiment(text): Get sentiment analysis from Azure Text Analytics (with caching).
    - _get_language(text): Detect language using Azure Text Analytics (with caching).

Dependencies:
    - openai: For Azure OpenAI GPT integration.
    - azure.ai.textanalytics: For sentiment and language detection.
    - AzureConfig: Loads Azure credentials and endpoints from config.
    - functools.lru_cache: For caching repeated sentiment/language analysis.

Usage Example:
    from services.ai_service import CekFaktaAIService

    ai_service = CekFaktaAIService()
    result = ai_service.analyze_text("Your suspicious message here")
    print(result)

Returns:
    A dictionary with keys:
        - kategori: The detected category (e.g., "Potential Scam", "Hoax", etc.)
        - confidence: Confidence level (high/medium/low)
        - penjelasan: Explanation of the classification
        - indikator_bahaya: List of detected risk indicators
        - sentiment: Sentiment label (positive/neutral/negative)
        - sentiment_score: Dict with sentiment confidence scores
        - detected_language: Name of detected language
        - error: (optional) Error message if analysis fails

Notes:
    - The service uses caching for sentiment and language detection to improve performance.
    - The GPT prompt is dynamically adjusted to return results in the detected language.
    - If the GPT response is not valid JSON, a fallback response is returned.
    - All Azure credentials and endpoints are loaded from environment variables via AzureConfig.

"""

import json
import openai
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from config.azure_config import AzureConfig
from typing import Dict, Union, List
from functools import lru_cache

class CekFaktaAIService:
    """
    Main AI service for analyzing suspicious text using Azure OpenAI and Text Analytics.

    Methods:
        - analyze_text(text): Analyze text and return structured results.
    """

    def __init__(self):
        """
        Initialize Azure OpenAI and Text Analytics clients using configuration from AzureConfig.
        """
        # Setup Azure OpenAI
        openai.api_type = "azure"
        openai.api_base = AzureConfig.AZURE_OPENAI_ENDPOINT
        openai.api_version = AzureConfig.AZURE_OPENAI_API_VERSION
        openai.api_key = AzureConfig.AZURE_OPENAI_API_KEY
        
        # Setup Text Analytics
        self.text_analytics_client = TextAnalyticsClient(
            endpoint=AzureConfig.AZURE_AI_ENDPOINT,
            credential=AzureKeyCredential(AzureConfig.AZURE_AI_API_KEY)
        )
    
    @staticmethod
    @lru_cache(maxsize=100)
    def _cached_analyze_sentiment(endpoint, key, text):
        """
        Cached static method to analyze sentiment using Azure Text Analytics.
        """
        client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        return client.analyze_sentiment([text])[0]

    @staticmethod
    @lru_cache(maxsize=100)
    def _cached_detect_language(endpoint, key, text):
        """
        Cached static method to detect language using Azure Text Analytics.
        """
        client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        return client.detect_language([text])[0]

    def _get_sentiment(self, text):
        """
        Get sentiment analysis for the given text (with caching).
        """
        return self._cached_analyze_sentiment(
            AzureConfig.AZURE_AI_ENDPOINT,
            AzureConfig.AZURE_AI_API_KEY,
            text
        )

    def _get_language(self, text):
        """
        Detect language for the given text (with caching).
        """
        return self._cached_detect_language(
            AzureConfig.AZURE_AI_ENDPOINT,
            AzureConfig.AZURE_AI_API_KEY,
            text
        )

    def analyze_text(self, text: str) -> Dict[str, Union[str, float, List]]:
        """
        Analyze the input text for potential scam, hoax, online gambling promotion, or safe content.
        The GPT output will be returned in the detected input language (based on Azure AI detection).
        If GPT does not respond with valid JSON, a safe fallback is returned.
        The system also re-verifies if Azure language detection is incorrect.

        Args:
            text (str): User input text (max 1000 characters)

        Returns:
            dict: Analysis result including category, explanation, indicators, sentiment, and language
        """
        print("📥 Input received:", repr(text))

        if not text or len(text.strip()) == 0:
            return {"error": "Text must not be empty"}

        if len(text) > 1000:
            return {"error": "Text is too long (max 1000 characters)"}

        try:
            # Detect language and sentiment
            sentiment_result = self._get_sentiment(text)
            language_result = self._get_language(text)

            # Get language code and name from Azure
            lang_code = language_result.primary_language.iso6391_name.lower()  # e.g., 'id'
            language_name = language_result.primary_language.name              # e.g., 'English'

            # Fallback: fix detection errors for Indonesian
            if lang_code == "en" and any(k in text.lower() for k in ["anda", "hadiah", "rekening", "jutaan"]):
                lang_code = "id"
                language_name = "Indonesian"

            # Map language code to standard name (for GPT)
            language_name = {
                "id": "Indonesian",
                "en": "English",
                "fr": "French",
                "es": "Spanish",
                "de": "German",
                "zh": "Chinese",
                "ar": "Arabic",
                "ru": "Russian",
                "ja": "Japanese",
                "ko": "Korean",
            }.get(lang_code, language_name)  # fallback to Azure name if unknown

            # Dynamic multilingual prompt
            system_prompt = f"""
            You are an AI expert in detecting scam, fraud, hoaxes, and online gambling. Analyze the following text and classify it into one of the categories below:

            1. "Potential Scam" – if the message offers a prize, an easy job, or asks for personal data.
            2. "Online Gambling Promotion" – if the message promotes online gambling or mentions “slot gacor”.
            3. "Hoax" – if the message contains misleading or false information.
            4. "Safe" – if the message is safe and not harmful.

            Return your response in this JSON format:
            {{
            "kategori": "category_result",
            "confidence": "high/medium/low",  // Always use English: high/medium/low
            "penjelasan": "short explanation in the detected language",
            "indikator_bahaya": ["list of detected risk indicators"]
            }}

            ⚠️ Important: Your answer MUST be in language: **{language_name}**, and always in the JSON format above. Do not add any explanation outside the JSON.


            Now analyze the following text:
            """

            # Send to Azure OpenAI GPT
            response = openai.ChatCompletion.create(
                engine=AzureConfig.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=500
            )

            # Print raw GPT result for debugging
            gpt_raw = response.choices[0].message.content.strip()
            print("📤 GPT raw response:", repr(gpt_raw))

            # Fallback if GPT returns empty
            if not gpt_raw:
                return {
                    "error": "Model did not respond or returned empty result.",
                    "kategori": "Unknown",
                    "confidence": "low",
                    "penjelasan": "Model did not return any response for this input.",
                    "indikator_bahaya": [],
                    "sentiment": sentiment_result.sentiment,
                    "sentiment_score": {
                        "positive": round(sentiment_result.confidence_scores.positive, 2),
                        "neutral": round(sentiment_result.confidence_scores.neutral, 2),
                        "negative": round(sentiment_result.confidence_scores.negative, 2)
                    },
                    "detected_language": language_name
                }

            # Fallback if GPT does not return valid JSON
            try:
                gpt_result = json.loads(gpt_raw)
            except json.JSONDecodeError:
                return {
                    "error": "Model did not respond in valid JSON format.",
                    "kategori": "Unknown",
                    "confidence": "low",
                    "penjelasan": gpt_raw,
                    "indikator_bahaya": [],
                    "sentiment": sentiment_result.sentiment,
                    "sentiment_score": {
                        "positive": round(sentiment_result.confidence_scores.positive, 2),
                        "neutral": round(sentiment_result.confidence_scores.neutral, 2),
                        "negative": round(sentiment_result.confidence_scores.negative, 2)
                    },
                    "detected_language": language_name
                }

            # Return final response
            return {
                "kategori": gpt_result.get("kategori", "Unknown"),
                "confidence": gpt_result.get("confidence", "medium"),
                "penjelasan": gpt_result.get("penjelasan", ""),
                "indikator_bahaya": gpt_result.get("indikator_bahaya", []),
                "sentiment": sentiment_result.sentiment,
                "sentiment_score": {
                    "positive": round(sentiment_result.confidence_scores.positive, 2),
                    "neutral": round(sentiment_result.confidence_scores.neutral, 2),
                    "negative": round(sentiment_result.confidence_scores.negative, 2)
                },
                "detected_language": language_name
            }

        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}",
                "kategori": "Error",
                "penjelasan": "Unable to analyze text",
                "indikator_bahaya": []
            }


