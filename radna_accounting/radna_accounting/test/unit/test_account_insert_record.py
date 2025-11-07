import pytest
import logging
from datetime import datetime, timezone
from sqlalchemy import (
    create_engine
)
from sqlalchemy.orm import (
    declarative_base
)
from ...configs.config import (
    engine,
    ENV
)
from ...configs.initialize import initialize
from ...models.chart_of_accounts import *
from ...validators.chart_of_accounts import (
    ChartOfAccountsModel
)
from ...core.chart_of_accounts.record_operations import (
    account_insert_record
)
from ..utils.db.connector import (
    SQLiteClient,
    PostgreSQLClient
)
from ..utils.helpers import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

Base = declarative_base()

creds = {
    "file_name": "temp_state.db"
}

class TestAccountInsertRecord:
    def test_happy_path(self, generate_account_request_payload):
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", ""),
            "<coa_account_id>": payload['account_id'],
            "<coa_name>": payload['name'],
            "<coa_type>": payload['type'],
            "<coa_description>": payload['description'],
            "<coa_created_date>": current_datetime,
            "<coa_updated_date>": current_datetime
        }
        
        account_insert_record(engine, payload)

        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

    @pytest.mark.parametrize("param", ["", "123", "abc"])
    def test_invalid_connection(self, generate_account_request_payload, param):
        expected = "Could not parse SQLAlchemy URL from given URL string"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()

        connection_string = param
        with pytest.raises(Exception) as excinfo:
            account_insert_record(create_engine(connection_string, echo=True), payload)
        logging.info(str(excinfo))
        assert expected in str(excinfo)

    def test_duplicate_record_error(self, generate_account_request_payload):
        expected = "UNIQUE constraint failed"
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", ""),
            "<coa_account_id>": payload['account_id'],
            "<coa_name>": payload['name'],
            "<coa_type>": payload['type'],
            "<coa_description>": payload['description'],
            "<coa_created_date>": current_datetime,
            "<coa_updated_date>": current_datetime
        }

        account_insert_record(engine, payload)
        with pytest.raises(Exception) as excinfo:
            account_insert_record(engine, payload)
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

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", "")
        }
        payload['account_id'] = param
        del payload["created_date"]
        del payload["updated_date"]
        
        with pytest.raises(TypeError) as excinfo:
            account_insert_record(engine, payload)
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

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", "")
        }
        payload['account_id'] = param
        del payload["created_date"]
        del payload["updated_date"]

        error_1 = "ChartOfAccountsModel Error: account ID minimum field length...ount_mapping': None}, input_type=dict]"
        error_2 = "ChartOfAccountsModel Error: account ID maximum length is 15"
        with pytest.raises(ValidationError) as excinfo:
            account_insert_record(engine, payload)
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

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", "")
        }
        payload['name'] = param
        del payload["created_date"]
        del payload["updated_date"]

        with pytest.raises(TypeError) as excinfo:
            account_insert_record(engine, payload)
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


    @pytest.mark.parametrize("param", ["", "ezxPOoQiJumfDGYvhtUwNcFerZklOFIfPrYABVtpkmVhCHwrCjGsw"])
    def test_invalid_account_name_values_ValidationError(self, generate_account_request_payload, param):
        from pydantic import ValidationError
        
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", "")
        }
        payload['name'] = param
        del payload["created_date"]
        del payload["updated_date"]

        error_1 = "ChartOfAccountsModel Error: account name minimum length is ...ount_mapping': None}"
        error_2 = "ChartOfAccountsModel Error: account name maximum length is ...ount_mapping': None}"

        with pytest.raises(ValidationError) as excinfo:
            account_insert_record(engine, payload)
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

        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", "")
        }
        payload['type'] = param
        del payload["created_date"]
        del payload["updated_date"]

        
        with pytest.raises(TypeError) as excinfo:
            account_insert_record(engine, payload)
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

        expected = "Error: Unknown account type"
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", "")
        }
        payload['type'] = param
        del payload["created_date"]
        del payload["updated_date"]

        with pytest.raises(ValidationError) as excinfo:
            account_insert_record(engine, payload)
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



        