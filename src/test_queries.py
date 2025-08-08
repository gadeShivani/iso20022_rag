"""Test script to compare GPT and Gemini performance on ISO 20022 message processing."""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.rag_implementations import ISO20022RAG
from src.evaluation import ISO20022Evaluator
from data.message_generator import generate_test_messages

# Generate test messages
TEST_MESSAGES = generate_test_messages(50)

# Comprehensive test scenarios
TEST_SCENARIOS = [
    # Basic Message Understanding
    {
        "category": "Basic Understanding",
        "queries": [
            {
                "name": "Message Type",
                "query": "What type of ISO 20022 message is this and what is its purpose?",
                "description": "Tests basic message identification"
            },
            {
                "name": "Key Fields",
                "query": "What are the key fields in this message and their values?",
                "description": "Tests field extraction"
            },
            {
                "name": "Transaction Summary",
                "query": "Provide a concise summary of this transaction.",
                "description": "Tests summarization ability"
            }
        ]
    },
    
    # Payment Processing
    {
        "category": "Payment Processing",
        "queries": [
            {
                "name": "Payment Flow",
                "query": "Explain the payment flow, including all parties involved.",
                "description": "Tests understanding of payment chain"
            },
            {
                "name": "Settlement Details",
                "query": "What are the settlement details and method used?",
                "description": "Tests settlement understanding"
            },
            {
                "name": "Charges",
                "query": "How are the charges handled in this payment?",
                "description": "Tests charge bearer understanding"
            }
        ]
    },
    
    # Compliance and Regulatory
    {
        "category": "Compliance",
        "queries": [
            {
                "name": "Regulatory Requirements",
                "query": "What regulatory requirements apply to this message?",
                "description": "Tests regulatory knowledge"
            },
            {
                "name": "Sanctions Screening",
                "query": "What sanctions screening considerations apply?",
                "description": "Tests compliance understanding"
            },
            {
                "name": "Reporting Requirements",
                "query": "What reporting requirements apply to this transaction?",
                "description": "Tests reporting knowledge"
            }
        ]
    },
    
    # Cross-Border Aspects
    {
        "category": "Cross-Border",
        "queries": [
            {
                "name": "Currency Exchange",
                "query": "Analyze the currency exchange aspects of this transaction.",
                "description": "Tests FX understanding"
            },
            {
                "name": "International Routing",
                "query": "How is this payment routed internationally?",
                "description": "Tests routing knowledge"
            },
            {
                "name": "Country Requirements",
                "query": "What country-specific requirements apply?",
                "description": "Tests geographic understanding"
            }
        ]
    },
    
    # Technical Analysis
    {
        "category": "Technical",
        "queries": [
            {
                "name": "Message Structure",
                "query": "Analyze the XML structure and namespace usage.",
                "description": "Tests technical understanding"
            },
            {
                "name": "Validation Rules",
                "query": "What validation rules apply to this message?",
                "description": "Tests schema knowledge"
            },
            {
                "name": "Message References",
                "query": "Explain the message reference system used.",
                "description": "Tests reference understanding"
            }
        ]
    },
    
    # Business Analysis
    {
        "category": "Business",
        "queries": [
            {
                "name": "Business Purpose",
                "query": "What is the business purpose of this transaction?",
                "description": "Tests business context understanding"
            },
            {
                "name": "Risk Assessment",
                "query": "Assess the business risks in this transaction.",
                "description": "Tests risk analysis"
            },
            {
                "name": "Process Optimization",
                "query": "Suggest optimizations for this payment process.",
                "description": "Tests process understanding"
            }
        ]
    },
    
    # Error Handling
    {
        "category": "Error Handling",
        "queries": [
            {
                "name": "Error Scenarios",
                "query": "What potential errors could occur with this message?",
                "description": "Tests error awareness"
            },
            {
                "name": "Resolution Process",
                "query": "How should errors in this message be resolved?",
                "description": "Tests problem-solving"
            },
            {
                "name": "Status Updates",
                "query": "How are status updates handled for this message?",
                "description": "Tests status handling"
            }
        ]
    },
    
    # Reconciliation
    {
        "category": "Reconciliation",
        "queries": [
            {
                "name": "Matching Rules",
                "query": "What matching rules apply for reconciliation?",
                "description": "Tests reconciliation understanding"
            },
            {
                "name": "Statement Analysis",
                "query": "Analyze the statement entries and balances.",
                "description": "Tests statement understanding"
            },
            {
                "name": "Exception Handling",
                "query": "How are reconciliation exceptions handled?",
                "description": "Tests exception handling"
            }
        ]
    },
    
    # Special Cases
    {
        "category": "Special Cases",
        "queries": [
            {
                "name": "High-Value Payment",
                "query": "What special considerations apply to high-value payments?",
                "description": "Tests high-value handling"
            },
            {
                "name": "Urgent Processing",
                "query": "How are urgent payments handled differently?",
                "description": "Tests priority handling"
            },
            {
                "name": "Return Processing",
                "query": "How are payment returns processed?",
                "description": "Tests return handling"
            }
        ]
    }
]

