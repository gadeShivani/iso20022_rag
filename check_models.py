"""Script to check available Gemini models."""

import google.generativeai as genai
from google.api_core import exceptions

def main():
    """Check available Gemini models."""
    try:
        # Configure the API
        genai.configure(api_key='AIzaSyDIwcvH7cHKyanyYpJmZYqL0CyK9haLn8I')
        
        # List available models
        print("🔍 Checking available models...")
        models = list(genai.list_models())
        
        print("\n📋 Available Models:")
        print("-" * 40)
        for model in models:
            print(f"Name: {model.name}")
            print(f"Display Name: {model.display_name}")
            print(f"Description: {model.description}")
            print(f"Generation Methods: {model.supported_generation_methods}")
            print("-" * 40)
            
    except exceptions.PermissionDenied as e:
        print("\n❌ Permission Denied Error:")
        print("Make sure you have enabled the Generative Language API in your Google Cloud Console.")
        print("1. Go to https://console.cloud.google.com")
        print("2. Select or create a project")
        print("3. Search for 'Generative Language API'")
        print("4. Click Enable")
        print("\nError details:", str(e))
        
    except exceptions.NotFound as e:
        print("\n❌ Model Not Found Error:")
        print("The requested model was not found. This could mean:")
        print("1. The model name is incorrect")
        print("2. The model is not available in your region")
        print("3. Your API key doesn't have access to this model")
        print("\nError details:", str(e))
        
    except Exception as e:
        print("\n❌ Unexpected Error:")
        print(str(e))

if __name__ == "__main__":
    main() 