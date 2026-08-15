import pytest
from datetime import datetime, timezone
from radna_accounting.validators.chart_of_accounts import ChartOfAccountsModel
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.test.data.chart_of_accounts import ChartOfAccountsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient

from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials

class TestAccountInsertRecord:

    def test_happy_path(self):
        core_model = ChartOfAccountsCore()
        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        del payload.created_date
        del payload.updated_date
        
        core_model.insertRecord(payload)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
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
        .execute({
            "coa_account_id": payload.account_id,
            "coa_name": payload.name,
            "coa_type": payload.type,
            "coa_description": payload.description,
            "coa_account_mapping": "",
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        })

        result = db_obj.getData()

        assert result.shape[0] == 1

    def test_duplicate_record_error(self):
        expected = "UNIQUE constraint failed"
        core_model = ChartOfAccountsCore()

        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)

        core_model.insertRecord(payload)
        with pytest.raises(Exception) as excinfo:
            core_model.insertRecord(payload)
        assert expected in str(excinfo)

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
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
        .execute({
            "coa_account_id": payload.account_id,
            "coa_name": payload.name,
            "coa_type": payload.type,
            "coa_description": payload.description,
            "coa_account_mapping": "",
            "coa_created_date": current_datetime,
            "coa_updated_date": current_datetime
        })

        result = db_obj.getData()

        assert result.shape[0] == 1


        