def run_model_comparison(openai_key: str = None, gemini_key: str = None):
    """Run comparison tests between GPT and Gemini."""
    # Initialize RAG system
    rag = ISO20022RAG(openai_key=openai_key, gemini_key=gemini_key)
    
    # Generate test messages
    messages = TEST_MESSAGES
    
    results = {
        "gpt": {
            "simple": {},
            "context": {},
            "reranker": {}
        },
        "gemini": {
            "simple": {},
            "context": {},
            "reranker": {}
        },
        "total_messages": len(messages),
        "total_queries": sum(len(s["queries"]) for s in TEST_SCENARIOS),
        "best_method": None,
        "avg_rouge1": 0.0,
        "avg_readability": 0.0
    }
    
    for msg_type, msg_list in messages.items():
        print(f"\n🔄 Testing {msg_type} Messages\n")
        print("=" * 80)
        
        # Test first message of each type
        message = msg_list[0]
        message_data = rag.parse_iso_message(message)
        
        # Find relevant scenarios for message type
        relevant_scenarios = get_relevant_scenarios(msg_type)
        
        for scenario in relevant_scenarios:
            print(f"\n📝 Category: {scenario['category']}")
            
            for test in scenario['queries']:
                print(f"\nTest: {test['name']}")
                print(f"Query: {test['query']}")
                print(f"Description: {test['description']}")
                print("\nResponses:")
                
                # Test each RAG method with GPT
                try:
                    # Simple RAG
                    gpt_simple = rag.simple_rag_summary(
                        message_data,
                        model_name="gpt-4",
                        query=test['query']
                    )
                    results["gpt"]["simple"][f"{msg_type}_{test['name']}"] = gpt_simple
                    print("\nGPT - Simple RAG:")
                    print("-" * 40)
                    print(gpt_simple)
                    
                    # Context-Enriched RAG
                    gpt_context = rag.context_enriched_rag_summary(
                        message_data,
                        model_name="gpt-4",
                        query=test['query']
                    )
                    results["gpt"]["context"][f"{msg_type}_{test['name']}"] = gpt_context
                    print("\nGPT - Context-Enriched RAG:")
                    print("-" * 40)
                    print(gpt_context)
                    
                    # Reranker RAG
                    gpt_reranker = rag.reranker_rag_summary(
                        message_data,
                        model_name="gpt-4",
                        query=test['query']
                    )
                    results["gpt"]["reranker"][f"{msg_type}_{test['name']}"] = gpt_reranker
                    print("\nGPT - Reranker RAG:")
                    print("-" * 40)
                    print(gpt_reranker)
                except Exception as e:
                    print(f"GPT Error: {str(e)}")
                    results["gpt"]["simple"][f"{msg_type}_{test['name']}"] = f"Error: {str(e)}"
                    results["gpt"]["context"][f"{msg_type}_{test['name']}"] = f"Error: {str(e)}"
                    results["gpt"]["reranker"][f"{msg_type}_{test['name']}"] = f"Error: {str(e)}"
                
                # Test each RAG method with Gemini
                try:
                    # Simple RAG
                    gemini_simple = rag.simple_rag_summary(
                        message_data,
                        model_name="gemini-1.5-pro",
                        query=test['query']
                    )
                    results["gemini"]["simple"][f"{msg_type}_{test['name']}"] = gemini_simple
                    print("\nGemini - Simple RAG:")
                    print("-" * 40)
                    print(gemini_simple)
                    
                    # Context-Enriched RAG
                    gemini_context = rag.context_enriched_rag_summary(
                        message_data,
                        model_name="gemini-1.5-pro",
                        query=test['query']
                    )
                    results["gemini"]["context"][f"{msg_type}_{test['name']}"] = gemini_context
                    print("\nGemini - Context-Enriched RAG:")
                    print("-" * 40)
                    print(gemini_context)
                    
                    # Reranker RAG
                    gemini_reranker = rag.reranker_rag_summary(
                        message_data,
                        model_name="gemini-1.5-pro",
                        query=test['query']
                    )
                    results["gemini"]["reranker"][f"{msg_type}_{test['name']}"] = gemini_reranker
                    print("\nGemini - Reranker RAG:")
                    print("-" * 40)
                    print(gemini_reranker)
                except Exception as e:
                    print(f"Gemini Error: {str(e)}")
                    results["gemini"]["simple"][f"{msg_type}_{test['name']}"] = f"Error: {str(e)}"
                    results["gemini"]["context"][f"{msg_type}_{test['name']}"] = f"Error: {str(e)}"
                    results["gemini"]["reranker"][f"{msg_type}_{test['name']}"] = f"Error: {str(e)}"
                
                print("\n" + "=" * 80)
    
    # Calculate best method and averages
    evaluator = ISO20022Evaluator()
    all_responses = []
    method_scores = {"gpt": {}, "gemini": {}}
    
    for model in ["gpt", "gemini"]:
        for method in ["simple", "context", "reranker"]:
            responses = [r for r in results[model][method].values() if not r.startswith("Error")]
            if responses:
                validation_scores = [evaluator.ba_validation_check(r)["overall_score"] for r in responses]
                avg_score = sum(validation_scores) / len(validation_scores)
                method_scores[model][f"{method}_rag"] = avg_score
                all_responses.extend(responses)
    
    # Initialize default values
    results["best_method"] = "No valid responses"
    results["avg_rouge1"] = 0.0
    results["avg_readability"] = 0.0
    results["method_scores"] = method_scores
    
    # Calculate best method only if we have valid scores
    for model in method_scores:
        if method_scores[model]:
            best_method = max(method_scores[model].items(), key=lambda x: x[1])[0]
            best_score = method_scores[model][best_method]
            if results["best_method"] == "No valid responses" or best_score > method_scores[results["best_method"].split(" - ")[0].lower()][results["best_method"].split(" - ")[1].lower().replace(" ", "_")]:
                results["best_method"] = f"{model.upper()} - {best_method.replace('_', ' ').title()}"
    
    # Calculate averages only if we have valid responses
    if all_responses:
        results["avg_rouge1"] = sum(evaluator.evaluate_summaries([r])["Simple RAG"]["rouge1"] for r in all_responses) / len(all_responses)
        results["avg_readability"] = sum(evaluator.evaluate_summaries([r])["Simple RAG"]["readability_score"] for r in all_responses) / len(all_responses)
    
    return results

