import uuid
from sqlalchemy import Table, Column, String, Date, DateTime, FLOAT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from ..configs.config import(
    CONFIGS,
    ENV,
    meta
)

schema_string = CONFIGS[f"{ENV}.database"]['schema'] if CONFIGS[f"{ENV}.database"]['schema'] != 'null' else None
uuid_generator_keyword = text("gen_random_uuid()") if schema_string is not None else None
sqlite_default=lambda: uuid.uuid4()

journal_entry_history = Table(
    "journal_entry_history",
    meta,
    Column(
        'id',
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=uuid_generator_keyword,  # uses pgcrypto
        default=sqlite_default  if schema_string is None else None
    ),
    Column('transaction_id', String(30), unique=False, nullable=False),
    Column(
        'transaction_date',
        Date,
        nullable=False
    ),
    Column('account_number', String(30), unique=False, nullable=False),
    Column('entry_type', String(12), unique=False, nullable=False),
    Column('description', String(50), unique=False, nullable=False),
    Column('amount', FLOAT, nullable=False),
    Column('currency_code', String(3), nullable=False),
    Column(
        'posting_date',
        Date,
        nullable=True
    ),
    Column('status', String(15), unique=False, nullable=False),
    Column(
        'created_date',
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")  # auto-generate timestamp
    ),
    Column(
        'updated_date',
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")  # auto-generate timestamp
    ),
    Column(
        'history_id',
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=uuid_generator_keyword,  # uses pgcrypto
        default=sqlite_default  if schema_string is None else None
    ),
    Column(
        'history_date',
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")  # auto-generate timestamp
    ),
    schema=schema_string
)