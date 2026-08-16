import pytest
from faker import Faker
import string
import random
from radna_accounting.controller.chart_of_accounts import ChartOfAccountsController
from radna_accounting.models.chart_of_accounts import (
    coa_meta,
    coa_types
)
from radna_accounting.test.data.chart_of_accounts import ChartOfAccountsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials
from radna_accounting.test.data.db.chart_of_accounts.queries import (
    SelectChartOfAccountsByDetails,
    SelectChartOfAccountsByDetailsDescriptionIsNull,
    SelectChartOfAccountsByAccountId,
    SelectChartOfAccountsByName
)
from radna_accounting.test.data.db.constants import SQL_TEXT_FIELD

class TestChartOfAccountsControllerCreateAccount:

    def test_happy_path(self):
        payload = ChartOfAccountsPayloadGenerator(
            description=None,
            is_dates_included=False
        ).model_dump(exclude=[coa_meta.CREATED_DATE, coa_meta.UPDATED_DATE])

        sql_query_details = SelectChartOfAccountsByDetailsDescriptionIsNull(
            coa_account_id=payload[coa_meta.ACCOUNT_ID],
            coa_name=payload[coa_meta.NAME],
            coa_type=payload[coa_meta.TYPE]
        )

        ChartOfAccountsController().createAccount(payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

        assert result.shape[0] == 1

    def test_happy_path_with_account_mapping(self):
        payload = ChartOfAccountsPayloadGenerator(
            description=None,
            is_dates_included=False
            ).model_dump(exclude=[coa_meta.CREATED_DATE, coa_meta.UPDATED_DATE])

        ChartOfAccountsController().createAccount(payload)
        
        payload = ChartOfAccountsPayloadGenerator(
            account_mapping=payload[coa_meta.ACCOUNT_ID], 
            is_dates_included=False
        ).model_dump(exclude=[coa_meta.CREATED_DATE, coa_meta.UPDATED_DATE])

        sql_query_details = SelectChartOfAccountsByDetails(
            coa_account_id=payload[coa_meta.ACCOUNT_ID],
            coa_name=payload[coa_meta.NAME],
            coa_type=payload[coa_meta.TYPE],
            coa_description=payload[coa_meta.DESCRIPTION],
            coa_account_mapping=payload[coa_meta.ACCOUNT_MAPPING]
        )

        ChartOfAccountsController().createAccount(payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

        assert result.shape[0] == 1
    
    def test_happy_path_with_description(self):
        payload = ChartOfAccountsPayloadGenerator(
            description=Faker().bs(),
            is_dates_included=False
        ).model_dump(exclude=[coa_meta.CREATED_DATE, coa_meta.UPDATED_DATE])

        sql_query_details = SelectChartOfAccountsByDetails(
            coa_account_id=payload[coa_meta.ACCOUNT_ID],
            coa_name=payload[coa_meta.NAME],
            coa_type=payload[coa_meta.TYPE],
            coa_description=payload[coa_meta.DESCRIPTION]
        )

        ChartOfAccountsController().createAccount(payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

        assert result.shape[0] == 1
        
    @pytest.mark.parametrize("param", coa_types.getTypesAsList())
    def test_happy_path_with_different_types(self, param):
        payload = ChartOfAccountsPayloadGenerator(
            description=None,
            type=param,
            is_dates_included=False
        ).model_dump(exclude=[coa_meta.CREATED_DATE, coa_meta.UPDATED_DATE])

        sql_query_details = SelectChartOfAccountsByDetailsDescriptionIsNull(
            coa_account_id=payload[coa_meta.ACCOUNT_ID],
            coa_name=payload[coa_meta.NAME],
            coa_type=payload[coa_meta.TYPE]
        )
        
        ChartOfAccountsController().createAccount(payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        result = db_obj.getData()

        assert result.shape[0] == 1

    def test_create_with_already_existing_account_id(self):
        payload = ChartOfAccountsPayloadGenerator(
            description=None,
            is_dates_included=False
        ).model_dump(exclude=[coa_meta.CREATED_DATE, coa_meta.UPDATED_DATE])

        ChartOfAccountsController().createAccount(payload)

        payload = ChartOfAccountsPayloadGenerator(
            account_id=payload[coa_meta.ACCOUNT_ID]
        ).model_dump(exclude=[coa_meta.CREATED_DATE, coa_meta.UPDATED_DATE])

        sql_query_details = SelectChartOfAccountsByAccountId(
            coa_account_id=payload[coa_meta.ACCOUNT_ID]
        )        

        output = ChartOfAccountsController().createAccount(payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))
        result = db_obj.getData()

        assert output["status"] == 400
        assert output["code"] == "COA0105"
        assert output["message"] == f"Account ID \'{payload[coa_meta.ACCOUNT_ID]}\' already exists"
        assert result.shape[0] == 1

    def test_create_with_already_existing_account_name(self):
        payload = ChartOfAccountsPayloadGenerator(
            description=None,
            is_dates_included=False
        ).model_dump(exclude=[coa_meta.CREATED_DATE, coa_meta.UPDATED_DATE])

        ChartOfAccountsController().createAccount(payload)

        payload = ChartOfAccountsPayloadGenerator(
            name=payload[coa_meta.NAME]
        ).model_dump(exclude=[coa_meta.CREATED_DATE, coa_meta.UPDATED_DATE])
        sql_query_details = SelectChartOfAccountsByName(
            coa_name=payload[coa_meta.NAME]
        )

        output = ChartOfAccountsController().createAccount(payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))
        result = db_obj.getData()

        assert output["status"] == 400
        assert output["code"] == "COA0103"
        assert output["message"] == f"Account Name \'{payload[coa_meta.NAME]}\' already exists"
        assert result.shape[0] == 1

    def test_create_with_nonexistent_account_mapping(self):
        payload = ChartOfAccountsPayloadGenerator(
            account_mapping=''.join(random.choices(string.digits, k=6)),
            is_dates_included=False
        ).model_dump(exclude=[coa_meta.CREATED_DATE, coa_meta.UPDATED_DATE])

        sql_query_details = SelectChartOfAccountsByAccountId(
            coa_account_id=payload[coa_meta.ACCOUNT_ID]
        )

        output = ChartOfAccountsController().createAccount(payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))
        result = db_obj.getData()

        assert output["status"] == 400
        assert output["code"] == "COA0104"
        assert output["message"] == f"Account Map \'{payload[coa_meta.ACCOUNT_MAPPING]}\' Not Found"
        assert result.shape[0] == 0
