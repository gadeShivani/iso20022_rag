"""Generate sample ISO 20022 messages for testing."""

import random
from datetime import datetime, timedelta
from typing import List
import xml.dom.minidom as minidom

class ISO20022MessageGenerator:
    def __init__(self):
        self.banks = [
            ("DEUTDEFF", "Deutsche Bank"),
            ("CHASUS33", "JPMorgan Chase"),
            ("BARCGB22", "Barclays Bank"),
            ("BNPAFRPP", "BNP Paribas"),
            ("UBSWCHZH", "UBS"),
            ("CITIGB2L", "Citibank London"),
            ("HSBCHKHH", "HSBC Hong Kong"),
            ("MHCBJPJT", "Mizuho Bank")
        ]
        
        self.currencies = ["USD", "EUR", "GBP", "JPY", "CHF", "AUD"]
        self.countries = ["US", "GB", "DE", "FR", "CH", "JP", "HK", "SG"]
        
    def _generate_id(self, prefix: str = "MSG") -> str:
        """Generate a unique message ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices('0123456789', k=6))
        return f"{prefix}{timestamp}{random_suffix}"
    
    def _generate_amount(self) -> tuple:
        """Generate a random amount and currency."""
        amount = round(random.uniform(1000, 1000000), 2)
        currency = random.choice(self.currencies)
        return str(amount), currency
    
    def _generate_datetime(self, days_offset: int = 0) -> str:
        """Generate a datetime string with optional offset."""
        base_date = datetime.now() + timedelta(days=days_offset)
        return base_date.strftime("%Y-%m-%dT%H:%M:%S")
    
    def _generate_bank_info(self) -> tuple:
        """Generate random bank BIC and name."""
        return random.choice(self.banks)
    
    def _generate_iban(self, country: str) -> str:
        """Generate a dummy IBAN."""
        country_code = country
        check_digits = ''.join(random.choices('0123456789', k=2))
        bank_code = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))
        account_number = ''.join(random.choices('0123456789', k=10))
        return f"{country_code}{check_digits}{bank_code}{account_number}"
    
    def generate_pacs008(self) -> str:
        """Generate a pacs.008 message."""
        msg_id = self._generate_id("PACS008")
        created_dt = self._generate_datetime()
        amount, currency = self._generate_amount()
        
        debtor_bank_bic, debtor_bank_name = self._generate_bank_info()
        creditor_bank_bic, creditor_bank_name = self._generate_bank_info()
        
        debtor_country = random.choice(self.countries)
        creditor_country = random.choice(self.countries)
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10">
    <FIToFICstmrCdtTrf>
        <GrpHdr>
            <MsgId>{msg_id}</MsgId>
            <CreDtTm>{created_dt}</CreDtTm>
            <TtlIntrBkSttlmAmt Ccy="{currency}">{amount}</TtlIntrBkSttlmAmt>
        </GrpHdr>
        <CdtTrfTxInf>
            <DbtrAgt>
                <FinInstnId>
                    <BICFI>{debtor_bank_bic}</BICFI>
                </FinInstnId>
            </DbtrAgt>
            <CdtrAgt>
                <FinInstnId>
                    <BICFI>{creditor_bank_bic}</BICFI>
                </FinInstnId>
            </CdtrAgt>
            <Dbtr>
                <Nm>{debtor_bank_name} Client</Nm>
                <Id>
                    <PrvtId>
                        <Othr>
                            <Id>{self._generate_iban(debtor_country)}</Id>
                        </Othr>
                    </PrvtId>
                </Id>
            </Dbtr>
            <Cdtr>
                <Nm>{creditor_bank_name} Client</Nm>
                <Id>
                    <PrvtId>
                        <Othr>
                            <Id>{self._generate_iban(creditor_country)}</Id>
                        </Othr>
                    </PrvtId>
                </Id>
            </Cdtr>
        </CdtTrfTxInf>
    </FIToFICstmrCdtTrf>
</Document>"""
        
        # Format XML with proper indentation
        dom = minidom.parseString(xml_content)
        return dom.toprettyxml(indent="    ")
    
    def generate_pacs002(self) -> str:
        """Generate a pacs.002 message."""
        msg_id = self._generate_id("PACS002")
        created_dt = self._generate_datetime()
        orig_msg_id = self._generate_id("ORIG")
        status = random.choice(["ACCP", "ACSC", "ACSP", "RJCT"])
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.002.001.12">
    <FIToFIPmtStsRpt>
        <GrpHdr>
            <MsgId>{msg_id}</MsgId>
            <CreDtTm>{created_dt}</CreDtTm>
        </GrpHdr>
        <OrgnlGrpInfAndSts>
            <OrgnlMsgId>{orig_msg_id}</OrgnlMsgId>
            <OrgnlMsgNmId>pacs.008.001.10</OrgnlMsgNmId>
            <GrpSts>{status}</GrpSts>
        </OrgnlGrpInfAndSts>
    </FIToFIPmtStsRpt>
