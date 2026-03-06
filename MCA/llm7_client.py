"""
LLM7.io API Client
Handles communication with LLM7.io API for agent workers
"""

import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class LLM7Client:
    """Client for interacting with LLM7.io API"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: str = "gpt-3.5-turbo"
    ):
        """
        Initialize LLM7 client
        
        Args:
            api_key: API key for LLM7.io (defaults to LLM7_API_KEY env var)
            base_url: Base URL for API (defaults to LLM7_BASE_URL env var)
            default_model: Default model to use (default: gpt-3.5-turbo)
        """
        self.api_key = api_key or os.getenv("LLM7_API_KEY")
        self.base_url = base_url or os.getenv(
            "LLM7_BASE_URL", 
            "https://api.llm7.io/v1"
        )
        self.default_model = os.getenv("DEFAULT_MODEL", default_model)
        
        if not self.api_key:
            raise ValueError(
                "LLM7_API_KEY not found. Set it in .env file or pass as parameter."
            )
    
    def chat_completion(
        self,
        messages: list[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a chat completion request to LLM7.io
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to default_model)
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API
            
        Returns:
            API response dictionary
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Try to get error details from response
            error_details = ""
            try:
                error_data = response.json()
                error_details = f" - {error_data.get('error', {}).get('message', str(error_data))}"
            except:
                pass
            raise Exception(f"LLM7 API request failed: {str(e)}{error_details}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"LLM7 API request failed: {str(e)}")
    
    def get_completion_text(self, response: Dict[str, Any]) -> str:
        """
        Extract text from completion response
        
        Args:
            response: API response dictionary
            
        Returns:
            Generated text content
        """
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to extract completion text: {str(e)}")
