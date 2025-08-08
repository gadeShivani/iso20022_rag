"""Evaluation metrics for ISO20022 RAG implementations."""

import nltk
import re
from typing import Dict, List, Optional
import os
import ssl

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

        # Download punkt tokenizer if not already present
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)

    except Exception as e:
        print(f"Warning: Error setting up NLTK: {str(e)}")

# Run NLTK setup when module is imported
setup_nltk()

def simple_tokenize(text: str) -> List[str]:
    """Fallback tokenizer when NLTK fails."""
    # Split on common sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Filter out empty strings and normalize whitespace
    return [s.strip() for s in sentences if s.strip()]

class ISO20022Evaluator:
    """Evaluator for ISO20022 message processing."""

    def __init__(self):
        """Initialize evaluator with metrics configuration."""
        self.technical_terms = {
            'pacs.008': ['credit transfer', 'settlement', 'clearing', 'interbank', 'FIToFICustomerCreditTransfer'],
            'pacs.002': ['status', 'reason', 'rejection', 'acceptance', 'FIToFIPaymentStatusReport'],
            'camt.053': ['statement', 'balance', 'entry', 'transaction', 'BankToCustomerStatement'],
            'pain.001': ['initiation', 'debtor', 'creditor', 'CustomerCreditTransferInitiation']
        }
        
        self.business_terms = {
            'pacs.008': ['payment', 'transfer', 'sender', 'receiver', 'amount'],
            'pacs.002': ['confirmation', 'processing', 'status', 'result', 'response'],
            'camt.053': ['account', 'balance', 'transaction', 'statement', 'period'],
            'pain.001': ['payment', 'instruction', 'transfer', 'request', 'initiation']
        }
        
        self.compliance_terms = {
            'pacs.008': ['AML', 'sanctions', 'compliance', 'regulatory', 'verification'],
            'pacs.002': ['validation', 'compliance', 'check', 'verification', 'control'],
            'camt.053': ['reconciliation', 'audit', 'compliance', 'reporting', 'verification'],
            'pain.001': ['authorization', 'validation', 'compliance', 'verification', 'control']
        }

    def _tokenize_text(self, text: str) -> List[str]:
        """Tokenize text into sentences with fallback."""
        try:
            return nltk.sent_tokenize(text)
        except Exception as e:
            print(f"Warning: NLTK tokenization failed ({str(e)}), using fallback tokenizer")
            return simple_tokenize(text)

    def _calculate_term_density(self, text: str, terms: List[str]) -> float:
        """Calculate density of specific terms in text."""
        if not text or not terms:
            return 0.0
        
        text_lower = text.lower()
        term_count = sum(1 for term in terms if term.lower() in text_lower)
        return term_count / len(terms) if terms else 0.0

    def _check_numeric_accuracy(self, text: str) -> float:
        """Check accuracy of numeric values in text."""
        # Look for currency amounts with proper formatting
        amount_pattern = r'(?:EUR|USD|GBP|JPY|CHF)\s*[\d,.]+|\d+(?:,\d{3})*(?:\.\d{2})?'
        has_amounts = bool(re.search(amount_pattern, text))
        
        # Look for dates in common formats
        date_pattern = r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}'
        has_dates = bool(re.search(date_pattern, text))
        
        # Look for reference numbers
        ref_pattern = r'(?:REF|Reference|ID):\s*[A-Z0-9-]+'
        has_refs = bool(re.search(ref_pattern, text))
        
        # Calculate score based on presence of different numeric elements
        score = sum([has_amounts, has_dates, has_refs]) / 3.0
        return score

    def _check_currency_accuracy(self, text: str) -> float:
        """Check accuracy of currency handling in text."""
        # Look for standard currency codes
        currency_pattern = r'(?:EUR|USD|GBP|JPY|CHF)'
        has_currency_codes = bool(re.search(currency_pattern, text))
        
        # Look for properly formatted amounts
        amount_pattern = r'\d+(?:,\d{3})*(?:\.\d{2})?'
        has_formatted_amounts = bool(re.search(amount_pattern, text))
        
        # Look for currency symbols
        symbol_pattern = r'[€$£¥]'
        has_symbols = bool(re.search(symbol_pattern, text))
        
        # Calculate score
        score = sum([has_currency_codes, has_formatted_amounts, has_symbols]) / 3.0
        return score

    def evaluate_response(self, response: str, message_type: str) -> Dict:
        """Evaluate response quality for a given message type."""
        try:
            # Tokenize response
            sentences = self._tokenize_text(response)
            if not sentences:
                return {
                    "status": "ERROR",
                    "scores": {},
                    "metrics": {},
                    "improvement_areas": ["Empty or invalid response"]
                }

            # Calculate various metrics
            technical_density = self._calculate_term_density(
                response,
                self.technical_terms.get(message_type, [])
            )
            
            business_density = self._calculate_term_density(
                response,
                self.business_terms.get(message_type, [])
            )
            
            compliance_density = self._calculate_term_density(
                response,
                self.compliance_terms.get(message_type, [])
            )
            
            numeric_accuracy = self._check_numeric_accuracy(response)
            currency_accuracy = self._check_currency_accuracy(response)
            
            # Calculate readability (simplified)
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            readability_score = min(1.0, 2.0 / (1.0 + avg_sentence_length/20.0))
            
            # Identify improvement areas
            improvement_areas = []
            if technical_density < 0.3:
                improvement_areas.append("Increase technical detail")
            if business_density < 0.3:
                improvement_areas.append("Add more business context")
            if compliance_density < 0.2:
                improvement_areas.append("Include compliance aspects")
            if numeric_accuracy < 0.5:
                improvement_areas.append("Improve numeric accuracy")
            if currency_accuracy < 0.5:
                improvement_areas.append("Enhance currency handling")
            if readability_score < 0.6:
                improvement_areas.append("Improve readability")
            
            return {
                "status": "SUCCESS",
                "scores": {
                    "technical_density": round(technical_density, 2),
                    "business_density": round(business_density, 2),
                    "compliance_density": round(compliance_density, 2),
                    "numeric_accuracy": round(numeric_accuracy, 2),
                    "currency_accuracy": round(currency_accuracy, 2),
                    "readability": round(readability_score, 2)
                },
                "metrics": {
                    "sentence_count": len(sentences),
                    "avg_sentence_length": round(avg_sentence_length, 1),
                    "message_type": message_type
                },
                "improvement_areas": improvement_areas if improvement_areas else ["None"]
            }
            
        except Exception as e:
            return {
                "status": "ERROR",
                "scores": {},
                "metrics": {},
                "improvement_areas": [f"Evaluation error: {str(e)}"]
            } 