"""Sample ISO 20022 messages for testing and demonstration."""

# XML namespace for ISO 20022 messages
XML_NAMESPACE = {
    'ns': 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10'
}

# Basic credit transfer message
SAMPLE_PACS008 = """<?xml version="1.0" encoding="UTF-8"?>
<ns:Document xmlns:ns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10">
  <ns:FIToFICstmrCdtTrf>
    <ns:GrpHdr>
      <ns:MsgId>MSG123456789</ns:MsgId>
      <ns:CreDtTm>2025-07-16T10:30:00Z</ns:CreDtTm>
      <ns:NbOfTxs>1</ns:NbOfTxs>
      <ns:TtlIntrBkSttlmAmt Ccy="USD">12345.67</ns:TtlIntrBkSttlmAmt>
    </ns:GrpHdr>
    <ns:CdtTrfTxInf>
      <ns:PmtId>
        <ns:InstrId>INSTR123</ns:InstrId>
        <ns:EndToEndId>E2E123456</ns:EndToEndId>
      </ns:PmtId>
      <ns:IntrBkSttlmAmt Ccy="USD">12345.67</ns:IntrBkSttlmAmt>
      <ns:ChrgBr>SHAR</ns:ChrgBr>
      <ns:Dbtr>
        <ns:Nm>John Doe</ns:Nm>
        <ns:PstlAdr>
          <ns:Ctry>US</ns:Ctry>
        </ns:PstlAdr>
      </ns:Dbtr>
      <ns:DbtrAcct>
        <ns:Id>
          <ns:Othr>
            <ns:Id>1234567890</ns:Id>
          </ns:Othr>
        </ns:Id>
      </ns:DbtrAcct>
      <ns:DbtrAgt>
        <ns:FinInstnId>
          <ns:BICFI>BOFAUS3N</ns:BICFI>
        </ns:FinInstnId>
      </ns:DbtrAgt>
      <ns:CdtrAgt>
        <ns:FinInstnId>
          <ns:BICFI>CHASUS33</ns:BICFI>
        </ns:FinInstnId>
      </ns:CdtrAgt>
      <ns:Cdtr>
        <ns:Nm>Jane Smith</ns:Nm>
        <ns:PstlAdr>
          <ns:Ctry>US</ns:Ctry>
        </ns:PstlAdr>
      </ns:Cdtr>
      <ns:CdtrAcct>
        <ns:Id>
          <ns:Othr>
            <ns:Id>0987654321</ns:Id>
          </ns:Othr>
        </ns:Id>
      </ns:CdtrAcct>
    </ns:CdtTrfTxInf>
  </ns:FIToFICstmrCdtTrf>
</ns:Document>
"""

# International payment with multiple currencies
SAMPLE_INTERNATIONAL = """<?xml version="1.0" encoding="UTF-8"?>
<ns:Document xmlns:ns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10">
  <ns:FIToFICstmrCdtTrf>
    <ns:GrpHdr>
      <ns:MsgId>INTL987654321</ns:MsgId>
      <ns:CreDtTm>2025-07-17T14:45:00Z</ns:CreDtTm>
      <ns:NbOfTxs>1</ns:NbOfTxs>
      <ns:TtlIntrBkSttlmAmt Ccy="EUR">50000.00</ns:TtlIntrBkSttlmAmt>
    </ns:GrpHdr>
    <ns:CdtTrfTxInf>
      <ns:PmtId>
        <ns:InstrId>INTL456</ns:InstrId>
        <ns:EndToEndId>E2E789012</ns:EndToEndId>
      </ns:PmtId>
      <ns:IntrBkSttlmAmt Ccy="EUR">50000.00</ns:IntrBkSttlmAmt>
      <ns:XchgRate>1.0850</ns:XchgRate>
      <ns:ChrgBr>SHAR</ns:ChrgBr>
      <ns:Dbtr>
        <ns:Nm>Tech Corp GmbH</ns:Nm>
        <ns:PstlAdr>
          <ns:Ctry>DE</ns:Ctry>
          <ns:AdrLine>Hauptstrasse 123, Berlin</ns:AdrLine>
        </ns:PstlAdr>
      </ns:Dbtr>
      <ns:DbtrAcct>
        <ns:Id>
          <ns:IBAN>DE89370400440532013000</ns:IBAN>
        </ns:Id>
      </ns:DbtrAcct>
      <ns:DbtrAgt>
        <ns:FinInstnId>
          <ns:BICFI>DEUTDEFF</ns:BICFI>
        </ns:FinInstnId>
      </ns:DbtrAgt>
      <ns:CdtrAgt>
        <ns:FinInstnId>
          <ns:BICFI>BNPAFRPP</ns:BICFI>
        </ns:FinInstnId>
      </ns:CdtrAgt>
      <ns:Cdtr>
        <ns:Nm>Innovation SARL</ns:Nm>
        <ns:PstlAdr>
          <ns:Ctry>FR</ns:Ctry>
          <ns:AdrLine>123 Rue de Paris, Paris</ns:AdrLine>
        </ns:PstlAdr>
      </ns:Cdtr>
      <ns:CdtrAcct>
        <ns:Id>
          <ns:IBAN>FR7630006000011234567890189</ns:IBAN>
        </ns:Id>
      </ns:CdtrAcct>
      <ns:RmtInf>
        <ns:Ustrd>Invoice 2025-0123 Payment</ns:Ustrd>
      </ns:RmtInf>
    </ns:CdtTrfTxInf>
  </ns:FIToFICstmrCdtTrf>
</ns:Document>
"""

