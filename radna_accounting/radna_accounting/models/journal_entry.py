import uuid
from sqlalchemy import Table, Column, String, Date, DateTime, FLOAT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from ..configs.config import(
    CONFIGS,
    ENV,
    meta
)

class JournalEntryTableMetaData:
    def __init__(self):
        self.TABLE_NAME = "journal_entry"
        self.ID = "id"
        self.TRANSACTION_ID = "transaction_id"
        self.TRANSACTION_DATE = "transaction_date"
        self.ACCOUNT_NUMBER = "account_number"
        self.ENTRY_TYPE = "entry_type"
        self.DESCRIPTION = "description"
        self.AMOUNT = "amount"
        self.CURRENCY_CODE = "currency_code"
        self.POSTING_DATE = "posting_date"
        self.STATUS = "status"
        self.CREATED_DATE = "created_date"
        self.UPDATED_DATE = "updated_date"

class JournalEntryStatuses:
    def __init__(self):
        self.NEW = "NEW"
        self.POSTED = "POSTED"
        self.REJECTED = "REJECTED"
        self.APPROVED = "APPROVED"

class JournalEntryTypes():
    def __init__(self):
        self.CREDIT = "CREDIT"
        self.DEBIT = "DEBIT"

je_meta = JournalEntryTableMetaData()
je_status = JournalEntryStatuses()
je_types = JournalEntryTypes()

schema_string = CONFIGS[f"{ENV}.database"]['schema'] if CONFIGS[f"{ENV}.database"]['schema'] != 'null' else None
uuid_generator_keyword = text("gen_random_uuid()") if schema_string is not None else None
sqlite_default=lambda: uuid.uuid4()

journal_entry = Table(
    je_meta.TABLE_NAME,
    meta,
    Column(
        je_meta.ID,
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=uuid_generator_keyword,  # uses pgcrypto
        default=sqlite_default  if schema_string is None else None
    ),
    Column(je_meta.TRANSACTION_ID, String(30), unique=False, nullable=False),
    Column(
        je_meta.TRANSACTION_DATE,
        Date,
        nullable=False
    ),
    Column(je_meta.ACCOUNT_NUMBER, String(30), unique=False, nullable=False),
    Column(je_meta.ENTRY_TYPE, String(12), unique=False, nullable=False),
    Column(je_meta.DESCRIPTION, String(50), unique=False, nullable=False),
    Column(je_meta.AMOUNT, FLOAT, nullable=False),
    Column(je_meta.CURRENCY_CODE, String(3), nullable=False),
    Column(
        je_meta.POSTING_DATE,
        Date,
        nullable=True
    ),
    Column(je_meta.STATUS, String(15), unique=False, nullable=False),
    Column(
        je_meta.CREATED_DATE,
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")  # auto-generate timestamp
    ),
    Column(
        je_meta.UPDATED_DATE,
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")  # auto-generate timestamp
    ),
    schema=schema_string
)