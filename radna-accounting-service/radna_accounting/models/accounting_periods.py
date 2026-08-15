import uuid
from sqlalchemy import Table, Column, String, INT, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from radna_accounting.configs.config import(
    CONFIGS,
    ENV,
    meta
)

schema_string = CONFIGS[f"{ENV}.database"]['schema'] if CONFIGS[f"{ENV}.database"]['schema'] != 'null' else None
uuid_generator_keyword = text("gen_random_uuid()") if schema_string is not None else None
sqlite_default=lambda: uuid.uuid4()

class AccountPeriodsMetaData:
    def __init__(self):
        self.TABLE_NAME = "accounting_periods"
        self.HISTORY_TABLE_NAME = "accounting_periods_history"
        self.YEAR = "year"
        self.MONTH = "month"
        self.STATUS = "status"
        self.CREATED_DATE = "created_date"
        self.UPDATED_DATE = "updated_date"

        self.HISTORY_ID = "history_id"
        self.HISTORY_DATE = "history_date"
        self.HISTORY_OPERATION = "history_operation"


class AccountPeriodStatuses:
    def __init__(self):
        self.OPEN = "OPEN"
        self.CLOSED = "CLOSED"
    
    def getStatusAsList(self):
        statuses = [
            self.OPEN,
            self.CLOSED
        ]
        return statuses
    
acp_meta = AccountPeriodsMetaData()
acp_status =AccountPeriodStatuses()

accounting_periods = Table(
    acp_meta.TABLE_NAME,
    meta,
    Column(acp_meta.YEAR, INT, nullable=False),
    Column(acp_meta.MONTH, INT, nullable=False),
    Column(acp_meta.STATUS, String(15), nullable=False),
    Column(
        acp_meta.CREATED_DATE,
        DateTime,
        nullable=False
    ),
    Column(
        acp_meta.UPDATED_DATE,
        DateTime,
        nullable=False
    ),
    schema=schema_string
)

accounting_periods_history = Table(
    acp_meta.HISTORY_TABLE_NAME,
    meta,
    Column(acp_meta.YEAR, INT, nullable=False),
    Column(acp_meta.MONTH, INT, nullable=False),
    Column(acp_meta.STATUS, String(15), nullable=False),
    Column(acp_meta.HISTORY_ID, UUID(as_uuid=True), primary_key=True, unique=True, nullable=False),
    Column(
        acp_meta.HISTORY_DATE,
        DateTime,
        nullable=False
    ),
    Column(acp_meta.HISTORY_OPERATION, String(1), unique=False, nullable=False),
    Column(
        acp_meta.CREATED_DATE,
        DateTime,
        nullable=False
    ),
    Column(
        acp_meta.UPDATED_DATE,
        DateTime,
        nullable=False
    ),
    schema=schema_string
)