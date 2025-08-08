"""Run model comparison tests."""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.test_queries import run_model_comparison
from config import validate_api_keys, OPENAI_API_KEY, GEMINI_API_KEY

def main():
    """Main entry point for running tests."""
    print("🚀 Starting ISO 20022 RAG Model Comparison")
    print("=" * 80)

    # Validate API keys
    validate_api_keys()

    print("\n📊 Running model comparison tests...")
    
    try:
        # Run tests with both models
        results = run_model_comparison(
            openai_key=OPENAI_API_KEY,
            gemini_key=GEMINI_API_KEY
        )
        
        print("\n✅ Tests completed successfully!")
        
        # Print summary
        print("\nSummary:")
        print("-" * 40)
        print(f"Total messages tested: {results['total_messages']}")
        print(f"Total queries tested: {results['total_queries']}")
        
        print(f"\nBest performing method: {results.get('best_method', 'No valid responses')}")
        print(f"Average ROUGE-1 score: {results.get('avg_rouge1', 0.000):.3f}")
        print(f"Average readability: {results.get('avg_readability', 0.000):.3f}")
        
        print("\nMethod Performance:")
        print("-" * 40)
        print("\ngpt:")
        for metric, value in results.get('gpt_metrics', {}).items():
            print(f"  {metric}: {value:.3f}")
        
        print("\ngemini:")
        for metric, value in results.get('gemini_metrics', {}).items():
            print(f"  {metric}: {value:.3f}")
            
    except Exception as e:
        print(f"\n❌ Error running tests: {str(e)}")
        print("\nPlease check:")
        print("1. API keys are correctly set")
        print("2. Generative Language API is enabled in Google Cloud Console")
        print("3. You have waited a few minutes after enabling the API")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 