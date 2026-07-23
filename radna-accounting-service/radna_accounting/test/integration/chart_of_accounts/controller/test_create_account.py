import pytest
from faker import Faker
import string
import random
from datetime import datetime, timezone
from radna_accounting.controller.chart_of_accounts import ChartOfAccountsController
from radna_accounting.models.chart_of_accounts import (
    coa_meta,
    coa_types
)
from radna_accounting.test.data.chart_of_accounts import ChartOfAccountsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.configs.response_codes.mapping import COA_CODE
creds = {
    "database": "temp_state.db"
}

class TestChartOfAccountsControllerCreateAccount:

    def test_happy_path(self):
        payload = ChartOfAccountsPayloadGenerator(is_dates_included=False).model_dump()
        payload[coa_meta.DESCRIPTION] = None

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "coa_account_id": payload[coa_meta.ACCOUNT_ID],
            "coa_name": payload[coa_meta.NAME],
            "coa_type": payload[coa_meta.TYPE],
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        }

        ChartOfAccountsController().createAccount(payload)

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
            AND account_mapping IS NULL
            AND description IS NULL
            AND created_date >= :coa_created_date
            AND updated_date >= :coa_updated_date
        """
        )\
        .execute(where_clause_values)

        result = db_obj.getData()

        assert result.shape[0] == 1

    def test_happy_path_with_account_mapping(self):
        payload = ChartOfAccountsPayloadGenerator(is_dates_included=False).model_dump()
        payload[coa_meta.DESCRIPTION] = None

        ChartOfAccountsController().createAccount(payload)
        
        payload = ChartOfAccountsPayloadGenerator(
            account_mapping=payload[coa_meta.ACCOUNT_ID]
        ).model_dump()
                
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "coa_account_id": payload[coa_meta.ACCOUNT_ID],
            "coa_name": payload[coa_meta.NAME],
            "coa_type": payload[coa_meta.TYPE],
            "coa_description": payload[coa_meta.DESCRIPTION],
            "coa_account_mapping": payload[coa_meta.ACCOUNT_MAPPING],
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        }

        ChartOfAccountsController().createAccount(payload)


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
            AND account_mapping = :coa_account_mapping
            AND created_date >= :coa_created_date
            AND updated_date >= :coa_updated_date
        """
        )\
        .execute(where_clause_values)

        result = db_obj.getData()

        assert result.shape[0] == 1
    
    def test_happy_path_with_description(self):
        payload = ChartOfAccountsPayloadGenerator(is_dates_included=False).model_dump()
        payload[coa_meta.DESCRIPTION] = Faker().bs()

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "coa_account_id": payload[coa_meta.ACCOUNT_ID],
            "coa_name": payload[coa_meta.NAME],
            "coa_type": payload[coa_meta.TYPE],
            "coa_description": payload[coa_meta.DESCRIPTION],
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        }

        ChartOfAccountsController().createAccount(payload)

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
            AND account_mapping IS NULL
            AND created_date >= :coa_created_date
            AND updated_date >= :coa_updated_date
        """
        )\
        .execute(where_clause_values)

        result = db_obj.getData()

        assert result.shape[0] == 1
        
    @pytest.mark.parametrize("param", coa_types.getTypesAsList())
    def test_happy_path_with_different_types(self, param):
        payload = ChartOfAccountsPayloadGenerator(is_dates_included=False).model_dump()
        payload[coa_meta.DESCRIPTION] = None
        payload[coa_meta.TYPE] = param

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "coa_account_id": payload[coa_meta.ACCOUNT_ID],
            "coa_name": payload[coa_meta.NAME],
            "coa_type": payload[coa_meta.TYPE],
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        }

        ChartOfAccountsController().createAccount(payload)

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
            AND account_mapping IS NULL
            AND created_date >= :coa_created_date
            AND updated_date >= :coa_updated_date
        """
        )\
        .execute(where_clause_values)

        result = db_obj.getData()

        assert result.shape[0] == 1

    def test_create_with_already_existing_account_id(self):
        payload = ChartOfAccountsPayloadGenerator(is_dates_included=False).model_dump()
        payload[coa_meta.DESCRIPTION] = None

        ChartOfAccountsController().createAccount(payload)

        payload = ChartOfAccountsPayloadGenerator(
            account_id=payload[coa_meta.ACCOUNT_ID]
        ).model_dump()
                
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "coa_account_id": payload[coa_meta.ACCOUNT_ID],
            "coa_name": payload[coa_meta.NAME],
            "coa_type": payload[coa_meta.TYPE],
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        }

        output = ChartOfAccountsController().createAccount(payload)
        assert output["status"] == 400
        assert output["code"] == "COA0105"
        assert output["message"] == f"Account ID \'{payload[coa_meta.ACCOUNT_ID]}\' already exists"
        
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
            AND account_mapping IS NULL
            AND created_date >= :coa_created_date
            AND updated_date >= :coa_updated_date
        """
        )\
        .execute(where_clause_values)

        result = db_obj.getData()

        assert result.shape[0] == 0

    def test_create_with_already_existing_account_name(self):
        payload = ChartOfAccountsPayloadGenerator(is_dates_included=False).model_dump()
        payload[coa_meta.DESCRIPTION] = None

        ChartOfAccountsController().createAccount(payload)

        payload = ChartOfAccountsPayloadGenerator(
            name=payload[coa_meta.NAME]
        ).model_dump()
                
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "coa_account_id": payload[coa_meta.ACCOUNT_ID],
            "coa_name": payload[coa_meta.NAME],
            "coa_type": payload[coa_meta.TYPE],
            "coa_account_mapping": "",
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        }

        output = ChartOfAccountsController().createAccount(payload)
        assert output["status"] == 400
        assert output["code"] == "COA0103"
        assert output["message"] == f"Account Name \'{payload[coa_meta.NAME]}\' already exists"
        
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
            AND account_mapping IS NULL
            AND created_date >= :coa_created_date
            AND updated_date >= :coa_updated_date
        """
        )\
        .execute(where_clause_values)

        result = db_obj.getData()

        assert result.shape[0] == 0

    def test_create_with_nonexistent_account_mapping(self):
        payload = ChartOfAccountsPayloadGenerator(is_dates_included=False).model_dump()
        payload[coa_meta.ACCOUNT_MAPPING] = ''.join(random.choices(string.digits, k=6))

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "coa_account_id": payload[coa_meta.ACCOUNT_ID],
            "coa_name": payload[coa_meta.NAME],
            "coa_type": payload[coa_meta.TYPE],
            "coa_account_mapping": payload[coa_meta.ACCOUNT_MAPPING],
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        }

        output = ChartOfAccountsController().createAccount(payload)
        assert output["status"] == 400
        assert output["code"] == "COA0104"
        assert output["message"] == f"Account Map \'{payload[coa_meta.ACCOUNT_MAPPING]}\' Not Found"

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

        assert result.shape[0] == 0
