"""RAG implementations for ISO 20022 message processing."""

import os
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET
from openai import OpenAI
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# XML namespaces for different message types
XML_NAMESPACES = {
    'pacs.008': {'ns': 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10'},
    'pacs.002': {'ns': 'urn:iso:std:iso:20022:tech:xsd:pacs.002.001.12'},
    'camt.053': {'ns': 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.10'},
    'pain.001': {'ns': 'urn:iso:std:iso:20022:tech:xsd:pain.001.001.11'}
}

# Constants for Gemini model configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-pro"
GEMINI_TEMPERATURE = 0.3
GPT_TEMPERATURE = 0.3

class ISO20022RAG:
    def __init__(self, openai_key: Optional[str] = None, gemini_key: Optional[str] = None):
        """Initialize RAG with API keys."""
        self.openai_key = openai_key
        self.gemini_key = gemini_key
        self.openai_client = None
        self.gemini_model = None
        
        # Initialize clients only if keys are provided
        if openai_key:
            self.openai_client = OpenAI(api_key=openai_key)
        
        if gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                generation_config = {
                    "temperature": 0.3,
                    "max_output_tokens": 2048,
                }
                self.gemini_model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro",
                    generation_config=generation_config
                )
            except Exception as e:
                print(f"Error initializing Gemini: {str(e)}")
    
    def _detect_message_type(self, root: ET.Element) -> str:
        """Detect the message type from the XML root element."""
        if root.find('.//ns:FIToFICstmrCdtTrf', XML_NAMESPACES['pacs.008']) is not None:
            return 'pacs.008'
        elif root.find('.//ns:FIToFIPmtStsRpt', XML_NAMESPACES['pacs.002']) is not None:
            return 'pacs.002'
        elif root.find('.//ns:BkToCstmrStmt', XML_NAMESPACES['camt.053']) is not None:
            return 'camt.053'
        elif root.find('.//ns:CstmrCdtTrfInitn', XML_NAMESPACES['pain.001']) is not None:
            return 'pain.001'
        else:
            raise ValueError("Unknown message type")
    
    def parse_iso_message(self, xml_content: str) -> Dict:
        """Parse ISO 20022 XML message into structured data."""
        # Try each namespace until we find the right one
        root = None
        msg_type = None
        
        for type_name, ns in XML_NAMESPACES.items():
            try:
                root = ET.fromstring(xml_content)
                if self._detect_message_type(root) == type_name:
                    msg_type = type_name
                    break
            except ET.ParseError:
                continue
        
        if not root or not msg_type:
            raise ValueError("Could not parse XML message or determine message type")
        
        ns = XML_NAMESPACES[msg_type]
        
        # Common fields for all message types
        data = {
            'message_type': msg_type,
            'message_id': root.find('.//ns:MsgId', ns).text,
            'created_at': root.find('.//ns:CreDtTm', ns).text
        }
        
        # Message type specific fields
        if msg_type == 'pacs.008':
            data.update({
                'amount': root.find('.//ns:TtlIntrBkSttlmAmt', ns).text,
                'currency': root.find('.//ns:TtlIntrBkSttlmAmt', ns).get('Ccy'),
                'debtor_name': root.find('.//ns:Dbtr/ns:Nm', ns).text,
                'creditor_name': root.find('.//ns:Cdtr/ns:Nm', ns).text,
                'debtor_bank': root.find('.//ns:DbtrAgt//ns:BICFI', ns).text,
                'creditor_bank': root.find('.//ns:CdtrAgt//ns:BICFI', ns).text
            })
            
            # Optional fields
            charge_bearer = root.find('.//ns:ChrgBr', ns)
            if charge_bearer is not None:
                data['charge_bearer'] = charge_bearer.text
            
            purpose = root.find('.//ns:RmtInf/ns:Ustrd', ns)
            if purpose is not None:
                data['purpose'] = purpose.text
        
        elif msg_type == 'pacs.002':
            # Status report fields
            data.update({
                'original_message_id': root.find('.//ns:OrgnlMsgId', ns).text,
                'original_message_type': root.find('.//ns:OrgnlMsgNmId', ns).text,
                'group_status': root.find('.//ns:GrpSts', ns).text
            })
        
        elif msg_type == 'camt.053':
            # Statement fields
            data.update({
                'statement_id': root.find('.//ns:Stmt/ns:Id', ns).text,
                'account_id': root.find('.//ns:Stmt/ns:Acct/ns:Id/ns:IBAN', ns).text,
                'balance_amount': root.find('.//ns:Stmt/ns:Bal/ns:Amt', ns).text,
                'balance_currency': root.find('.//ns:Stmt/ns:Bal/ns:Amt', ns).get('Ccy')
            })
            
            # Get transactions
            entries = root.findall('.//ns:Stmt/ns:Ntry', ns)
            data['transactions'] = []
            for entry in entries:
                txn = {
                    'amount': entry.find('.//ns:Amt', ns).text,
                    'currency': entry.find('.//ns:Amt', ns).get('Ccy'),
                    'credit_debit': entry.find('.//ns:CdtDbtInd', ns).text,
                    'status': entry.find('.//ns:Sts', ns).text,
                    'booking_date': entry.find('.//ns:BookgDt/ns:DtTm', ns).text
                }
                data['transactions'].append(txn)
        
        elif msg_type == 'pain.001':
            # Payment initiation fields
            data.update({
                'initiator_name': root.find('.//ns:InitgPty/ns:Nm', ns).text,
                'payment_method': root.find('.//ns:PmtInf/ns:PmtMtd', ns).text,
                'execution_date': root.find('.//ns:PmtInf/ns:ReqdExctnDt', ns).text,
                'debtor_name': root.find('.//ns:Dbtr/ns:Nm', ns).text,
                'debtor_account': root.find('.//ns:DbtrAcct/ns:Id/ns:IBAN', ns).text,
                'amount': root.find('.//ns:InstdAmt', ns).text,
                'currency': root.find('.//ns:InstdAmt', ns).get('Ccy'),
                'creditor_name': root.find('.//ns:Cdtr/ns:Nm', ns).text,
                'creditor_account': root.find('.//ns:CdtrAcct/ns:Id/ns:IBAN', ns).text
            })
        
        return data
    
    def simple_rag_summary(
        self,
        message_data: Dict,
        model_name: str = "gpt-4",
        query: str = None
    ) -> str:
        """Simple RAG: Basic retrieval and generation."""
        # Knowledge base
        iso_knowledge_base = [
            {
                "field": "pacs.008",
                "description": "Customer credit transfer message",
                "key_fields": ["MsgId", "CreDtTm", "TtlIntrBkSttlmAmt", "Dbtr", "Cdtr"],
                "summary_template": "Payment of {amount} {currency} was made on {created_at} from {debtor_name} to {creditor_name}."
            },
            {
                "field": "pacs.002",
                "description": "Payment status report message",
                "key_fields": ["MsgId", "CreDtTm", "OrgnlMsgId", "GrpSts"],
                "summary_template": "Status report for message {original_message_id}: {group_status} at {created_at}."
            },
            {
                "field": "camt.053",
                "description": "Bank statement message",
                "key_fields": ["MsgId", "CreDtTm", "StmtId", "Bal"],
                "summary_template": "Statement {statement_id} with balance {balance_amount} {balance_currency} at {created_at}."
            },
            {
                "field": "pain.001",
                "description": "Payment initiation message",
                "key_fields": ["MsgId", "CreDtTm", "InitgPty", "Dbtr", "Cdtr"],
                "summary_template": "Payment initiation from {debtor_name} to {creditor_name} for {amount} {currency} on {created_at}."
            }
        ]
        
        # Find relevant template
        msg_type = message_data.get('message_type', '')
        template = next((t for t in iso_knowledge_base if t["field"] == msg_type), None)
        
        if not template:
            raise ValueError(f"Unknown message type: {msg_type}")
        
        # Generate summary using template
        if query:
            prompt = f"""
            Analyze this ISO 20022 financial message to answer: {query}
            
            Message Type: {template['description']}
            Key Fields: {template['key_fields']}
            Message Data: {message_data}
            
            Provide a clear, business-friendly response focusing on the specific query.
            """
        else:
            summary = template["summary_template"].format(**message_data)
            prompt = f"""
            Generate a summary for this ISO 20022 financial message:
            
            Message Type: {template['description']}
            Summary: {summary}
            Message Data: {message_data}
            
            Provide a clear, business-friendly summary.
            """
        
        return self._call_llm(prompt, model_name)
    
    def context_enriched_rag_summary(
        self,
        message_data: Dict,
        model_name: str = "gpt-4",
        query: str = None
    ) -> str:
        """Context-Enriched RAG: Enhanced retrieval with document-level context."""
        
        # Get message type specific context
        msg_type = message_data['message_type']
        msg_contexts = {
            'pacs.008': {
                "description": "Customer credit transfer",
                "key_points": [
                    f"Transfer amount: {message_data.get('amount', 'N/A')} {message_data.get('currency', 'N/A')}",
                    f"From: {message_data.get('debtor_name', 'N/A')} (Bank: {message_data.get('debtor_bank', 'N/A')})",
                    f"To: {message_data.get('creditor_name', 'N/A')} (Bank: {message_data.get('creditor_bank', 'N/A')})",
                    f"Date: {message_data.get('created_at', 'N/A')}"
                ],
                "compliance": [
                    "Verify sender and receiver details",
                    "Check for valid bank identifiers",
                    "Ensure positive amount in valid currency"
                ]
            },
            'pacs.002': {
                "description": "Payment status report",
                "key_points": [
                    f"Status: {message_data.get('group_status', 'N/A')}",
                    f"Original message: {message_data.get('original_message_id', 'N/A')}",
                    f"Message type: {message_data.get('original_message_type', 'N/A')}",
                    f"Date: {message_data.get('created_at', 'N/A')}"
                ],
                "compliance": [
                    "Valid status code",
                    "Reference to original message",
                    "Proper status reason if rejected"
                ]
            },
            'camt.053': {
                "description": "Bank statement",
                "key_points": [
                    f"Statement ID: {message_data.get('statement_id', 'N/A')}",
                    f"Account: {message_data.get('account_id', 'N/A')}",
                    f"Balance: {message_data.get('balance_amount', 'N/A')} {message_data.get('balance_currency', 'N/A')}",
                    f"Date: {message_data.get('created_at', 'N/A')}"
                ],
                "compliance": [
                    "Valid account identifier",
                    "Balance calculation accuracy",
                    "Transaction details completeness"
                ]
            },
            'pain.001': {
                "description": "Payment initiation",
                "key_points": [
                    f"Amount: {message_data.get('amount', 'N/A')} {message_data.get('currency', 'N/A')}",
                    f"Initiator: {message_data.get('initiator_name', 'N/A')}",
                    f"From: {message_data.get('debtor_name', 'N/A')} ({message_data.get('debtor_account', 'N/A')})",
                    f"To: {message_data.get('creditor_name', 'N/A')} ({message_data.get('creditor_account', 'N/A')})",
                    f"Date: {message_data.get('created_at', 'N/A')}"
                ],
                "compliance": [
                    "Valid account numbers",
                    "Authorized initiator",
                    "Sufficient funds check"
                ]
            }
        }
        
        context = msg_contexts.get(msg_type, {
            "description": "Unknown message type",
            "key_points": [f"Message ID: {message_data['message_id']}", f"Date: {message_data['created_at']}"],
            "compliance": ["Standard message validation"]
        })
        
        # Generate prompt based on query or default to summary
        if query:
            prompt = f"""
            Question about this {context['description']} message: {query}

            Key Information:
            {chr(10).join(f"• {point}" for point in context['key_points'])}

            Compliance Checks:
            {chr(10).join(f"• {check}" for check in context['compliance'])}

            Please provide a clear, concise response focusing on the question.
            Keep the language business-friendly and avoid technical jargon.
            Limit the response to 2-3 sentences unless more detail is specifically requested.
            """
        else:
            prompt = f"""
            Summarize this {context['description']} message:

            Key Information:
            {chr(10).join(f"• {point}" for point in context['key_points'])}

            Please provide a clear, concise summary in 2-3 sentences.
            Focus on the key business information and impact.
            Use business-friendly language and avoid technical details unless crucial.
            """
        
        return self._call_llm(prompt, model_name)
    
    def reranker_rag_summary(
        self,
        message_data: Dict,
        model_name: str = "gpt-4",
        query: str = None
    ) -> str:
        """Reranker RAG: Uses reranking to prioritize most relevant context chunks."""
        # Generate context chunks based on message type
        context_chunks = []
        
        # Common chunks for all message types
        context_chunks.extend([
            {
                "content": f"Message ID: {message_data['message_id']}",
                "relevance": 0.5,
                "type": "metadata"
            },
            {
                "content": f"Created at: {message_data['created_at']}",
                "relevance": 0.6,
                "type": "metadata"
            }
        ])
        
        # Message type specific chunks
        if message_data['message_type'] == 'pacs.008':
            context_chunks.extend([
                {
                    "content": f"Payment transaction: {message_data['amount']} {message_data['currency']}",
                    "relevance": 0.9,
                    "type": "transaction_details"
                },
                {
                    "content": f"Parties involved: {message_data['debtor_name']} → {message_data['creditor_name']}",
                    "relevance": 0.8,
                    "type": "party_information"
                },
                {
                    "content": f"Banks: {message_data['debtor_bank']} → {message_data['creditor_bank']}",
                    "relevance": 0.7,
                    "type": "banking_details"
                }
            ])
        elif message_data['message_type'] == 'pacs.002':
            context_chunks.extend([
                {
                    "content": f"Status: {message_data['group_status']}",
                    "relevance": 0.9,
                    "type": "status"
                },
                {
                    "content": f"Original message: {message_data['original_message_id']} ({message_data['original_message_type']})",
                    "relevance": 0.8,
                    "type": "reference"
                }
            ])
        elif message_data['message_type'] == 'camt.053':
            context_chunks.extend([
                {
                    "content": f"Statement ID: {message_data['statement_id']}",
                    "relevance": 0.7,
                    "type": "metadata"
                },
                {
                    "content": f"Account: {message_data['account_id']}",
                    "relevance": 0.8,
                    "type": "account"
                },
                {
                    "content": f"Balance: {message_data['balance_amount']} {message_data['balance_currency']}",
                    "relevance": 0.9,
                    "type": "balance"
                }
            ])
            # Add transactions if available
            if 'transactions' in message_data:
                for i, txn in enumerate(message_data['transactions']):
                    context_chunks.append({
                        "content": f"Transaction {i+1}: {txn['amount']} {txn['currency']} ({txn['credit_debit']})",
                        "relevance": 0.6 - (i * 0.1),  # Decrease relevance for each transaction
                        "type": "transaction"
                    })
        elif message_data['message_type'] == 'pain.001':
            context_chunks.extend([
                {
                    "content": f"Payment initiation: {message_data['amount']} {message_data['currency']}",
                    "relevance": 0.9,
                    "type": "transaction_details"
                },
                {
                    "content": f"Initiator: {message_data['initiator_name']}",
                    "relevance": 0.7,
                    "type": "party_information"
                },
                {
                    "content": f"From: {message_data['debtor_name']} ({message_data['debtor_account']})",
                    "relevance": 0.8,
                    "type": "debtor_details"
                },
                {
                    "content": f"To: {message_data['creditor_name']} ({message_data['creditor_account']})",
                    "relevance": 0.8,
                    "type": "creditor_details"
                }
            ])
        
        # Rerank by relevance
        reranked_chunks = sorted(context_chunks, key=lambda x: x['relevance'], reverse=True)
        
        # Use top 3 most relevant chunks
        top_chunks = reranked_chunks[:3]
        
        if query:
            prompt = f"""
            Analyze this ISO 20022 financial message to answer: {query}
            
            Most relevant information:
            Primary: {top_chunks[0]['content']}
            Secondary: {top_chunks[1]['content']}
            Additional: {top_chunks[2]['content']}
            
            Message Type: {message_data['message_type']}
            
            Provide a clear, business-friendly response focusing on the specific query.
            """
        else:
            prompt = f"""
            Generate a summary using the most relevant information:
            
            Primary: {top_chunks[0]['content']}
            Secondary: {top_chunks[1]['content']}
            Additional: {top_chunks[2]['content']}
            
            Message Type: {message_data['message_type']}
            
            Create a concise business summary focusing on the key details.
            Keep the response clear and direct.
            """
        
        return self._call_llm(prompt, model_name)
    
    def _validate_api_keys(self, model_name: str) -> bool:
        """Validate that required API keys are available."""
        if model_name.startswith('gpt') and not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        elif not model_name.startswith('gpt') and not self.gemini_model:
            raise ValueError("Gemini API key not configured")
        return True

    def _call_llm(self, prompt: str, model_name: str) -> str:
        """Call the appropriate LLM based on model name."""
        try:
            self._validate_api_keys(model_name)
            
            if model_name.startswith('gpt'):
                response = self.openai_client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                return response.choices[0].message.content
            else:
                try:
                    response = self.gemini_model.generate_content(prompt)
                    if not response.text:
                        return "Error: Empty response from Gemini"
                    return response.text
                except Exception as e:
                    if "not found" in str(e):
                        # Try fallback to default model if specified model not found
                        self.gemini_model = genai.GenerativeModel("gemini-1.5-pro")
                        response = self.gemini_model.generate_content(prompt)
                        return response.text
                    raise
        except Exception as e:
            return f"Error calling {model_name}: {str(e)}" 