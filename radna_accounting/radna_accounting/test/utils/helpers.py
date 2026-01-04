import pytest
from faker import Faker
import uuid
import string
import random
import copy
from datetime import datetime, timezone
from ...validators.chart_of_accounts import (
    account_types
)
from pathlib import Path
BASE_DIR = str(Path(__file__).resolve().parent)

fake = Faker()

sql_map = {
    "Chart Of Accounts": {
        "Uniqueness Test": {
            "file_path": f"{BASE_DIR}\\db\\sqlite\\chart_of_accounts\\select_coa_uniqueness_test.sql",
            "columns": [
                 "account_id", 
                 "name", 
                 "type", 
                 "description", 
                 "account_mapping", 
                 "created_date", 
                 "updated_date"
            ],
            "parameters": {
                "<coa_id>": "",
                "<coa_account_id>": "",
                "<coa_name>": "",
                "<coa_type>": "",
                "<coa_account_mapping>": "",
                "<coa_description>": "",
                "<coa_created_date>": "",
                "<coa_updated_date>": ""
            }
        },
        "Search By ID": {
            "file_path": f"{BASE_DIR}\\db\\sqlite\\chart_of_accounts\\select_coa_by_id.sql",
            "columns": [
                 "account_id", 
                 "name", 
                 "type", 
                 "description", 
                 "account_mapping", 
                 "created_date", 
                 "updated_date"
            ],
            "parameters": {
                "<coa_id>": ""
            }
        },
        "Search By Type": {
            "file_path": "f{BASE_DIR}\\db\\sqlite\\chart_of_accounts\\select_coa_by_type.sql",
            "columns": [
                 "account_id", 
                 "name", 
                 "type", 
                 "description", 
                 "account_mapping", 
                 "created_date", 
                 "updated_date"
            ],
            "parameters": {
                "<coa_type>": ""
            }
        }
    }
}

def load_mapped_sql_files(table_name, sql_name, params):
    contents = ""
    sql_ref = copy.deepcopy(sql_map[table_name])
    columns = sql_ref[sql_name]['columns']
    file_path = sql_ref[sql_name]['file_path']

    with open(file_path) as file:
         contents = file.read()
         for key, value in params.items():
                contents = contents.replace(key, value)
    return {
         "sql": contents,
         "columns": columns
    }

@pytest.fixture
def generate_account_request_payload():
    current_datetime = datetime.now(timezone.utc)
    input_values = {
        "account_id": ''.join(random.choices(string.digits, k=6)),
        "name": fake.bs(),
        "type": account_types[random.randrange(0, len(account_types))],
        "description": fake.bs(),
        "account_mapping": None,
        "created_date": current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}",
        "updated_date": current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
    }
    return input_values