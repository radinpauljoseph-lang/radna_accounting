import uuid
from sqlalchemy import Table, Column, String, DateTime, INT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from ..configs.config import(
    CONFIGS,
    ENV,
    meta
)

schema_string = CONFIGS[f"{ENV}.database"]['schema'] if CONFIGS[f"{ENV}.database"]['schema'] != 'null' else None

transaction_id_tracker = Table(
    "transaction_id_tracker",
    meta,
    Column('month', INT, unique=False, nullable=False),
    Column('year', INT, unique=False, nullable=False),
    Column('id', String(5), unique=False, nullable=False),
    schema=schema_string
)