import pytest
import logging
import string
import random
from datetime import datetime
from radna_accounting.validators.chart_of_accounts import (
    ChartOfAccountsModel
)
from radna_accounting.validators.data_model import DATA_KEY
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.test.data.chart_of_accounts import ChartOfAccountsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials
from radna_accounting.test.data.db.chart_of_accounts.queries import SelectChartOfAccountsByDetails
from radna_accounting.test.data.db.constants import SQL_TEXT_FIELD

class TestAccountSelectRecord:

    @pytest.mark.parametrize("param", ["byId", "byName"])
    def test_happy_path(self, param):
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)

        sql_query_details = SelectChartOfAccountsByDetails(
              coa_account_id=payload.account_id,
              coa_name=payload.name,
              coa_type=payload.type,
              coa_description=payload.description
        )

        core_method_map = {
            "byId": {
                "method": core_model.selectRecordById,
                "value": payload.account_id
            },
            "byName": {
                "method": core_model.selectRecordByName,
                "value": payload.name
            }
        }

        core_model.insertRecord(payload)

        query_result = core_method_map[param]['method'](
            core_method_map[param]['value']
        )

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

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
            
        