</Document>"""
        
        dom = minidom.parseString(xml_content)
        return dom.toprettyxml(indent="    ")
    
    def generate_camt053(self) -> str:
        """Generate a camt.053 message."""
        msg_id = self._generate_id("CAMT053")
        created_dt = self._generate_datetime()
        stmt_id = self._generate_id("STMT")
        account_id = self._generate_iban(random.choice(self.countries))
        balance_amount, balance_currency = self._generate_amount()
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.10">
    <BkToCstmrStmt>
        <GrpHdr>
            <MsgId>{msg_id}</MsgId>
            <CreDtTm>{created_dt}</CreDtTm>
        </GrpHdr>
        <Stmt>
            <Id>{stmt_id}</Id>
            <Acct>
                <Id>
                    <IBAN>{account_id}</IBAN>
                </Id>
            </Acct>
            <Bal>
                <Amt Ccy="{balance_currency}">{balance_amount}</Amt>
            </Bal>
        </Stmt>
    </BkToCstmrStmt>
</Document>"""
        
        dom = minidom.parseString(xml_content)
        return dom.toprettyxml(indent="    ")
    
    def generate_pain001(self) -> str:
        """Generate a pain.001 message."""
        msg_id = self._generate_id("PAIN001")
        created_dt = self._generate_datetime()
        amount, currency = self._generate_amount()
        execution_date = self._generate_datetime(days_offset=1)
        
        debtor_country = random.choice(self.countries)
        creditor_country = random.choice(self.countries)
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.11">
    <CstmrCdtTrfInitn>
        <GrpHdr>
            <MsgId>{msg_id}</MsgId>
            <CreDtTm>{created_dt}</CreDtTm>
            <InitgPty>
                <Nm>Initiating Company</Nm>
            </InitgPty>
        </GrpHdr>
        <PmtInf>
            <PmtInfId>{self._generate_id("PMT")}</PmtInfId>
            <PmtMtd>TRF</PmtMtd>
            <ReqdExctnDt>{execution_date}</ReqdExctnDt>
            <Dbtr>
                <Nm>Debtor Name</Nm>
            </Dbtr>
            <DbtrAcct>
                <Id>
                    <IBAN>{self._generate_iban(debtor_country)}</IBAN>
                </Id>
            </DbtrAcct>
            <CdtTrfTxInf>
                <PmtId>
                    <EndToEndId>{self._generate_id("E2E")}</EndToEndId>
                </PmtId>
                <Amt>
                    <InstdAmt Ccy="{currency}">{amount}</InstdAmt>
                </Amt>
                <Cdtr>
                    <Nm>Creditor Name</Nm>
                </Cdtr>
                <CdtrAcct>
                    <Id>
                        <IBAN>{self._generate_iban(creditor_country)}</IBAN>
                    </Id>
                </CdtrAcct>
            </CdtTrfTxInf>
        </PmtInf>
    </CstmrCdtTrfInitn>
</Document>"""
        
        dom = minidom.parseString(xml_content)
        return dom.toprettyxml(indent="    ")
    
    def generate_test_messages(self, count: int = 1, message_types: List[str] = None) -> List[str]:
        """Generate a list of test messages.
        
        Args:
            count: Number of messages to generate
            message_types: List of message types to generate. If None, generates random types.
            
        Returns:
            List of XML message strings
        """
        if message_types is None:
            message_types = ["pacs.008", "pacs.002", "camt.053", "pain.001"]
            
        messages = []
        for _ in range(count):
            msg_type = random.choice(message_types) if len(message_types) > 1 else message_types[0]
            
            if msg_type == "pacs.008":
                messages.append(self.generate_pacs008())
            elif msg_type == "pacs.002":
                messages.append(self.generate_pacs002())
            elif msg_type == "camt.053":
                messages.append(self.generate_camt053())
            elif msg_type == "pain.001":
                messages.append(self.generate_pain001())
                
        return messages 