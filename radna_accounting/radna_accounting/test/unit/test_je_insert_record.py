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
        record = {
            "id": uuid.uuid4(),
            "transaction_id": "202412-00001",
            "transaction_date": date.today(),
            "account_number": "000000000000000000000000000000"
        }
        print("&&&&&&&&&&&&&&&")
        print(record)
        print("&&&&&&&&&&&&&&&")
        payload = JournalEntryModel(**record).model_dump()
        print(payload)
        assert True is False
    