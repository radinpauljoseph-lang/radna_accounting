import pytest
import uuid
from datetime import date
from datetime import datetime, timezone
from ...models.chart_of_accounts import *
from ...validators.journal_entry import (
    JournalEntryModel
)
from ...core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from ...models.chart_of_accounts import coa_meta
from ..utils.db.connector import (
    SQLiteClient
)
from ..utils.helpers import *

creds = {
    "file_name": "temp_state.db"
}

class TestJEInsertRecord:
    def test_happy_path(self):
        current_datetime = datetime.now()
        record = {
            "id": uuid.uuid4(),
            "transaction_id": "202412-00001",
            "transaction_date": "2024-02-29",
            "currency_code": "PHP",
            "status": "NEW",
            "account_number": "000000000000000000000000000000",
            "entry_type": "DEBIT",
            "description": "",
            "amount": 1,
            "posting_date": date.today(),
            "created_date": current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}",
            "updated_date": current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        }
        print("&&&&&&&&&&&&&&&")
        print(record)
        print("&&&&&&&&&&&&&&&")
        payload = JournalEntryModel(**record).model_dump()
        payload = payload
        print(payload)
        assert True is False
    