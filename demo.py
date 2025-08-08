"""Demo script for ISO 20022 RAG system."""

import os
from src.rag_implementations import ISO20022RAG
from src.evaluation import ISO20022Evaluator
from data.sample_messages import (
    SAMPLE_PACS008, SAMPLE_INTERNATIONAL, SAMPLE_HIGH_VALUE,
    EXPECTED_SUMMARIES, VALIDATION_DATA
)
from config import OPENAI_API_KEY, GEMINI_API_KEY

def main():
    """Run a demo of the ISO 20022 RAG system."""
    # Initialize RAG system
    print("🚀 Initializing ISO 20022 RAG System...")
    rag = ISO20022RAG(openai_key=OPENAI_API_KEY, gemini_key=GEMINI_API_KEY)
    evaluator = ISO20022Evaluator()
    
    # Test with different message types
    messages = {
        "Basic Payment": SAMPLE_PACS008,
        "International Transfer": SAMPLE_INTERNATIONAL,
        "High-Value Payment": SAMPLE_HIGH_VALUE
    }
    
    for name, message in messages.items():
        print(f"\n📝 Testing {name}")
        print("=" * 80)
        
        # Parse message
        print("\nParsing message...")
        message_data = rag.parse_iso_message(message)
        print("✅ Message parsed successfully")
        
        # Generate summaries using different RAG methods
        print("\nGenerating summaries...")
        
        # Simple RAG
        print("\n🔍 Simple RAG:")
        simple_summary = rag.simple_rag_summary(message_data, model_name="gpt-4")
        print(simple_summary)
        
        # Context-Enriched RAG
        print("\n🔍 Context-Enriched RAG:")
        context_summary = rag.context_enriched_rag_summary(message_data, model_name="gpt-4")
        print(context_summary)
        
        # Reranker RAG
        print("\n🔍 Reranker RAG:")
        reranker_summary = rag.reranker_rag_summary(message_data, model_name="gpt-4")
        print(reranker_summary)
        
        # Evaluate summaries
        print("\n📊 Evaluating summaries...")
        validation = evaluator.evaluate_all(
            [simple_summary, context_summary, reranker_summary],
            reference_summary=EXPECTED_SUMMARIES.get(name.lower().replace(" ", "_")),
            message_type=message_data['message_type']
        )
        
        # Print evaluation results
        print("\nEvaluation Results:")
        for i, method in enumerate(["Simple RAG", "Context-Enriched RAG", "Reranker RAG"]):
            result = validation["validations"][i]
            print(f"\n{method}:")
            print(f"Score: {result['validation']['overall_score']:.2f} ({result['validation']['status']})")
            print("Checks:", ", ".join(f"{k}: {v}" for k, v in result['validation']['checks'].items()))

if __name__ == "__main__":
    main() 