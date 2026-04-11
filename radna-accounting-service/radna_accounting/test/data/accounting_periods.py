import string
import random
from datetime import datetime
from typing import Any
from pydantic import BaseModel, model_validator, Field

from radna_accounting.models.accounting_periods import acp_meta
class AccountingPeriodsPayloadGenerator(BaseModel):
    month: Any = 1
    year: Any = 1000

    @model_validator(mode="before")
    def month_year_generator(cls, values):
        if acp_meta.MONTH not in values.keys() and acp_meta.YEAR not in values.keys():
            now = datetime.now()
            current_year = now.year
            current_month = now.month

            values[acp_meta.YEAR] = random.randint(1000, current_year)

            if values[acp_meta.YEAR] == current_year:
                values[acp_meta.MONTH] = random.randint(1, current_month)
            else:
                values[acp_meta.MONTH] = random.randint(1, 12)

        return values