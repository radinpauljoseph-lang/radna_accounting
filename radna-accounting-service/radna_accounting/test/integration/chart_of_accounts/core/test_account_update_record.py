import pytest
from faker import Faker
from datetime import datetime, timezone
from radna_accounting.validators.chart_of_accounts import ChartOfAccountsModel
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.models.chart_of_accounts import coa_types

from radna_accounting.test.data.chart_of_accounts import ChartOfAccountsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient

creds = {
    "database": "temp_state.db"
}

class TestAccounUpdateRecord:
    def test_happy_path_update_name(self):
        account_name = Faker().bs()
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"

        core_model.insertRecord(payload)
        updated_datetime = datetime.now(timezone.utc)
        updated_datetime = updated_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(updated_datetime.microsecond / 1000):03d}"
        
        where_clause_values = {
            "coa_account_id": payload.account_id,
            "coa_name": account_name,
            "coa_type": payload.type,
            "coa_description": payload.description,
            "coa_account_mapping": "",
            "coa_created_date": current_datetime,
            "coa_updated_date": updated_datetime
        }
        payload.name = account_name
        core_model.updateRecordById(payload.account_id, payload)

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
    
    def test_happy_path_update_description_none(self):
        account_description = Faker().bs()
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator(
            description=account_description
        ).model_dump()
        payload = ChartOfAccountsModel(**payload)
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"

        core_model.insertRecord(payload)
        updated_datetime = datetime.now(timezone.utc)
        updated_datetime = updated_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(updated_datetime.microsecond / 1000):03d}"

        where_clause_values = {
            "coa_account_id": payload.account_id,
            "coa_name": payload.name,
            "coa_type": payload.type,
            "coa_account_mapping": "",
            "coa_created_date": current_datetime,
            "coa_updated_date": updated_datetime
        }

        payload.description = None
        core_model.updateRecordById(payload.account_id, payload)

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
            AND description IS NULL
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

    def test_happy_path_update_description(self):
        account_description = Faker().bs()
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"

        core_model.insertRecord(payload)
        updated_datetime = datetime.now(timezone.utc)
        updated_datetime = updated_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(updated_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "coa_account_id": payload.account_id,
            "coa_name": payload.name,
            "coa_type": payload.type,
            "coa_description": account_description,
            "coa_account_mapping": "",
            "coa_created_date": current_datetime,
            "coa_updated_date": updated_datetime
        }

        payload.description = account_description
        core_model.updateRecordById(payload.account_id, payload)

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

    @pytest.mark.parametrize("param", [coa_types.ASSET, coa_types.LIABILITY, coa_types.EQUITY, coa_types.LIABILITY, coa_types.REVENUE, coa_types.COST])
    def test_happy_path_update_account_type(self, param):
        core_model = ChartOfAccountsCore()
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"

        core_model.insertRecord(payload)
        updated_datetime = datetime.now(timezone.utc)
        updated_datetime = updated_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(updated_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "coa_account_id": payload.account_id,
            "coa_name": payload.name,
            "coa_type": param,
            "coa_description": payload.description,
            "coa_account_mapping": "",
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        }

        payload.type = param
        core_model.updateRecordById(payload.account_id, payload)

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

    def test_duplicate_name_error(self):
        expected = "UNIQUE constraint failed"
        core_model = ChartOfAccountsCore()
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
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
            core_model = ChartOfAccountsCore()
            payload = ChartOfAccountsPayloadGenerator().model_dump()
            payload = ChartOfAccountsModel(**payload)
            expected = "COA0101"
            
            with pytest.raises(Exception) as excinfo:
                core_model.updateRecordById(payload.account_id, payload)
            assert expected in str(excinfo)

