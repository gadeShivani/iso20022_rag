"""ISO 20022 message type definitions and templates."""

# Message type definitions
MESSAGE_TYPES = {
    "pacs": {
        "pacs.008": "FIToFICustomerCreditTransfer - Customer credit transfer",
        "pacs.009": "FinancialInstitutionCreditTransfer - Bank-to-bank credit transfer",
        "pacs.002": "FIToFIPaymentStatusReport - Payment status report",
        "pacs.004": "PaymentReturn - Return of funds",
        "pacs.028": "FIToFIPaymentStatusRequest - Payment status inquiry"
    },
    "pain": {
        "pain.001": "CustomerCreditTransferInitiation - Payment initiation",
        "pain.002": "CustomerPaymentStatusReport - Payment status report to customer",
        "pain.007": "CustomerPaymentReversal - Payment reversal",
        "pain.008": "CustomerDirectDebitInitiation - Direct debit initiation"
    },
    "camt": {
        "camt.052": "BankToCustomerAccountReport - Account report",
        "camt.053": "BankToCustomerStatement - Bank statement",
        "camt.054": "BankToCustomerDebitCreditNotification - Debit/credit notification",
        "camt.029": "ResolutionOfInvestigation - Investigation outcome",
        "camt.056": "FIToFIPaymentCancellationRequest - Cancel payment request"
    },
    "setr": {
        "setr.004": "RedemptionBulkOrder - Bulk redemption order",
        "setr.010": "SubscriptionBulkOrder - Bulk subscription order",
        "setr.012": "SubscriptionOrder - Single subscription order"
    },
    "secl": {
        "secl.010": "SettlementObligation - Settlement obligation report",
        "secl.003": "NetPositionReport - Net position report"
    }
}

# XML namespace definitions
XML_NAMESPACES = {
    "pacs.008": "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10",
    "pacs.009": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.10",
    "pacs.002": "urn:iso:std:iso:20022:tech:xsd:pacs.002.001.12",
    "pacs.004": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.11",
    "pacs.028": "urn:iso:std:iso:20022:tech:xsd:pacs.028.001.05",
    "pain.001": "urn:iso:std:iso:20022:tech:xsd:pain.001.001.11",
    "pain.002": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.12",
    "pain.007": "urn:iso:std:iso:20022:tech:xsd:pain.007.001.11",
    "pain.008": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.10",
    "camt.052": "urn:iso:std:iso:20022:tech:xsd:camt.052.001.10",
    "camt.053": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.10",
    "camt.054": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.10",
    "camt.029": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.12",
    "camt.056": "urn:iso:std:iso:20022:tech:xsd:camt.056.001.11",
    "setr.004": "urn:iso:std:iso:20022:tech:xsd:setr.004.001.04",
    "setr.010": "urn:iso:std:iso:20022:tech:xsd:setr.010.001.04",
    "setr.012": "urn:iso:std:iso:20022:tech:xsd:setr.012.001.04",
    "secl.010": "urn:iso:std:iso:20022:tech:xsd:secl.010.001.03",
    "secl.003": "urn:iso:std:iso:20022:tech:xsd:secl.003.001.03"
}

# Common XML elements and structures
COMMON_ELEMENTS = {
    "header": """
    <GrpHdr>
        <MsgId>{msg_id}</MsgId>
        <CreDtTm>{created_at}</CreDtTm>
        <NbOfTxs>{num_transactions}</NbOfTxs>
        <TtlIntrBkSttlmAmt Ccy="{currency}">{amount}</TtlIntrBkSttlmAmt>
    </GrpHdr>
    """,
    
    "party": """
    <{party_type}>
        <Nm>{name}</Nm>
        <PstlAdr>
            <Ctry>{country}</Ctry>
            <AdrLine>{address}</AdrLine>
        </PstlAdr>
        {id_block}
    </{party_type}>
    """,
    
    "bank": """
    <FinInstnId>
        <BICFI>{bic}</BICFI>
        <Nm>{name}</Nm>
        <PstlAdr>
            <Ctry>{country}</Ctry>
        </PstlAdr>
    </FinInstnId>
    """,
    
    "account": """
    <Id>
        <{id_type}>
            <Id>{account_id}</Id>
        </{id_type}>
    </Id>
    """,
    
    "amount": """
    <{amount_type} Ccy="{currency}">{value}</{amount_type}>
    """
}

