import pytest
from datetime import datetime, timezone
from radna_accounting.validators.chart_of_accounts import ChartOfAccountsModel
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.test.data.chart_of_accounts import ChartOfAccountsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient

creds = {
    "database": "temp_state.db"
}

class TestAccountInsertRecord:

    def test_happy_path(self):
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
        del payload.created_date
        del payload.updated_date
        
        core_model.insertRecord(payload)

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
        del db_obj

        assert result.shape[0] == 1

    def test_duplicate_record_error(self):
        expected = "UNIQUE constraint failed"
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

        core_model.insertRecord(payload)
        with pytest.raises(Exception) as excinfo:
            core_model.insertRecord(payload)
        assert expected in str(excinfo)

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
        del db_obj

        assert result.shape[0] == 1

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_invalid_account_id_values_Exception(self, param):
        expected = f"Incorrect account ID data type '{type(param).__name__}'"
        core_model = ChartOfAccountsCore()

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        payload.account_id = param
        
        with pytest.raises(Exception) as excinfo:
            core_model.insertRecord(payload)
        assert expected in str(excinfo)


    @pytest.mark.parametrize("param", ["", "1234", "1234567890123451234567890123456"])
    def test_invalid_account_id_values_field_length_error(self, param):
        core_model = ChartOfAccountsCore()

        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        payload.account_id = param
        
        error_code_one = "COA0002"
        error_code_two = "COA0003"
        with pytest.raises(Exception) as excinfo:
            core_model.insertRecord(payload)

        if len(param) < 5:
            assert error_code_one in str(excinfo)
        else:
            assert error_code_two in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_invalid_account_name_values_Exception(self, param):
        expected = f"Incorrect account name data type '{type(param).__name__}'"
        core_model = ChartOfAccountsCore()
        
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        payload.name = param

        with pytest.raises(Exception) as excinfo:
            core_model.insertRecord(payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", ["", "2647902066830292456314023255772735635300818039589536229964640280111382742403410796944455975648526778393253846437709638360033347483170939266852249670143"])
    def test_invalid_account_name_values_field_length_error(self, param):
        core_model = ChartOfAccountsCore()

        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        payload.name = param

        error_code_one = "COA0006"
        error_code_two = "COA0005"
        with pytest.raises(Exception) as excinfo:
            core_model.insertRecord(payload)
        
        if len(param) <= 0:
            assert error_code_one in str(excinfo)
        else:
            assert error_code_two in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_invalid_account_type_values_Exception(self, param):
        expected = f"Incorrect account type data type '{type(param).__name__}'"
        core_model = ChartOfAccountsCore()

        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        payload.type = param
        
        with pytest.raises(Exception) as excinfo:
            core_model.insertRecord(payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", ["", "SAMPLE", "DISBURSEMENT", "asset", "liability"])
    def test_invalid_account_type_values_invalid_account_type(self, param):
        core_model = ChartOfAccountsCore()

        expected = f"Unknown account type \'{param}\'"
        payload = ChartOfAccountsPayloadGenerator().model_dump()
        payload = ChartOfAccountsModel(**payload)
        payload.type = param

        with pytest.raises(Exception) as excinfo:
            core_model.insertRecord(payload)
        
        assert expected in str(excinfo)


        