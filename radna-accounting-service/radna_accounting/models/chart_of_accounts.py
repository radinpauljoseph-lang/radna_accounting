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

        self.ACCOUNT_ID_LENGTH = 30
        self.ACCOUNT_ID_MIN_LENGTH = 5
        self.NAME_LENGTH = 150
        self.DESCRIPTION_LENGTH = 300

    def getColumnsAsList(self):
        col = [
            self.ACCOUNT_ID,
            self.NAME,
            self.TYPE,
            self.DESCRIPTION,
            self.ACCOUNT_MAPPING,
            self.CREATED_DATE,
            self.UPDATED_DATE
        ]
        return col

class AccountTypes:
    def __init__(self):
        self.ASSET = "ASSET"
        self.LIABILITY = "LIABILITY"
        self.EQUITY = "EQUITY"
        self.REVENUE = "REVENUE"
        self.EXPENSES = "EXPENSES"
        self.COST = "COST"

    def getTypesAsList(self):
        account_types = [
            self.ASSET,
            self.LIABILITY,
            self.EQUITY,
            self.REVENUE,
            self.EXPENSES,
            self.COST
        ]
        return account_types

coa_meta = ChartOfAccountTableMetaData()
coa_types = AccountTypes()

schema_string = CONFIGS[f"{ENV}.database"]['schema'] if CONFIGS[f"{ENV}.database"]['schema'] != 'null' else None
uuid_generator_keyword = text("gen_random_uuid()") if schema_string is not None else None
sqlite_default=lambda: uuid.uuid4()

chart_of_accounts = Table(
    coa_meta.TABLE_NAME,
    meta,
    Column(coa_meta.ACCOUNT_ID, String(coa_meta.ACCOUNT_ID_LENGTH), unique=True, nullable=False),
    Column(coa_meta.NAME, String(coa_meta.NAME_LENGTH), unique=True, nullable=False),
    Column(coa_meta.TYPE, String(20), nullable=False),
    Column(coa_meta.DESCRIPTION, String(coa_meta.DESCRIPTION_LENGTH), nullable=True),
    Column(coa_meta.ACCOUNT_MAPPING, String(coa_meta.ACCOUNT_ID_LENGTH), nullable=True),
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