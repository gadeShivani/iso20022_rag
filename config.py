"""Configuration settings for the ISO20022 RAG system.

To enable the Gemini API:
1. Go to https://makersuite.google.com/app/apikey
2. If you haven't already:
   - Sign in with your Google account
   - Accept the terms of service
   - Enable the Generative Language API
3. Create a new API key
4. Set the GEMINI_API_KEY environment variable:
   export GEMINI_API_KEY='your-api-key'
   
Or update the DEFAULT_GEMINI_KEY below with your API key.

Note: If you get a '403 Generative Language API has not been used in project' error:
1. Go to https://console.cloud.google.com
2. Create a new project or select an existing one
3. Search for 'Generative Language API' and enable it
4. Wait a few minutes for the API to be fully enabled
5. Try running the tests again
"""

import os

# Default API keys (override with environment variables)
DEFAULT_OPENAI_KEY = "your-openai-key-here"
DEFAULT_GEMINI_KEY = "your-gemini-key-here"

# Get API keys from environment variables or use defaults
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", DEFAULT_OPENAI_KEY)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", DEFAULT_GEMINI_KEY)

# Model settings
GPT_MODEL = "gpt-4"
GEMINI_MODEL = "gemini-1.5-pro"  # Updated to use stable 1.5 Pro model without models/ prefix

# Temperature settings (lower = more focused, higher = more creative)
DEFAULT_TEMPERATURE = 0.3
GPT_TEMPERATURE = DEFAULT_TEMPERATURE
GEMINI_TEMPERATURE = DEFAULT_TEMPERATURE

# Logging settings
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"

def validate_api_keys():
    """Validate that API keys are properly set."""
    warnings = []
    
    if OPENAI_API_KEY == DEFAULT_OPENAI_KEY:
        warnings.append("⚠️  Using default OpenAI API key. Set OPENAI_API_KEY environment variable for production use.")
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your-gemini-key-here":
        warnings.append("""
❌ Gemini API key not set. To enable Gemini:
1. Go to https://makersuite.google.com/app/apikey
2. If you haven't already:
   - Sign in with your Google account
   - Accept the terms of service
   - Enable the Generative Language API
3. Create a new API key
4. Set the GEMINI_API_KEY environment variable:
   export GEMINI_API_KEY='your-api-key'
   
Or update DEFAULT_GEMINI_KEY in config.py

Note: If you get a '403 Generative Language API has not been used in project' error:
1. Go to https://console.cloud.google.com
2. Create a new project or select an existing one
3. Search for 'Generative Language API' and enable it
4. Wait a few minutes for the API to be fully enabled
5. Try running the tests again
""")
    
    for warning in warnings:
        print(warning)
    
    return len(warnings) == 0 