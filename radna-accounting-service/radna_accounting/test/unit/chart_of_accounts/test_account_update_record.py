import pytest
from faker import Faker
import logging
from datetime import datetime, timezone
from radna_accounting.models.chart_of_accounts import *
from radna_accounting.validators.chart_of_accounts import (
    ChartOfAccountsModel,
    account_types
)
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.models.chart_of_accounts import (
    coa_meta,
    coa_types
)

from radna_accounting.test.utils.db.connector import (
    SQLiteClient
)
from radna_accounting.test.utils.helpers import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


creds = {
    "file_name": "temp_state.db"
}

class TestAccounUpdateRecord:
    def test_happy_path_update_name(self, generate_account_request_payload):
        account_name = Faker().bs()
        core_model = ChartOfAccountsCore()
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"

        core_model.insertRecord(payload)
        updated_datetime = datetime.now(timezone.utc)
        updated_datetime = updated_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(updated_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID],
            "<coa_name>": account_name,
            "<coa_type>": payload[coa_meta.TYPE],
            "<coa_description>": payload[coa_meta.DESCRIPTION],
            "<coa_created_date>": current_datetime,
            "<coa_updated_date>": updated_datetime
        }

        payload[coa_meta.NAME] = account_name
        core_model.updateRecordById(payload[coa_meta.ACCOUNT_ID], payload)

        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1
    
    def test_happy_path_update_description_none(self, generate_account_request_payload):
        account_description = Faker().bs()
        core_model = ChartOfAccountsCore()
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"

        core_model.insertRecord(payload)
        updated_datetime = datetime.now(timezone.utc)
        updated_datetime = updated_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(updated_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID],
            "<coa_name>": payload[coa_meta.NAME],
            "<coa_type>": payload[coa_meta.TYPE],
            "<coa_description>": account_description,
            "<coa_created_date>": current_datetime,
            "<coa_updated_date>": updated_datetime
        }

        payload[coa_meta.DESCRIPTION] = None
        core_model.updateRecordById(payload[coa_meta.ACCOUNT_ID], payload)

        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test with description equal to Null", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

    def test_happy_path_update_description(self, generate_account_request_payload):
        account_description = Faker().bs()
        core_model = ChartOfAccountsCore()
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"

        core_model.insertRecord(payload)
        updated_datetime = datetime.now(timezone.utc)
        updated_datetime = updated_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(updated_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID],
            "<coa_name>": payload[coa_meta.NAME],
            "<coa_type>": payload[coa_meta.TYPE],
            "<coa_description>": account_description,
            "<coa_created_date>": current_datetime,
            "<coa_updated_date>": updated_datetime
        }

        payload[coa_meta.DESCRIPTION] = account_description
        core_model.updateRecordById(payload[coa_meta.ACCOUNT_ID], payload)

        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

    @pytest.mark.parametrize("param", [coa_types.ASSET, coa_types.LIABILITY, coa_types.EQUITY, coa_types.LIABILITY, coa_types.REVENUE, coa_types.COST])
    def test_happy_path_update_account_type(self, generate_account_request_payload, param):
        core_model = ChartOfAccountsCore()
        payload = generate_account_request_payload
        payload = ChartOfAccountsModel(**payload).model_dump()
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"

        core_model.insertRecord(payload)
        updated_datetime = datetime.now(timezone.utc)
        updated_datetime = updated_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(updated_datetime.microsecond / 1000):03d}"
        where_clause_values = {
            "<coa_account_id>": payload[coa_meta.ACCOUNT_ID],
            "<coa_name>": payload[coa_meta.NAME],
            "<coa_type>": param,
            "<coa_description>": payload[coa_meta.DESCRIPTION],
            "<coa_created_date>": current_datetime,
            "<coa_updated_date>": updated_datetime
        }

        payload[coa_meta.TYPE] = param
        core_model.updateRecordById(payload[coa_meta.ACCOUNT_ID], payload)

        contents = load_mapped_sql_files("Chart Of Accounts", "Uniqueness Test", where_clause_values)
        db_obj = SQLiteClient(creds)
        db_obj.set_sql_command(contents["sql"])\
            .set_columns(contents["columns"])
        result = db_obj.execute()\
            .get_data()
        del db_obj

        assert result.shape[0] == 1

    def test_duplicate_name_error(self):
        expected = "UNIQUE constraint failed"
        core_model = ChartOfAccountsCore()
        current_datetime = datetime.now(timezone.utc)
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
        first_record = None
        second_record = None
        for index in range(2):
            now = datetime.now(timezone.utc)
            payload = {
                coa_meta.ACCOUNT_ID: ''.join(random.choices(string.digits, k=6)),
                coa_meta.NAME: fake.bs(),
                coa_meta.TYPE: account_types[random.randrange(0, len(account_types))],
                coa_meta.DESCRIPTION: fake.bs(),
                coa_meta.ACCOUNT_MAPPING: None,
                coa_meta.CREATED_DATE: now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond / 1000):03d}",
                coa_meta.UPDATED_DATE: now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond / 1000):03d}"
            }
            payload = ChartOfAccountsModel(**payload).model_dump()
            core_model.insertRecord(payload)
            if index == 0:
                first_record = payload
            else:
                second_record = payload

        second_record[coa_meta.NAME] = first_record[coa_meta.NAME]
        with pytest.raises(Exception) as excinfo:
            core_model.updateRecordById(second_record[coa_meta.ACCOUNT_ID], second_record)
        logging.info(str(excinfo))
        assert expected in str(excinfo)

    def test_using_nonexistent_record_value(self, generate_account_request_payload):
            core_model = ChartOfAccountsCore()
            payload = generate_account_request_payload
            payload = ChartOfAccountsModel(**payload).model_dump()
            expected = "COA0101"
            
            with pytest.raises(Exception) as excinfo:
                core_model.updateRecordById(payload[coa_meta.ACCOUNT_ID], payload)
            logging.info(str(excinfo))
            assert expected in str(excinfo)