# High-value payment with additional compliance checks
SAMPLE_HIGH_VALUE = """<?xml version="1.0" encoding="UTF-8"?>
<ns:Document xmlns:ns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10">
  <ns:FIToFICstmrCdtTrf>
    <ns:GrpHdr>
      <ns:MsgId>HV123456789</ns:MsgId>
      <ns:CreDtTm>2025-07-18T09:15:00Z</ns:CreDtTm>
      <ns:NbOfTxs>1</ns:NbOfTxs>
      <ns:TtlIntrBkSttlmAmt Ccy="USD">1000000.00</ns:TtlIntrBkSttlmAmt>
    </ns:GrpHdr>
    <ns:CdtTrfTxInf>
      <ns:PmtId>
        <ns:InstrId>HV789</ns:InstrId>
        <ns:EndToEndId>E2E456789</ns:EndToEndId>
      </ns:PmtId>
      <ns:IntrBkSttlmAmt Ccy="USD">1000000.00</ns:IntrBkSttlmAmt>
      <ns:ChrgBr>SHAR</ns:ChrgBr>
      <ns:Dbtr>
        <ns:Nm>Global Investments LLC</ns:Nm>
        <ns:PstlAdr>
          <ns:Ctry>US</ns:Ctry>
          <ns:AdrLine>100 Wall Street, New York</ns:AdrLine>
        </ns:PstlAdr>
        <ns:Id>
          <ns:OrgId>
            <ns:LEI>724500ABC123DEF456GH</ns:LEI>
          </ns:OrgId>
        </ns:Id>
      </ns:Dbtr>
      <ns:DbtrAcct>
        <ns:Id>
          <ns:Othr>
            <ns:Id>9876543210</ns:Id>
          </ns:Othr>
        </ns:Id>
      </ns:DbtrAcct>
      <ns:DbtrAgt>
        <ns:FinInstnId>
          <ns:BICFI>JPMCUS33</ns:BICFI>
        </ns:FinInstnId>
      </ns:DbtrAgt>
      <ns:CdtrAgt>
        <ns:FinInstnId>
          <ns:BICFI>GSACGB2L</ns:BICFI>
        </ns:FinInstnId>
      </ns:CdtrAgt>
      <ns:Cdtr>
        <ns:Nm>European Asset Management Ltd</ns:Nm>
        <ns:PstlAdr>
          <ns:Ctry>GB</ns:Ctry>
          <ns:AdrLine>1 London Bridge, London</ns:AdrLine>
        </ns:PstlAdr>
        <ns:Id>
          <ns:OrgId>
            <ns:LEI>213800XYZ456ABC789DE</ns:LEI>
          </ns:OrgId>
        </ns:Id>
      </ns:Cdtr>
      <ns:CdtrAcct>
        <ns:Id>
          <ns:IBAN>GB29NWBK60161331926819</ns:IBAN>
        </ns:Id>
      </ns:CdtrAcct>
      <ns:RgltryRptg>
        <ns:Dtls>
          <ns:Tp>UKREG</ns:Tp>
          <ns:Cd>GBFCA</ns:Cd>
        </ns:Dtls>
      </ns:RgltryRptg>
      <ns:RmtInf>
        <ns:Ustrd>Portfolio Investment Transfer Q3 2025</ns:Ustrd>
      </ns:RmtInf>
    </ns:CdtTrfTxInf>
  </ns:FIToFICstmrCdtTrf>
</ns:Document>
"""

# Expected summaries for validation
EXPECTED_SUMMARIES = {
    "basic": "Payment of 12,345.67 USD was made on July 16, 2025 from John Doe to Jane Smith.",
    
    "international": """International payment of 50,000.00 EUR from Tech Corp GmbH (Germany) to Innovation SARL (France).
Transfer executed on July 17, 2025 with exchange rate 1.0850.
Payment routed from DEUTDEFF to BNPAFRPP for Invoice 2025-0123.""",
    
    "high_value": """High-value transfer of 1,000,000.00 USD from Global Investments LLC to European Asset Management Ltd.
Transaction executed on July 18, 2025 with enhanced compliance checks.
LEI identifiers and regulatory reporting included for both parties.
Payment purpose: Portfolio Investment Transfer Q3 2025."""
}

# Sample validation data
VALIDATION_DATA = {
    "basic": {
        "message_id": "MSG123456789",
        "date": "2025-07-16T10:30:00Z",
        "amount": "12345.67",
        "currency": "USD",
        "debtor_name": "John Doe",
        "creditor_name": "Jane Smith",
        "debtor_bank": "BOFAUS3N",
        "creditor_bank": "CHASUS33"
    },
    "international": {
        "message_id": "INTL987654321",
        "date": "2025-07-17T14:45:00Z",
        "amount": "50000.00",
        "currency": "EUR",
        "exchange_rate": "1.0850",
        "debtor_name": "Tech Corp GmbH",
        "creditor_name": "Innovation SARL",
        "debtor_bank": "DEUTDEFF",
        "creditor_bank": "BNPAFRPP",
        "purpose": "Invoice 2025-0123 Payment"
    },
    "high_value": {
        "message_id": "HV123456789",
        "date": "2025-07-18T09:15:00Z",
        "amount": "1000000.00",
        "currency": "USD",
        "debtor_name": "Global Investments LLC",
        "creditor_name": "European Asset Management Ltd",
        "debtor_bank": "JPMCUS33",
        "creditor_bank": "GSACGB2L",
        "debtor_lei": "724500ABC123DEF456GH",
        "creditor_lei": "213800XYZ456ABC789DE",
        "purpose": "Portfolio Investment Transfer Q3 2025"
    }
} 