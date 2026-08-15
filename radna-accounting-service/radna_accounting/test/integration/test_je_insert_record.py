# import pytest
# import uuid
# from datetime import date
# from datetime import datetime, timezone
# from radna_accounting.models.chart_of_accounts import *
# from radna_accounting.validators.journal_entry import (
#     JournalEntryModel
# )
# from radna_accounting.core.journal_entry.journal_entry import JournalEntryCore
# from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
# from radna_accounting.models.chart_of_accounts import coa_meta
# from radna_accounting.test.utils.db.connector import (
#     SQLiteClient
# )
# from radna_accounting.test.utils.helpers import *

# creds = {
#     "file_name": "temp_state.db"
# }

# class TestJEInsertRecord:
#     def test_happy_path(self):
#         core_model = JournalEntryCore()
#         current_datetime = datetime.now()
#         record = {
#             "id": uuid.uuid4(),
#             "transaction_id": "202412-00001",
#             "transaction_date": date.today(),
#             "currency_code": "PHP",
#             "status": "NEW",
#             "account_number": "000000000000000000000000000000",
#             "entry_type": "DEBIT",
#             "description": "",
#             "amount": 1,
#             "posting_date": None,
#             "created_date": current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}",
#             "updated_date": current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
#         }
#         core_model.insertRecord(record)
#         # result = core_model.selectRecordById(record['id'])
#         # record['transaction_id'] = "202412-00002"
#         # core_model.updateRecordById(record['id'], record)
#         # core_model.deleteRecordById(record['id'])
#         # print("^^^^^^^^^^^^^^^^^^^^")
#         # print(result)
#         # print("^^^^^^^^^^^^^^^^^^^^")
#         assert True is False
    