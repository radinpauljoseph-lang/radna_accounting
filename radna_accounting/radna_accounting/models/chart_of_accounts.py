import uuid
from sqlalchemy import Table, Column, String, DateTime
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

chart_of_accounts = Table(
    "chart_of_accounts",
    meta,
    Column(
        'id',
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=uuid_generator_keyword,  # uses pgcrypto
        default=sqlite_default  if schema_string is None else None
    ),
    Column('account_id', String(30), unique=True, nullable=False),
    Column('name', String(50), unique=True, nullable=False),
    Column('type', String(20), nullable=False),
    Column('description', String(50), nullable=True),
    Column('account_mapping', String(30), nullable=True),
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
    schema=schema_string
)