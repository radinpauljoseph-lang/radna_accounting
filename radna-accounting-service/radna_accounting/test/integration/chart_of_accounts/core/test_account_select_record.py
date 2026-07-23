import pytest
import logging
import string
import random
from datetime import datetime, timezone
from radna_accounting.models.chart_of_accounts import coa_meta
from radna_accounting.validators.chart_of_accounts import (
    ChartOfAccountsModel
)
from radna_accounting.validators.data_model import DATA_KEY
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.test.data.chart_of_accounts import ChartOfAccountsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient

creds = {
    "database": "temp_state.db"
}


class TestAccountSelectRecord:

    @pytest.mark.parametrize("param", ["byId", "byName"])
    def test_happy_path(self, param):
        core_model = ChartOfAccountsCore()
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        where_clause_values = {
            "coa_account_id": payload.account_id,
            "coa_name": payload.name,
            "coa_type": payload.type,
            "coa_description": payload.description,
            "coa_account_mapping": "",
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        }
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

        db_obj = SQLiteClient(creds)\
            .connect(creds)\
            .setCommand(f"""
            SELECT
                account_id, 
                name,
                type,
                description, 
                account_mapping, 
                created_date, 
                updated_date
            FROM chart_of_accounts
            WHERE 1=1
            AND account_id = :coa_account_id
            AND name = :coa_name
            AND type = :coa_type
            AND description = :coa_description
            AND (
                account_mapping IS NULL
                OR (
                    account_mapping IS NOT NULL
                    AND account_mapping = :coa_account_mapping
                )
            )
            AND created_date >= :coa_created_date
            AND updated_date >= :coa_updated_date
        """
        )\
        .execute(where_clause_values)

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
            
        