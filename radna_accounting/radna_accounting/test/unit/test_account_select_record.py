import pytest
import logging
import string
import random
from datetime import datetime, timezone
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
    account_insert_record,
    account_select_record
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


class TestAccountSelectRecord:
    @pytest.mark.parametrize("param", ["id", "name", "account_id"])
    def test_happy_path_using_unique_value_columns(self, generate_account_request_payload, param):
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

        query_value = payload[param] if param != 'id' else str(payload[param]).replace("-", "")
        query_result = account_select_record(engine, param, query_value)

        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

        for key in query_result.keys():
            if key == 'id':
                assert str(query_result[key]).replace("-", "") == result[key].iloc[0]
            elif 'date' in key:
                assert query_result[key] == datetime.strptime(result[key].iloc[0], "%Y-%m-%d %H:%M:%S")
            else:
                assert query_result[key] == result[key].iloc[0]
    
    def test_happy_path_using_account_type(self, generate_account_request_payload):
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        where_clause_values = {
            "<coa_type>": payload['type']
        }
        
        account_insert_record(engine, payload)

        query_result = account_select_record(engine, 'name', payload['name'])

        contents = load_mapped_sql_files("Chart Of Accounts", "Search By Type", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] >= 1

        expected = result[result['id'] == str(query_result['id']).replace("-", "")]
        assert expected.shape[0] == 1     

    @pytest.mark.parametrize("param", ["id", "name", "account_id", "type", "description"])
    def test_using_nonexistent_record_values(self, param):
            expected = "AttributeError"
            value = ''.join(random.choices(string.digits, k=6))
            with pytest.raises(AttributeError) as excinfo:
                account_select_record(engine, param, value)
            assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}])
    def test_id_invalid_data_type(self, param):
            expected = "TypeError"
            value = param
            with pytest.raises(TypeError) as excinfo:
                account_select_record(engine, "id", value)
            assert expected in str(excinfo)

    def test_id_using_nonetype(self):
            expected = "AttributeError"
            value = None
            with pytest.raises(AttributeError) as excinfo:
                account_select_record(engine, "id", value)
            assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}])
    def test_account_id_invalid_data_type(self, param):
            expected = "TypeError"
            value = param
            with pytest.raises(TypeError) as excinfo:
                account_select_record(engine, "id", value)
            assert expected in str(excinfo)

    def test_account_id_using_nonetype(self):
            expected = "AttributeError"
            value = None
            with pytest.raises(AttributeError) as excinfo:
                account_select_record(engine, "account_id", value)
            assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}])
    def test_account_name_invalid_data_type(self, param):
            expected = "TypeError"
            value = param
            with pytest.raises(TypeError) as excinfo:
                account_select_record(engine, "name", value)
            assert expected in str(excinfo)

    def test_account_name_using_nonetype(self):
            expected = "AttributeError"
            value = None
            with pytest.raises(AttributeError) as excinfo:
                account_select_record(engine, "name", value)
            assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}])
    def test_account_type_invalid_data_type(self, param):
            expected = "TypeError"
            value = param
            with pytest.raises(TypeError) as excinfo:
                account_select_record(engine, "type", value)
            assert expected in str(excinfo)

    def test_account_type_using_nonetype(self):
            expected = "AttributeError"
            value = None
            with pytest.raises(AttributeError) as excinfo:
                account_select_record(engine, "type", value)
            assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}])
    def test_column_name_param_invalid_data_type(self, generate_account_request_payload, param):
            expected = "OperationalError"
            value = param
            payload = generate_account_request_payload
            payload = ChartOfAccountsModel(**payload).model_dump()

            account_insert_record(engine, payload)

            with pytest.raises(Exception) as excinfo:
                account_select_record(engine, value, payload['id'])
            assert expected in str(excinfo)