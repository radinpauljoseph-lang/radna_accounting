# import pytest
# # import radna_accounting as my_package
# from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
# from radna_accounting.validators.chart_of_accounts import (
#     account_types
# )

# from unittest.mock import MagicMock, patch

# from faker import Faker
# import uuid
# import string
# import random
# import copy
# from datetime import datetime, timezone

# class TestAccountInsertRecord:
    
#     def test_insert_record(self, mock_chart):
#         # from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore

#         fake = Faker()
#         current_datetime = datetime.now(timezone.utc)
#         mock_data = {
#             "account_id": ''.join(random.choices(string.digits, k=6)),
#             "name": fake.bs(),
#             "type": account_types[random.randrange(0, len(account_types))],
#             "description": fake.bs(),
#             "account_mapping": None,
#             "created_date": current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}",
#             "updated_date": current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
#         }
#         core_model = ChartOfAccountsCore()
#         mock_insert = MagicMock()
#         mock_chart.insert.return_value = mock_insert
#         core_model.insertRecord(mock_data)
#         assert 1 == 0