"""Setup NLTK data and handle SSL certificate issues."""

import nltk
import ssl
import os

def setup_nltk():
    """Set up NLTK with proper SSL handling and data directory creation."""
    try:
        # Handle SSL certificate verification
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        # Create NLTK data directory if it doesn't exist
        nltk_data_dir = os.path.expanduser('~/nltk_data')
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir)
            print(f"✅ Created NLTK data directory at {nltk_data_dir}")

        # Try to find the punkt tokenizer
        try:
            nltk.data.find('tokenizers/punkt')
            print("✅ NLTK punkt tokenizer already downloaded")
        except LookupError:
            print("📥 Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=False)
            print("✅ NLTK punkt tokenizer downloaded successfully")

        # Verify the download
        try:
            nltk.data.find('tokenizers/punkt')
            return True
        except LookupError:
            print("❌ Failed to verify punkt tokenizer download")
            return False

    except Exception as e:
        print(f"❌ Error setting up NLTK: {str(e)}")
        return False

if __name__ == "__main__":
    setup_nltk() 