def get_relevant_scenarios(msg_type: str) -> list:
    """Get relevant test scenarios for a message type."""
    # Common scenarios for all messages
    common_scenarios = ["Basic Understanding", "Technical", "Error Handling"]
    
    # Message-specific scenarios
    type_scenarios = {
        "pacs.008": ["Payment Processing", "Compliance", "Cross-Border", "Business"],
        "pacs.002": ["Error Handling", "Status Updates"],
        "camt.053": ["Reconciliation", "Business", "Technical"],
        "pain.001": ["Payment Processing", "Business", "Compliance"]
    }
    
    # Filter scenarios
    relevant_categories = common_scenarios + type_scenarios.get(msg_type, [])
    return [s for s in TEST_SCENARIOS if s["category"] in relevant_categories]

def evaluate_responses(evaluator: ISO20022Evaluator, results: dict, messages: dict):
    """Evaluate and compare model responses."""
    print("\n📊 Response Evaluation\n")
    
    for msg_type, msg_list in messages.items():
        print(f"\nEvaluating {msg_type} Responses")
        print("=" * 40)
        
        relevant_scenarios = get_relevant_scenarios(msg_type)
        
        for scenario in relevant_scenarios:
            print(f"\nCategory: {scenario['category']}")
            
            for test in scenario['queries']:
                test_key = f"{msg_type}_{test['name']}"
                print(f"\nTest: {test['name']}")
                
                # Evaluate GPT responses
                print("\nGPT Results:")
                for rag_type in ["simple", "context", "reranker"]:
                    response = results["gpt"][rag_type].get(test_key, "")
                    if response and not response.startswith("Error"):
                        validation = evaluator.ba_validation_check(
                            response,
                            message_type=msg_type
                        )
                        print(f"\n{rag_type.title()} RAG:")
                        print(f"Score: {validation['overall_score']:.2f} ({validation['status']})")
                        print("Checks:", ", ".join(f"{k}: {v}" for k, v in validation["checks"].items()))
                
                # Evaluate Gemini responses
                print("\nGemini Results:")
                for rag_type in ["simple", "context", "reranker"]:
                    response = results["gemini"][rag_type].get(test_key, "")
                    if response and not response.startswith("Error"):
                        validation = evaluator.ba_validation_check(
                            response,
                            message_type=msg_type
                        )
                        print(f"\n{rag_type.title()} RAG:")
                        print(f"Score: {validation['overall_score']:.2f} ({validation['status']})")
                        print("Checks:", ", ".join(f"{k}: {v}" for k, v in validation["checks"].items()))

def main():
    """Run the model comparison tests."""
    # Get API keys
    openai_key = os.getenv('OPENAI_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not openai_key or not gemini_key:
        print("⚠️  Please set OPENAI_API_KEY and GEMINI_API_KEY environment variables")
        return
    
    # Initialize RAG and evaluator
    print("🚀 Initializing ISO 20022 RAG System...")
    rag = ISO20022RAG(openai_key=openai_key, gemini_key=gemini_key)
    evaluator = ISO20022Evaluator()
    
    # Generate test messages
    print("📝 Generating test messages...")
    messages = TEST_MESSAGES
    
    # Run tests
    results = run_model_comparison(openai_key=openai_key, gemini_key=gemini_key)
    
    # Evaluate responses
    evaluate_responses(evaluator, results, messages)

if __name__ == "__main__":
    main() 