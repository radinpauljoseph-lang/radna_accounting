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
    ChartOfAccountsModel,
    account_types
)
from ...core.chart_of_accounts.record_operations import (
    account_insert_record,
    account_update_record
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

class TestAccounUpdateRecord:
    def test_happy_path_update_account_name(self, generate_account_request_payload):
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        
        account_insert_record(engine, payload)
        payload['name'] = fake.bs()
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
        payload['created_date'] = now
        payload['updated_date'] = now
        account_update_record(engine, payload['account_id'], payload)
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", ""),
            "<coa_account_id>": payload['account_id'],
            "<coa_name>": payload['name'],
            "<coa_type>": payload['type'],
            "<coa_description>": payload['description'],
            "<coa_created_date>": payload['created_date'],
            "<coa_updated_date>": payload['updated_date']
        }
        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

    def test_happy_path_update_account_type(self, generate_account_request_payload):
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        current_type = payload['type']

        account_insert_record(engine, payload)
        while payload['type'] == current_type:
            payload['type'] = account_types[random.randrange(0, len(account_types))]
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
        payload['created_date'] = now
        payload['updated_date'] = now
        account_update_record(engine, payload['account_id'], payload)
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", ""),
            "<coa_account_id>": payload['account_id'],
            "<coa_name>": payload['name'],
            "<coa_type>": payload['type'],
            "<coa_description>": payload['description'],
            "<coa_created_date>": payload['created_date'],
            "<coa_updated_date>": payload['updated_date']
        }
        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

    def test_happy_path_update_account_description(self, generate_account_request_payload):
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        
        account_insert_record(engine, payload)
        payload['description'] = fake.bs()
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
        payload['created_date'] = now
        payload['updated_date'] = now
        account_update_record(engine, payload['account_id'], payload)
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", ""),
            "<coa_account_id>": payload['account_id'],
            "<coa_name>": payload['name'],
            "<coa_type>": payload['type'],
            "<coa_description>": payload['description'],
            "<coa_created_date>": payload['created_date'],
            "<coa_updated_date>": payload['updated_date']
        }
        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

    def test_happy_path_update_account_mapping(self, generate_account_request_payload):
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        
        account_insert_record(engine, payload)
        payload['account_mapping'] = ''.join(random.choices(string.digits, k=6))
        while payload['account_mapping'] == payload['account_id']:
            payload['account_mapping'] = ''.join(random.choices(string.digits, k=6))
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
        payload['created_date'] = now
        payload['updated_date'] = now
        account_update_record(engine, payload['account_id'], payload)
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", ""),
            "<coa_account_id>": payload['account_id'],
            "<coa_name>": payload['name'],
            "<coa_type>": payload['type'],
            "<coa_description>": payload['description'],
            "<coa_account_mapping>": payload['account_mapping'],
            "<coa_created_date>": payload['created_date'],
            "<coa_updated_date>": payload['updated_date']
        }
        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

    def test_update_nonexistent_record(self, generate_account_request_payload):
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
        payload['created_date'] = now
        payload['updated_date'] = now
        account_update_record(engine, ''.join(random.choices(string.digits, k=6)), payload)
        where_clause_values = {
            "<coa_id>": str(payload['id']).replace("-", ""),
            "<coa_account_id>": payload['account_id'],
            "<coa_name>": payload['name'],
            "<coa_type>": payload['type'],
            "<coa_description>": payload['description'],
            "<coa_created_date>": payload['created_date'],
            "<coa_updated_date>": payload['updated_date']
        }
        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 0