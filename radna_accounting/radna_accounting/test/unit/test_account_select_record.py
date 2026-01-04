import pytest
import logging
import string
import random
from datetime import datetime, timezone
from ...models.chart_of_accounts import coa_meta
from ...validators.chart_of_accounts import (
    ChartOfAccountsModel
)
from ...core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore

from ..utils.db.connector import (
    SQLiteClient
)
from ..utils.helpers import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

creds = {
    "file_name": "temp_state.db"
}


class TestAccountSelectRecord:
    @pytest.mark.parametrize("param", ["byId", "byName"])
    def test_happy_path(self, generate_account_request_payload, param):
        DATA_KEY = 'data'
        core_model = ChartOfAccountsCore()
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID],
            "<coa_name>": payload[coa_meta.NAME],
            "<coa_type>": payload[coa_meta.TYPE],
            "<coa_description>": payload[coa_meta.DESCRIPTION],
            "<coa_created_date>": current_datetime,
            "<coa_updated_date>": current_datetime
        }
        core_method_map = {
            "byId": {
                "method": core_model.selectRecordById,
                "value": payload[coa_meta.ACCOUNT_ID]
            },
            "byName": {
                "method": core_model.selectRecordByName,
                "value": payload[coa_meta.NAME]
            }
        }

        core_model.insertRecord(payload)

        query_result = core_method_map[param]['method'](
            core_method_map[param]['value']
        )

        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

        for key in query_result[DATA_KEY].keys():   
            logging.info(f"assert field {key}: {result[key].iloc[0]} == {query_result[DATA_KEY][key]}")
            if 'date' in key:
                assert query_result[DATA_KEY][key] == datetime.strptime(result[key].iloc[0], "%Y-%m-%d %H:%M:%S.%f")
            else:
                assert query_result[DATA_KEY][key] == result[key].iloc[0]

    @pytest.mark.parametrize("param", ["byId", "byName"])
    def test_using_nonexistent_record_values(self, param):
            core_model = ChartOfAccountsCore()
            value = ''.join(random.choices(string.digits, k=6))
            core_method_map = {
                "byId": core_model.selectRecordById,
                "byName": core_model.selectRecordByName
            }
            query_result = core_method_map[param](value)
            assert query_result is None

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, None])
    def test_id_invalid_data_type(self, param):
            core_model = ChartOfAccountsCore()
            query_result = core_model.selectRecordById(param)
            assert query_result is None
    
    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, None])
    def test_name_invalid_data_type(self, param):
            core_model = ChartOfAccountsCore()
            query_result = core_model.selectRecordByName(param)
            assert query_result is None
            
        