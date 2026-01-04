import pytest
import logging
from datetime import datetime, timezone
from ...models.chart_of_accounts import *
from ...validators.chart_of_accounts import (
    ChartOfAccountsModel
)
from ...core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from ...models.chart_of_accounts import coa_meta
from ..utils.db.connector import (
    SQLiteClient
)
from ..utils.helpers import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


creds = {
    "file_name": "temp_state.db"
}

class TestAccountInsertRecord:
    def test_happy_path(self, generate_account_request_payload):
        core_model = ChartOfAccountsCore()
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID],
            "<coa_name>": payload[coa_meta.NAME],
            "<coa_type>": payload[coa_meta.TYPE],
            "<coa_description>": payload[coa_meta.DESCRIPTION],
            "<coa_created_date>": current_datetime,
            "<coa_updated_date>": current_datetime
        }
        
        core_model.insertRecord(payload)

        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

    def test_duplicate_record_error(self, generate_account_request_payload):
        expected = "UNIQUE constraint failed"
        core_model = ChartOfAccountsCore()

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID],
            "<coa_name>": payload[coa_meta.NAME],
            "<coa_type>": payload[coa_meta.TYPE],
            "<coa_description>": payload[coa_meta.DESCRIPTION],
            "<coa_created_date>": current_datetime,
            "<coa_updated_date>": current_datetime
        }

        core_model.insertRecord(payload)
        with pytest.raises(Exception) as excinfo:
            core_model.insertRecord(payload)
        logging.info(str(excinfo))
        assert expected in str(excinfo)

        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_invalid_account_id_values_TypeError(self, generate_account_request_payload, param):
        expected = f"ChartOfAccountsModel Error: incorrect account ID data type '{type(param).__name__}'"
        core_model = ChartOfAccountsCore()

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID]
        }
        payload[coa_meta.ACCOUNT_ID] = param
        
        with pytest.raises(TypeError) as excinfo:
            core_model.insertRecord(payload)
        logging.info(str(excinfo))
        assert expected in str(excinfo)

        contents = load_mapped_sql_files("Chart Of Accounts", "Search By ID", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 0


    @pytest.mark.parametrize("param", ["", "1234", "1234567890123456"])
    def test_invalid_account_id_values_ValidationError(self, generate_account_request_payload, param):
        from pydantic import ValidationError
        core_model = ChartOfAccountsCore()

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID]
        }
        payload[coa_meta.ACCOUNT_ID] = param
        del payload[coa_meta.CREATED_DATE]
        del payload[coa_meta.UPDATED_DATE]
        
        error_1 = "ChartOfAccountsModel Error: account ID minimum field length...ount_mapping': None}, input_type=dict]"
        error_2 = "ChartOfAccountsModel Error: account ID maximum length is 15"
        with pytest.raises(ValidationError) as excinfo:
            core_model.insertRecord(payload)
        logging.info(str(excinfo))
        if len(param) < 5:
            assert error_1 in str(excinfo)
        else:
            assert error_2 in str(excinfo)

        contents = load_mapped_sql_files("Chart Of Accounts", "Search By ID", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 0

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_invalid_account_name_values_TypeError(self, generate_account_request_payload, param):
        expected = f"ChartOfAccountsModel Error: incorrect account name data type '{type(param).__name__}'"
        core_model = ChartOfAccountsCore()
        
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID]
        }
        payload[coa_meta.NAME] = param
        del payload[coa_meta.CREATED_DATE]
        del payload[coa_meta.UPDATED_DATE]

        with pytest.raises(TypeError) as excinfo:
            core_model.insertRecord(payload)
        logging.info(str(excinfo))
        assert expected in str(excinfo)

        contents = load_mapped_sql_files("Chart Of Accounts", "Search By ID", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 0


    @pytest.mark.parametrize("param", ["", "2647902066830292456314023255772735635300818039589536229964640280111382742403410796944455975648526778393253846437709638360033347483170939266852249670143"])
    def test_invalid_account_name_values_ValidationError(self, generate_account_request_payload, param):
        from pydantic import ValidationError
        core_model = ChartOfAccountsCore()
        
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID]
        }
        payload[coa_meta.NAME] = param
        del payload[coa_meta.CREATED_DATE]
        del payload[coa_meta.UPDATED_DATE]

        error_1 = "ChartOfAccountsModel Error: account name minimum length is ...ount_mapping': None}"
        error_2 = "ChartOfAccountsModel Error: account name maximum length is ...ount_mapping': None}"

        with pytest.raises(ValidationError) as excinfo:
            core_model.insertRecord(payload)
        logging.info(str(excinfo))
        if len(param) <= 0:
            assert error_1 in str(excinfo)
        else:
            assert error_2 in str(excinfo)

        contents = load_mapped_sql_files("Chart Of Accounts", "Search By ID", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 0

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_invalid_account_type_values_TypeError(self, generate_account_request_payload, param):
        expected = f"ChartOfAccountsModel Error: incorrect account type data type '{type(param).__name__}'"
        core_model = ChartOfAccountsCore()

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID]
        }
        payload[coa_meta.TYPE] = param
        del payload[coa_meta.CREATED_DATE]
        del payload[coa_meta.UPDATED_DATE]

        
        with pytest.raises(TypeError) as excinfo:
            core_model.insertRecord(payload)
        logging.info(str(excinfo))
        assert expected in str(excinfo)

        contents = load_mapped_sql_files("Chart Of Accounts", "Search By ID", where_clause_values) 
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 0

    @pytest.mark.parametrize("param", ["", "SAMPLE", "DISBURSEMENT", "asset", "liability"])
    def test_invalid_account_type_values_ValidationError(self, generate_account_request_payload, param):
        from pydantic import ValidationError
        core_model = ChartOfAccountsCore()

        expected = "Error: Unknown account type"
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID]
        }
        payload[coa_meta.TYPE] = param
        del payload[coa_meta.CREATED_DATE]
        del payload[coa_meta.UPDATED_DATE]

        with pytest.raises(ValidationError) as excinfo:
            core_model.insertRecord(payload)
        logging.info(str(excinfo))
        assert expected in str(excinfo)

        contents = load_mapped_sql_files("Chart Of Accounts", "Search By ID", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 0



        