# Organization identifiers
ORGANIZATION_TYPES = {
    "LEI": "Legal Entity Identifier",
    "DUNS": "Dun & Bradstreet Number",
    "BIC": "Bank Identifier Code",
    "TXID": "Tax Identification Number"
}

# Currency codes with descriptions
CURRENCIES = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "CHF": "Swiss Franc",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CNY": "Chinese Yuan",
    "HKD": "Hong Kong Dollar",
    "SGD": "Singapore Dollar"
}

# Country codes with financial centers
COUNTRIES = {
    "US": {"name": "United States", "financial_center": "New York"},
    "GB": {"name": "United Kingdom", "financial_center": "London"},
    "DE": {"name": "Germany", "financial_center": "Frankfurt"},
    "FR": {"name": "France", "financial_center": "Paris"},
    "JP": {"name": "Japan", "financial_center": "Tokyo"},
    "CH": {"name": "Switzerland", "financial_center": "Zurich"},
    "SG": {"name": "Singapore", "financial_center": "Singapore"},
    "HK": {"name": "Hong Kong", "financial_center": "Hong Kong"},
    "CN": {"name": "China", "financial_center": "Shanghai"},
    "AU": {"name": "Australia", "financial_center": "Sydney"}
}

# Bank codes with names
BANK_CODES = {
    "BOFAUS3N": "Bank of America",
    "CHASUS33": "JPMorgan Chase",
    "DEUTDEFF": "Deutsche Bank",
    "BNPAFRPP": "BNP Paribas",
    "HSBCGB2L": "HSBC UK",
    "UBSWCHZH": "UBS",
    "SGSBSGSG": "Societe Generale Singapore",
    "HSBCHKHH": "HSBC Hong Kong",
    "ICBKCNBJ": "ICBC China",
    "ANZEAU3M": "ANZ Bank"
}

# Payment purposes
PAYMENT_PURPOSES = {
    "TRADE": "Trade Settlement",
    "SALA": "Salary Payment",
    "DIVI": "Dividend Payment",
    "TAXS": "Tax Payment",
    "HEDG": "Hedging Operation",
    "INTC": "Intra-Company Payment",
    "TREA": "Treasury Operation",
    "GOVT": "Government Payment",
    "PENS": "Pension Payment",
    "INVS": "Investment Settlement"
}

# Regulatory reporting codes
REGULATORY_CODES = {
    "UKREG": "UK Regulatory Reporting",
    "USREG": "US Regulatory Reporting",
    "EUREG": "EU Regulatory Reporting",
    "ASREG": "Asia Regulatory Reporting",
    "GBFCA": "UK FCA Reporting",
    "USFINC": "US FinCEN Reporting",
    "EUESMA": "EU ESMA Reporting",
    "HKMA": "Hong Kong Monetary Authority",
    "SGMAS": "Singapore MAS Reporting",
    "AUREG": "Australian Regulatory Reporting"
}

# Status codes
STATUS_CODES = {
    "ACCC": "Accepted and Settled",
    "ACCP": "Accepted",
    "PDNG": "Pending",
    "RJCT": "Rejected",
    "CANC": "Cancelled",
    "ACSP": "Accepted for Settlement",
    "ACWC": "Accepted with Change",
    "PART": "Partially Accepted",
    "RCVD": "Received",
    "INVL": "Invalid"
}

# Charge bearers
CHARGE_BEARERS = {
    "DEBT": "All transaction charges are to be borne by the debtor",
    "CRED": "All transaction charges are to be borne by the creditor",
    "SHAR": "Shared charges (SHA) - Transaction charges on the sender side are borne by the debtor, transaction charges on the receiver side are borne by the creditor",
    "SLEV": "Following Service Level - Charges are to be applied following the rules agreed in the service level and/or scheme"
} 