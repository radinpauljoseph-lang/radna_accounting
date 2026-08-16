import pytest
from faker import Faker
from datetime import datetime
from radna_accounting.validators.chart_of_accounts import ChartOfAccountsModel
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.models.chart_of_accounts import coa_types
from radna_accounting.test.data.chart_of_accounts import ChartOfAccountsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials
from radna_accounting.test.data.db.chart_of_accounts.queries import (
    SelectChartOfAccountsByDetails,
    SelectChartOfAccountsByDetailsDescriptionIsNull
)
from radna_accounting.test.data.db.constants import SQL_TEXT_FIELD
class TestAccounUpdateRecord:
    def test_happy_path_update_name(self):
        account_name = Faker().bs()
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)

        sql_query_details = SelectChartOfAccountsByDetails(
            coa_account_id=payload.account_id,
            coa_name=account_name,
            coa_type=payload.type,
            coa_description=payload.description
        )

        core_model.insertRecord(payload)
        
        payload.name = account_name
        core_model.updateRecordById(payload.account_id, payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

        assert result.shape[0] == 1
    
    def test_happy_path_update_description_none(self):
        account_description = Faker().bs()
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator(
            description=account_description
        ).model_dump()
        payload = ChartOfAccountsModel(**payload)

        sql_query_details = SelectChartOfAccountsByDetailsDescriptionIsNull(
            coa_account_id=payload.account_id,
            coa_name=payload.name,
            coa_type=payload.type
        )

        core_model.insertRecord(payload)

        payload.description = None
        core_model.updateRecordById(payload.account_id, payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

        assert result.shape[0] == 1

    def test_happy_path_update_description(self):
        account_description = Faker().bs()
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)

        sql_query_details = SelectChartOfAccountsByDetails(
            coa_account_id=payload.account_id,
            coa_name=payload.name,
            coa_type=payload.type,
            coa_description=account_description
        )

        core_model.insertRecord(payload)

        payload.description = account_description
        core_model.updateRecordById(payload.account_id, payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

        assert result.shape[0] == 1

    @pytest.mark.parametrize("param", [coa_types.ASSET, coa_types.LIABILITY, coa_types.EQUITY, coa_types.LIABILITY, coa_types.REVENUE, coa_types.COST])
    def test_happy_path_update_account_type(self, param):
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)

        sql_query_details = SelectChartOfAccountsByDetails(
            coa_account_id=payload.account_id,
            coa_name=payload.name,
            coa_type=param,
            coa_description=payload.description
        )
        
        core_model.insertRecord(payload)

        payload.type = param
        core_model.updateRecordById(payload.account_id, payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

        assert result.shape[0] == 1

    def test_duplicate_name_error(self):
        expected = "UNIQUE constraint failed"
        core_model = ChartOfAccountsCore()
        first_record = None
        second_record = None

        for index in range(2):
            payload = ChartOfAccountsPayloadGenerator().model_dump()
            payload = ChartOfAccountsModel(**payload)
            core_model.insertRecord(payload)
            if index == 0:
                first_record = payload
            else:
                second_record = payload

        second_record.name = first_record.name

        with pytest.raises(Exception) as excinfo:
            core_model.updateRecordById(second_record.account_id, second_record)
        assert expected in str(excinfo)

    def test_using_nonexistent_record_value(self):
            expected = "COA0101"
            core_model = ChartOfAccountsCore()
            payload = ChartOfAccountsPayloadGenerator().model_dump()
            payload = ChartOfAccountsModel(**payload)
            
            with pytest.raises(Exception) as excinfo:
                core_model.updateRecordById(payload.account_id, payload)
            assert expected in str(excinfo)

