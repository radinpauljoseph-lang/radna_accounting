import uuid
from sqlalchemy import Table, Column, String, Date, DateTime, FLOAT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from .chart_of_accounts import coa_meta
from .journal_entry import je_meta
from ..configs.config import(
    CONFIGS,
    ENV,
    meta
)

class JournalVoucherTableMetaData:
    def __init__(self):
        self.TABLE_NAME = "journal_voucher"
        self.HISTORY_TABLE_NAME = "journal_voucher_history"
        self.ID = "id"
        self.TRANSACTION_ID = 'transaction_id'
        self.DOCUMENT_NAME = 'document_name'
        self.DOCUMENT_PATH = 'document_path'
        self.DOCUMENT_FILE_TYPE = 'document_file_type'
        self.SIGNED_DOCUMENT_NAME = 'signed_document_name'
        self.SIGNED_DOCUMENT_PATH = 'signed_document_path'
        self.SIGNED_DOCUMENT_FILE_TYPE = 'signed_document_file_type'
        self.CREATED_DATE = "created_date"
        self.UPDATED_DATE = "updated_date"

        self.DOCUMENT_NAME_LENGTH = 255
        self.DOCUMENT_PATH_LENGTH = 500
        self.DOCUMENT_FILE_TYPE_LENGTH = 10
        self.SIGNED_DOCUMENT_NAME_LENGTH = 255
        self.SIGNED_DOCUMENT_PATH_LENGTH = 500
        self.SIGNED_DOCUMENT_FILE_TYPE_LENGTH = 10

        self.HISTORY_ID = "history_id"
        self.HISTORY_DATE = "history_date"
        self.HISTORY_OPERATION = "history_operation"

schema_string = CONFIGS[f"{ENV}.database"]['schema'] if CONFIGS[f"{ENV}.database"]['schema'] != 'null' else None
uuid_generator_keyword = text("gen_random_uuid()") if schema_string is not None else None
sqlite_default=lambda: uuid.uuid4()

jv_meta = JournalVoucherTableMetaData()

journal_voucher = Table(
    jv_meta.TABLE_NAME,
    meta,
    Column(
        jv_meta.ID, UUID(as_uuid=True), primary_key=True, unique=True, nullable=False),
    Column(jv_meta.TRANSACTION_ID, String(je_meta.TRANSACTION_ID_LENGTH), unique=False, nullable=False),
    Column(jv_meta.DOCUMENT_NAME, String(jv_meta.DOCUMENT_NAME_LENGTH), unique=False, nullable=False),
    Column(jv_meta.DOCUMENT_PATH, String(jv_meta.DOCUMENT_PATH_LENGTH), unique=False, nullable=False),
    Column(jv_meta.DOCUMENT_FILE_TYPE, String(jv_meta.DOCUMENT_FILE_TYPE_LENGTH), unique=False, nullable=False),
    Column(jv_meta.SIGNED_DOCUMENT_NAME, String(jv_meta.DOCUMENT_NAME_LENGTH), unique=False, nullable=True),
    Column(jv_meta.SIGNED_DOCUMENT_PATH, String(jv_meta.SIGNED_DOCUMENT_PATH_LENGTH), unique=False, nullable=True),
    Column(jv_meta.SIGNED_DOCUMENT_FILE_TYPE, String(jv_meta.SIGNED_DOCUMENT_FILE_TYPE_LENGTH), unique=False, nullable=True),
    # add docs columns here
    Column(
        jv_meta.CREATED_DATE,
        DateTime,
        nullable=False
    ),
    Column(
        jv_meta.UPDATED_DATE,
        DateTime,
        nullable=False
    ),
    schema=schema_string
)

journal_voucher_history = Table(
    jv_meta.HISTORY_TABLE_NAME,
    meta,
    Column(
        jv_meta.ID, UUID(as_uuid=True), primary_key=True, unique=True, nullable=False),
    Column(jv_meta.TRANSACTION_ID, String(je_meta.TRANSACTION_ID_LENGTH), unique=False, nullable=False),
    Column(jv_meta.DOCUMENT_NAME, String(jv_meta.DOCUMENT_NAME_LENGTH), unique=False, nullable=False),
    Column(jv_meta.DOCUMENT_PATH, String(jv_meta.DOCUMENT_PATH_LENGTH), unique=False, nullable=False),
    Column(jv_meta.DOCUMENT_FILE_TYPE, String(jv_meta.DOCUMENT_FILE_TYPE_LENGTH), unique=False, nullable=False),
    Column(jv_meta.SIGNED_DOCUMENT_NAME, String(jv_meta.DOCUMENT_NAME_LENGTH), unique=False, nullable=True),
    Column(jv_meta.SIGNED_DOCUMENT_PATH, String(jv_meta.SIGNED_DOCUMENT_PATH_LENGTH), unique=False, nullable=True),
    Column(jv_meta.SIGNED_DOCUMENT_FILE_TYPE, String(jv_meta.SIGNED_DOCUMENT_FILE_TYPE_LENGTH), unique=False, nullable=True),
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