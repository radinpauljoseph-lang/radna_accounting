import pytest
from faker import Faker
import logging
from datetime import datetime, timezone
from radna_accounting.models.chart_of_accounts import *
from radna_accounting.validators.chart_of_accounts import (
    ChartOfAccountsModel,
    account_types
)
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.models.chart_of_accounts import (
    coa_meta,
    coa_types
)

from radna_accounting.test.utils.db.connector import (
    SQLiteClient
)
from radna_accounting.test.utils.helpers import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


creds = {
    "file_name": "temp_state.db"
}

class TestAccountDeleteRecord:
    def test_happy_path(self, generate_account_request_payload):
        core_model = ChartOfAccountsCore()
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"

        core_model.insertRecord(payload)
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID],
            "<coa_name>": payload[coa_meta.NAME],
            "<coa_type>": payload[coa_meta.TYPE],
            "<coa_description>": payload[coa_meta.DESCRIPTION],
            "<coa_created_date>": current_datetime,
            "<coa_updated_date>": current_datetime
        }
        core_model.deleteRecordById(payload[coa_meta.ACCOUNT_ID])

        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 0
