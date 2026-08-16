import pytest
from datetime import datetime

from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials
from radna_accounting.validators.chart_of_accounts import ChartOfAccountsModel
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.test.data.chart_of_accounts import ChartOfAccountsPayloadGenerator
from radna_accounting.test.data.db.chart_of_accounts.queries import SelectChartOfAccountsByDetails
from radna_accounting.test.data.db.constants import SQL_TEXT_FIELD

class TestAccountInsertRecord:

    def test_happy_path(self):
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)

        sql_query_details = SelectChartOfAccountsByDetails(
            coa_account_id=payload.account_id,
            coa_name=payload.name,
            coa_type=payload.type,
            coa_description=payload.description
        )
        
        core_model.insertRecord(payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

        assert result.shape[0] == 1

    def test_duplicate_record_error(self):
        expected = "UNIQUE constraint failed"
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)

        sql_query_details = SelectChartOfAccountsByDetails(
            coa_account_id=payload.account_id,
            coa_name=payload.name,
            coa_type=payload.type,
            coa_description=payload.description
        )
        
        core_model.insertRecord(payload)
        with pytest.raises(Exception) as excinfo:
            core_model.insertRecord(payload)
        assert expected in str(excinfo)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

        assert result.shape[0] == 1


        