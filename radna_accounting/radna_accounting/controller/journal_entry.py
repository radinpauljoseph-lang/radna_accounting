import copy
import uuid
from datetime import datetime

from ..configs.config import (
    logger, 
    engine
)
from ..validators.journal_entry import JournalEntryModel

from ..core.chart_of_accounts.record_operations import account_select_all_account_records 
from ..core.journal_entry.record_operations import (
    je_record_value_validate,
    je_select_record,
    je_select_multiple_record,
    je_select_transaction_id_distinct_values,
    je_insert_record,
    je_update_record
)

class JournalEntryController:
    def __init__(self):
        self.validator_model = JournalEntryModel
        self.engine = engine

    def create_journal_entry(self, obj) -> dict:
        return_data = {}
        try:
            logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@")
            logger.info(obj)
            je_obj = self.validator_model(**obj)
            logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@")
            je_obj = je_obj.model_dump()
            logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@")
            je_obj['id'] = uuid.uuid4()
            logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@")
            je_exists = je_record_value_validate(self.engine, 'id', je_obj['id'])
            logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # je_trans_id_values = je_select_transaction_id_distinct_values(self.engine)
            # logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # logger.info(je_trans_id_values.head())
            if not je_exists:
                record = copy.deepcopy(je_obj)
                del record['created_date']
                del record['updated_date']
                logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@")
                account_numbers = account_select_all_account_records(self.engine)
                logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@")
                account_numbers_filtered = account_numbers[account_numbers['account_id'] == record['account_number']]
                is_account_number_exists = True if account_numbers_filtered.shape[0] == 1 else False
                if not is_account_number_exists:
                    raise Exception("account number does not exist")
                    
                je_insert_record(self.engine, record)
                record = je_select_record(self.engine, record['id'])
                logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@")
                logger.info(record)
                record = self.validator_model(**record)
                record = record.model_dump()
                return_data = {
                    "data": record
                }
                logger.info(f"create_journal_entry - {return_data}")
            else:
                return_data = {
                    "error": "create_journal_entry - Journal Entry already exists"
                }
        except TypeError as e:
            logger.error(f"create_journal_entry - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"create_journal_entry - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: create_journal_entry - {return_data}")
            return return_data
    
    def update_journal_entry(self, id, obj) -> dict:
        return_data = {}
        try:
            id_value = str(id)
            temp_obj = copy.deepcopy(obj)
            temp_obj['account_id'] = id_value
            account_obj = self.validator_model(**temp_obj)
            account_obj = account_obj.model_dump()
            allowed_fields = [
                'name',
                'type',
                'description',
                'account_mapping'
            ]
            account_id_exists = account_record_value_validate(self.engine, 'account_id', id_value, False)
            if account_id_exists:
                record = account_select_record(self.engine, 'account_id', id_value)
                record = self.validator_model(**record)
                record = record.model_dump()
                for key in obj.keys():
                    if key not in allowed_fields:
                        return_data = {
                            "error": f"update_account - {key} field not allowed"
                        }
                        raise Exception(f"{key} field not allowed")
                    
                if account_obj['name'] != record['name']:
                    account_name_exists = account_record_value_validate(self.engine, 'name', obj['name'], True)
                    if account_name_exists:
                        raise Exception("update_account - Account Name already exists")
                
                if account_obj['account_mapping'] is not None:
                    if account_obj['account_mapping'] == record['account_id']:
                        raise Exception("account_mapping should not be the same as account_id")
                    account_id_exists = account_record_value_validate(self.engine, 'account_id', account_obj['account_mapping'])
                    if not account_id_exists:
                        raise Exception("Account Map Not Found")
                    
                now = datetime.now()
                now = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
                record['updated_date'] = now
                for key in account_obj.keys():
                    if key in allowed_fields:
                        record[key] = account_obj[key]
                    
                account_update_record(self.engine, id_value, record)
                record = account_select_record(self.engine, 'account_id', id_value)
                record = self.validator_model(**record)
                record = record.model_dump()

                return_data = {
                    "data": record
                }
                logger.info(f"update_account - {return_data}")
            else:
                return_data = {
                    "error": "update_account - Account Not Found"
                }
        except TypeError as e:
            logger.error(f"update_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except ValueError as e:
            logger.error(f"update_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"update_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: update_account - {return_data}")
            return return_data

    def get_account(self, id) -> dict:
        return_data = {}
        try:
            value = str(id)

            search_cols = [
                'account_id'
            ]

            for col in search_cols:
                record_exists = account_record_value_validate(self.engine, col, value)
                if record_exists:
                    account_obj = account_select_record(self.engine, col, value)
                    account_obj = self.validator_model(**account_obj)
                    account_obj = account_obj.model_dump()
                    return_data = {
                        "data": account_obj
                    }
                    logger.info(f"get_account - {return_data}")
                    break
            else:
                return_data = {
                    "error": "get_account - Account Not Found"
                }
        except TypeError as e:
            logger.error(f"get_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"get_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: get_account - {return_data}")
            return return_data

        

    
