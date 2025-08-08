"""Test script to verify API connections for both GPT and Gemini."""

import os
from openai import OpenAI
import google.generativeai as genai
from config import OPENAI_API_KEY, GEMINI_API_KEY, GEMINI_MODEL

def test_openai_connection():
    """Test OpenAI API connection."""
    print("\n🔄 Testing OpenAI API connection...")
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello, can you hear me?"}],
            temperature=0.3
        )
        print("✅ OpenAI API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {str(e)}")
        return False

def test_gemini_connection():
    """Test Gemini API connection."""
    print("\n🔄 Testing Gemini API connection...")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content("Hello, can you hear me?")
        print("✅ Gemini API connection successful!")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Gemini API connection failed: {str(e)}")
        return False

def main():
    """Run API connection tests."""
    print("🚀 Starting API Connection Tests")
    print("=" * 80)
    
    openai_success = test_openai_connection()
    gemini_success = test_gemini_connection()
    
    print("\n📊 Summary:")
    print("-" * 40)
    print(f"OpenAI API: {'✅ Connected' if openai_success else '❌ Failed'}")
    print(f"Gemini API: {'✅ Connected' if gemini_success else '❌ Failed'}")
    
    if not openai_success or not gemini_success:
        print("\n⚠️  Please check your API keys and make sure the APIs are enabled.")
        return 1
    return 0

if __name__ == "__main__":
    exit(main()) 