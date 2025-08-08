"""Hybrid RAG implementation combining Simple, Context-Enriched, and Reranker RAGs."""

from typing import Dict, List, Optional, Tuple
import numpy as np
from .rag_implementations import ISO20022RAG

class HybridRAG(ISO20022RAG):
    def __init__(self, openai_key: Optional[str] = None, gemini_key: Optional[str] = None):
        """Initialize Hybrid RAG with API keys."""
        super().__init__(openai_key=openai_key, gemini_key=gemini_key)
        
        # Weights for different RAG methods (can be adjusted based on performance)
        self.weights = {
            'simple': 0.3,      # Good for standard cases and quick responses
            'context': 0.4,     # Best for compliance and detailed analysis
            'reranker': 0.3     # Best for specific queries and complex cases
        }
        
        # Confidence thresholds for each method
        self.thresholds = {
            'simple': 0.7,
            'context': 0.8,
            'reranker': 0.75
        }
        
        # Message type specific weights
        self.message_type_weights = {
            'pacs.008': {
                'simple': 0.25,
                'context': 0.45,  # Higher weight for cross-border payments
                'reranker': 0.30
            },
            'pacs.002': {
                'simple': 0.40,   # Higher weight for status messages
                'context': 0.35,
                'reranker': 0.25
            },
            'camt.053': {
                'simple': 0.30,
                'context': 0.40,  # Higher weight for statement analysis
                'reranker': 0.30
            },
            'pain.001': {
                'simple': 0.35,
                'context': 0.35,
                'reranker': 0.30
            }
        }

    def _calculate_confidence(self, response: str, message_type: str) -> float:
        """Calculate confidence score for a response."""
        # Basic confidence metrics
        has_amounts = any(char.isdigit() for char in response)
        has_currency = any(curr in response for curr in ['USD', 'EUR', 'GBP', 'JPY', 'CHF'])
        has_parties = any(term in response.lower() for term in ['sender', 'receiver', 'debtor', 'creditor', 'bank'])
        
        # Message type specific checks
        type_specific_score = 0.0
        if message_type == 'pacs.008':
            type_specific_score = sum([
                'transfer' in response.lower(),
                'payment' in response.lower(),
                has_amounts,
                has_currency
            ]) / 4.0
        elif message_type == 'pacs.002':
            type_specific_score = sum([
                'status' in response.lower(),
                'original' in response.lower(),
                any(status in response.upper() for status in ['ACCP', 'ACSC', 'RJCT'])
            ]) / 3.0
        elif message_type == 'camt.053':
            type_specific_score = sum([
                'statement' in response.lower(),
                'balance' in response.lower(),
                has_amounts,
                has_currency
            ]) / 4.0
        elif message_type == 'pain.001':
            type_specific_score = sum([
                'initiation' in response.lower(),
                'payment' in response.lower(),
                has_amounts,
                has_parties
            ]) / 4.0
            
        # Combine scores
        base_score = sum([
            has_amounts,
            has_currency,
            has_parties,
            len(response.split()) > 10,  # Reasonable length
            '.' in response  # Complete sentences
        ]) / 5.0
        
        return (base_score * 0.6) + (type_specific_score * 0.4)

    def _adjust_weights(self, message_type: str, query: Optional[str] = None) -> Dict[str, float]:
        """Adjust weights based on message type and query."""
        # Start with message type specific weights
        weights = self.message_type_weights.get(message_type, self.weights)
        
        if query:
            query_lower = query.lower()
            
            # Adjust for compliance/regulatory queries
            if any(term in query_lower for term in ['compliance', 'regulatory', 'regulation', 'aml', 'kyc']):
                weights = {
                    'simple': weights['simple'] * 0.7,
                    'context': weights['context'] * 1.3,  # Increase context weight
                    'reranker': weights['reranker']
                }
            
            # Adjust for specific detail queries
            elif any(term in query_lower for term in ['specific', 'detail', 'explain', 'why', 'how']):
                weights = {
                    'simple': weights['simple'] * 0.8,
                    'context': weights['context'],
                    'reranker': weights['reranker'] * 1.2  # Increase reranker weight
                }
            
            # Adjust for quick summary queries
            elif any(term in query_lower for term in ['quick', 'summary', 'brief', 'short']):
                weights = {
                    'simple': weights['simple'] * 1.3,  # Increase simple weight
                    'context': weights['context'] * 0.8,
                    'reranker': weights['reranker'] * 0.9
                }
        
        # Normalize weights
        total = sum(weights.values())
        return {k: v/total for k, v in weights.items()}

    def hybrid_rag_summary(
        self,
        message_data: Dict,
        model_name: str = "gpt-4",
        query: Optional[str] = None
    ) -> Tuple[str, Dict]:
        """Generate summary using hybrid approach combining all RAG methods."""
        # Get adjusted weights
        weights = self._adjust_weights(message_data['message_type'], query)
        
        # Get responses from each method
        responses = {
            'simple': self.simple_rag_summary(message_data, model_name, query),
            'context': self.context_enriched_rag_summary(message_data, model_name, query),
            'reranker': self.reranker_rag_summary(message_data, model_name, query)
        }
        
        # Calculate confidence scores
        confidences = {
            method: self._calculate_confidence(response, message_data['message_type'])
            for method, response in responses.items()
        }
        
        # Adjust weights based on confidence scores
        for method, confidence in confidences.items():
            if confidence < self.thresholds[method]:
                weights[method] *= (confidence / self.thresholds[method])
        
        # Normalize weights again
        total_weight = sum(weights.values())
        weights = {k: v/total_weight for k, v in weights.items()}
        
        # Select best response based on confidence and weights
        weighted_scores = {
            method: confidence * weights[method]
            for method, confidence in confidences.items()
        }
        
        best_method = max(weighted_scores.items(), key=lambda x: x[1])[0]
        best_response = responses[best_method]
        
        # Return best response and metadata
        metadata = {
            'selected_method': best_method,
            'confidence_scores': confidences,
            'final_weights': weights,
            'weighted_scores': weighted_scores
        }
        
        return best_response, metadata

    def analyze_message(
        self,
        message_data: Dict,
        model_name: str = "gpt-4",
        query: Optional[str] = None
    ) -> Dict:
        """Comprehensive message analysis using hybrid approach."""
        # Get summary and metadata
        summary, metadata = self.hybrid_rag_summary(message_data, model_name, query)
        
        # Get all responses for comparison
        all_responses = {
            'simple': self.simple_rag_summary(message_data, model_name, query),
            'context': self.context_enriched_rag_summary(message_data, model_name, query),
            'reranker': self.reranker_rag_summary(message_data, model_name, query),
            'hybrid': summary
        }
        
        # Calculate confidence scores for all responses
        confidence_scores = {
            method: self._calculate_confidence(response, message_data['message_type'])
            for method, response in all_responses.items()
        }
        
        return {
            'summary': summary,
            'all_responses': all_responses,
            'confidence_scores': confidence_scores,
            'metadata': metadata,
            'message_type': message_data['message_type'],
            'analysis_method': 'hybrid_rag'
        } 