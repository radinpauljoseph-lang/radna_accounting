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
    Column('account_id', String(30), unique=True, nullable=False),
    Column('name', String(150), unique=True, nullable=False),
    Column('type', String(20), nullable=False),
    Column('description', String(300), nullable=True),
    Column('account_mapping', String(30), nullable=True),
    Column(
        'created_date',
        DateTime,
        nullable=False
    ),
    Column(
        'updated_date',
        DateTime,
        nullable=False
    ),
    schema=schema_string
)