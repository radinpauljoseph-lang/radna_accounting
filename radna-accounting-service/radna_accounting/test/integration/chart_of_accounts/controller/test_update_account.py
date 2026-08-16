import pytest
from faker import Faker
import string
import uuid
import random
from datetime import datetime, timedelta
from radna_accounting.controller.chart_of_accounts import ChartOfAccountsController
from radna_accounting.models.chart_of_accounts import coa_meta
from radna_accounting.validators.chart_of_accounts import account_types
from radna_accounting.test.data.chart_of_accounts import (
    ChartOfAccountsPayloadGenerator,
    ChartOfAccountsUpdatePayloadGenerator
)
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials
from radna_accounting.test.data.db.chart_of_accounts.queries import (
    SelectChartOfAccountsByDetails,
    SelectChartOfAccountsByAccountId,
    SelectChartOfAccountsByName
)
from radna_accounting.test.data.db.constants import SQL_TEXT_FIELD

class TestChartOfAccountsControllerUpdateAccount:

    @pytest.mark.parametrize("param", [coa_meta.NAME, coa_meta.TYPE, coa_meta.DESCRIPTION, coa_meta.ACCOUNT_MAPPING])
    def test_happy_path_update_values(self, param):
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        
        ChartOfAccountsController().createAccount(payload)

        account_id = payload[coa_meta.ACCOUNT_ID]

        if param in [coa_meta.NAME, coa_meta.DESCRIPTION]:
            payload[param] = Faker().bs()
        elif param == coa_meta.TYPE:
            new_value = account_types[random.randrange(0, len(account_types))]

            is_new_value_same = True if new_value == payload[param] else False
            current_datetime = datetime.now()
            end_datetime = current_datetime + timedelta(seconds=30)

            while is_new_value_same:
                new_value = account_types[random.randrange(0, len(account_types))]
                is_new_value_same = True if new_value == payload[param] else False

                if current_datetime >= end_datetime:
                    raise Exception({
                        "error": "Failed to generate new Account Type"
                    })
                current_datetime = datetime.now()
            payload[param] = new_value
        else:
            account_data = ChartOfAccountsPayloadGenerator().model_dump()
            payload[param] = account_data[coa_meta.ACCOUNT_ID]
            ChartOfAccountsController().createAccount(account_data)
        
        payload = ChartOfAccountsUpdatePayloadGenerator(**payload).model_dump()

        sql_query_details = SelectChartOfAccountsByDetails(
            coa_account_id=account_id,
            coa_name=payload[coa_meta.NAME],
            coa_type=payload[coa_meta.TYPE],
            coa_description=payload[coa_meta.DESCRIPTION],
            coa_account_mapping=payload[coa_meta.ACCOUNT_MAPPING] if payload[coa_meta.ACCOUNT_MAPPING] is not None else ""
        )

        ChartOfAccountsController().updateAccount(
            id=account_id,
            obj=payload
        )

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))
        result = db_obj.getData()

        assert result.shape[0] == 1
        assert result[param].iloc[0] == payload[param]

    def test_update_nonexistent_account(self):
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        account_id = payload[coa_meta.ACCOUNT_ID]
        payload = ChartOfAccountsUpdatePayloadGenerator(**payload).model_dump()

        sql_query_details = SelectChartOfAccountsByAccountId(
            coa_account_id=account_id
        )

        output = ChartOfAccountsController().updateAccount(
            id=account_id,
            obj=payload
        )
        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))
        result = db_obj.getData()

        assert output["status"] == 400
        assert output["code"] == "COA0101"
        assert output["message"] == f"Account ID \'{account_id}\' does not exist"
        assert result.shape[0] == 0

    def test_update_name_with_existing_name(self):
        account_name = Faker().bs()
        ChartOfAccountsController().createAccount(
            obj=ChartOfAccountsPayloadGenerator(name=account_name).model_dump()
        )

        payload = ChartOfAccountsPayloadGenerator().model_dump()
        current_name = payload[coa_meta.NAME]
        account_id = payload[coa_meta.ACCOUNT_ID]

        ChartOfAccountsController().createAccount(payload)

        payload[coa_meta.NAME] = account_name
        payload = ChartOfAccountsUpdatePayloadGenerator(**payload).model_dump()

        sql_query_details = SelectChartOfAccountsByName(
            coa_name=current_name
        )

        output = ChartOfAccountsController().updateAccount(
            id=account_id,
            obj=payload
        )

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
        .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))
        result = db_obj.getData()
        
        assert output["status"] == 400
        assert output["code"] == "COA0103"
        assert output["message"] == f"Account Name \'{account_name}\' already exists"
        assert result.shape[0] == 1

    def test_update_account_with_nonexistent_account_mapping(self):
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        account_id = payload[coa_meta.ACCOUNT_ID]

        ChartOfAccountsController().createAccount(payload)

        payload[coa_meta.ACCOUNT_MAPPING] = ''.join(random.choices(string.digits, k=6))
        payload = ChartOfAccountsUpdatePayloadGenerator(**payload).model_dump()

        sql_query_details = SelectChartOfAccountsByAccountId(
            coa_account_id=account_id
        )

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))
        result = db_obj.getData()

        output = ChartOfAccountsController().updateAccount(
            id=account_id,
            obj=payload
        )

        assert output["status"] == 400
        assert output["code"] == "COA0104"
        assert output["message"] == f"Account Map \'{payload[coa_meta.ACCOUNT_MAPPING]}\' Not Found"
        assert result.shape[0] == 1
        assert result[coa_meta.ACCOUNT_MAPPING].iloc[0] is None

    def test_update_account_with_nonexistent_account_mapping_current_value_not_none(self):
        current_account_mapping_value = ''.join(random.choices(string.digits, k=6))
        ChartOfAccountsController(rrn=str(uuid.uuid4())).createAccount(
            ChartOfAccountsPayloadGenerator(
                account_id=current_account_mapping_value
            ).model_dump()
        )

        payload = ChartOfAccountsPayloadGenerator(
            account_mapping=current_account_mapping_value
        ).model_dump()
        account_id = payload[coa_meta.ACCOUNT_ID]

        ChartOfAccountsController().createAccount(payload)

        payload[coa_meta.ACCOUNT_MAPPING] = ''.join(random.choices(string.digits, k=6))
        payload = ChartOfAccountsUpdatePayloadGenerator(**payload).model_dump()

        sql_query_details = SelectChartOfAccountsByAccountId(
            coa_account_id=account_id
        )

        output = ChartOfAccountsController(rrn=str(uuid.uuid4())).updateAccount(
            id=account_id,
            obj=payload
        )
        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(sql_query_details.text)\
            .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))
        result = db_obj.getData()

        assert output["status"] == 400
        assert output["code"] == "COA0104"
        assert output["message"] == f"Account Map \'{payload[coa_meta.ACCOUNT_MAPPING]}\' Not Found"
        assert result.shape[0] == 1
        assert result[coa_meta.ACCOUNT_MAPPING].iloc[0] == current_account_mapping_value


        



        

        







