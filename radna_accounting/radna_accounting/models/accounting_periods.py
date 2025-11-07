import uuid
from sqlalchemy import Table, Column, String, INT
from sqlalchemy.sql import text
from ..configs.config import(
    CONFIGS,
    ENV,
    meta
)

schema_string = CONFIGS[f"{ENV}.database"]['schema'] if CONFIGS[f"{ENV}.database"]['schema'] != 'null' else None
uuid_generator_keyword = text("gen_random_uuid()") if schema_string is not None else None
sqlite_default=lambda: uuid.uuid4()

accounting_periods = Table(
    "accounting_periods",
    meta,
    Column('year', INT, nullable=False),
    Column('month', INT, nullable=False),
    Column('status', String(15), nullable=False),
    schema=schema_string
)