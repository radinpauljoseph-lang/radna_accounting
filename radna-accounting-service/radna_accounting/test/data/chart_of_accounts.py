import pytest
import string
import random
from typing import Any
from faker import Faker
from datetime import datetime
from pydantic import BaseModel, model_validator, Field

from radna_accounting.validators.chart_of_accounts import account_types
fake = Faker()

class ChartOfAccountsPayloadGeneratorMetaData:
    def __init__(self):
        self.IS_CREATED_DATE_INCLUDED = "is_created_date_included"
        self.IS_UPDATED_DATE_UNCLUDED = "is_updated_date_included"
        self.IS_DATES_INCLUDED = "is_dates_included"
        self.CREATED_DATE = "created_date"
        self.UPDATED_DATE = "updated_date"

coa_payload_meta = ChartOfAccountsPayloadGeneratorMetaData()

class ChartOfAccountsPayloadGenerator(BaseModel):
    account_id: Any = Field(default_factory=lambda: ''.join(random.choices(string.digits, k=6)))
    name: Any = Field(default_factory=lambda: fake.bs())
    type: Any = Field(default_factory=lambda: account_types[random.randrange(0, len(account_types))])
    description: Any = Field(default_factory=lambda: fake.bs())
    account_mapping: Any = None
    created_date: datetime | str = None
    updated_date: datetime | str = None
    is_dates_included: bool | None = False

    @model_validator(mode="before")
    def include_dates(cls, values):
        if coa_payload_meta.IS_DATES_INCLUDED in values.keys():
            if values[coa_payload_meta.IS_DATES_INCLUDED] is True:
                current_datetime = datetime.now()
                values[coa_payload_meta.CREATED_DATE] = current_datetime
                values[coa_payload_meta.UPDATED_DATE] = current_datetime
        return values
    
class ChartOfAccountsUpdatePayloadGenerator(BaseModel):
    name: Any = None
    type: Any = None
    description: Any = None
    account_mapping: Any = None


