import uuid
from sqlalchemy import Table, Column, String, Date, DateTime, FLOAT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from .chart_of_accounts import coa_meta
from ..configs.config import(
    CONFIGS,
    ENV,
    meta
)

class JournalEntryTableMetaData:
    def __init__(self):
        self.TABLE_NAME = "journal_entry"
        self.HISTORY_TABLE_NAME = "journal_entry_history"
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

        self.TRANSACTION_ID_LENGTH = 30
        self.CURRENCY_CODE_LENGTH = 3
        self.STATUS_LENGTH = 15
        self.DESCRIPTION_LENGTH = 300

        self.HISTORY_ID = "history_id"
        self.HISTORY_DATE = "history_date"
        self.HISTORY_OPERATION = "history_operation"

class JournalEntryStatuses:
    def __init__(self):
        self.NEW = "NEW"
        self.POSTED = "POSTED"
        self.REJECTED = "REJECTED"
        self.APPROVED = "APPROVED"

    def getStatusAsList(self):
        statuses = [
            self.NEW,
            self.POSTED,
            self.REJECTED,
            self.APPROVED
        ]
        return statuses

class JournalEntryTypes():
    def __init__(self):
        self.CREDIT = "CREDIT"
        self.DEBIT = "DEBIT"

    def getEntryTypesAsList(self):
        entry_types = [
            self.CREDIT,
            self.DEBIT
        ]
        return entry_types

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
        je_meta.ID, UUID(as_uuid=True), primary_key=True, unique=True, nullable=False),
    Column(je_meta.TRANSACTION_ID, String(je_meta.TRANSACTION_ID_LENGTH), unique=False, nullable=False),
    Column(
        je_meta.TRANSACTION_DATE,
        Date,
        nullable=False
    ),
    Column(je_meta.CURRENCY_CODE, String(je_meta.CURRENCY_CODE_LENGTH), nullable=False),
    Column(je_meta.STATUS, String(je_meta.STATUS_LENGTH), unique=False, nullable=False),
    Column(je_meta.ACCOUNT_NUMBER, String(coa_meta.ACCOUNT_ID_LENGTH), unique=False, nullable=False),
    Column(je_meta.ENTRY_TYPE, String(15), unique=False, nullable=False),
    Column(je_meta.DESCRIPTION, String(je_meta.DESCRIPTION_LENGTH), nullable=True),
    Column(je_meta.AMOUNT, FLOAT, nullable=False),
    Column(
        je_meta.POSTING_DATE,
        Date,
        nullable=True
    ),
    Column(
        je_meta.CREATED_DATE,
        DateTime,
        nullable=False
    ),
    Column(
        je_meta.UPDATED_DATE,
        DateTime,
        nullable=False
    ),
    schema=schema_string
)

journal_entry_history = Table(
    je_meta.HISTORY_TABLE_NAME,
    meta,
    Column(je_meta.ID, UUID(as_uuid=True), primary_key=False, unique=False, nullable=False),
    Column(je_meta.TRANSACTION_ID, String(je_meta.TRANSACTION_ID_LENGTH), unique=False, nullable=False),
    Column(
        je_meta.TRANSACTION_DATE,
        Date,
        nullable=False
    ),
    Column(je_meta.CURRENCY_CODE, String(je_meta.CURRENCY_CODE_LENGTH), nullable=False),
    Column(je_meta.STATUS, String(je_meta.STATUS_LENGTH), unique=False, nullable=False),
    Column(je_meta.ACCOUNT_NUMBER, String(coa_meta.ACCOUNT_ID_LENGTH), unique=False, nullable=False),
    Column(je_meta.ENTRY_TYPE, String(15), unique=False, nullable=False),
    Column(je_meta.DESCRIPTION, String(je_meta.DESCRIPTION_LENGTH), unique=False, nullable=True),
    Column(je_meta.AMOUNT, FLOAT, nullable=False),
    Column(
        je_meta.POSTING_DATE,
        Date,
        nullable=True
    ),
    Column(je_meta.HISTORY_ID, UUID(as_uuid=True), primary_key=True, unique=True, nullable=False),
    Column(
        je_meta.HISTORY_DATE,
        DateTime,
        nullable=False
    ),
    Column(je_meta.HISTORY_OPERATION, String(1), unique=False, nullable=False),
    Column(
        je_meta.CREATED_DATE,
        DateTime,
        nullable=False
    ),
    Column(
        je_meta.UPDATED_DATE,
        DateTime,
        nullable=False
    ),
    schema=schema_string
)