import uuid
from sqlalchemy import Table, Column, String, DateTime
from sqlalchemy.sql import text
from ..configs.config import(
    CONFIGS,
    ENV,
    meta
)

class ChartOfAccountTableMetaData:
    def __init__(self):
        self.TABLE_NAME = "chart_of_accounts"
        self.ACCOUNT_ID = "account_id"
        self.NAME = "name"
        self.TYPE = "type"
        self.DESCRIPTION = "description"
        self.ACCOUNT_MAPPING ="account_mapping"
        self.CREATED_DATE = "created_date"
        self.UPDATED_DATE = "updated_date"

class AccountTypes:
    def __init__(self):
        self.ASSET = "ASSET"
        self.LIABILITY = "LIABILITY"
        self.EQUITY = "EQUITY"
        self.REVENUE = "REVENUE"
        self.EXPENSES = "EXPENSES"

coa_meta = ChartOfAccountTableMetaData()
coa_types = AccountTypes()

schema_string = CONFIGS[f"{ENV}.database"]['schema'] if CONFIGS[f"{ENV}.database"]['schema'] != 'null' else None
uuid_generator_keyword = text("gen_random_uuid()") if schema_string is not None else None
sqlite_default=lambda: uuid.uuid4()

chart_of_accounts = Table(
    coa_meta.TABLE_NAME,
    meta,
    Column(coa_meta.ACCOUNT_ID, String(30), unique=True, nullable=False),
    Column(coa_meta.NAME, String(150), unique=True, nullable=False),
    Column(coa_meta.TYPE, String(20), nullable=False),
    Column(coa_meta.DESCRIPTION, String(300), nullable=True),
    Column(coa_meta.ACCOUNT_MAPPING, String(30), nullable=True),
    Column(
        coa_meta.CREATED_DATE,
        DateTime,
        nullable=False
    ),
    Column(
        coa_meta.UPDATED_DATE,
        DateTime,
        nullable=False
    ),
    schema=schema_string
)