import uuid
from sqlalchemy import Table, Column, String, INT
from radna_accounting.configs.config import(
    CONFIGS,
    ENV,
    meta
)

schema_string = CONFIGS[f"{ENV}.database"]['schema'] if CONFIGS[f"{ENV}.database"]['schema'] != 'null' else None

class TransactionIdsMetaData:
    def __init__(self):
        self.TABLE_NAME = "transaction_ids"
        self.MONTH = "month"
        self.YEAR = "year"
        self.ID = "id"

        self.ID_LENGTH = 50

ti_meta = TransactionIdsMetaData()

transaction_ids = Table(
    ti_meta.TABLE_NAME,
    meta,
    Column(ti_meta.MONTH, INT, unique=False, nullable=False),
    Column(ti_meta.YEAR, INT, unique=False, nullable=False),
    Column(ti_meta.ID, String(ti_meta.ID_LENGTH), unique=False, nullable=False),
    schema=schema_string
)