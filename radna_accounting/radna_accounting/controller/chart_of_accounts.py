import copy
import uuid
from datetime import datetime

from ..configs.config import (
    logger, 
    engine
)
from ..validators.chart_of_accounts import ChartOfAccountsModel
from ..core.chart_of_accounts.record_operations import (
    account_record_value_validate,
    account_select_record,
    account_insert_record,
    account_update_record
)

class ChartOfAccountsController:
    def __init__(self):
        self.validator_model = ChartOfAccountsModel
        self.engine = engine
    def create_account(self, obj) -> dict:
        return_data = {}
        try:
            account_obj = self.validator_model(**obj)
            account_obj = account_obj.model_dump()
            account_obj['id'] = uuid.uuid4()

            account_id_exists = account_record_value_validate(self.engine, 'account_id', account_obj['account_id'])
            account_name_exists = account_record_value_validate(self.engine, 'name', account_obj['name'])
            if not account_id_exists and not account_name_exists:
                record = copy.deepcopy(account_obj)
                del record['created_date']
                del record['updated_date']
                if record['account_mapping'] is not None:
                    if record['account_mapping'] == str(record['account_id']):
                        raise Exception("account_mapping should not be the same as account_id")
                    account_id_exists = account_record_value_validate(self.engine, 'account_id', record['account_mapping'])
                    if not account_id_exists:
                        raise Exception("Account Map Not Found")
                    
                account_insert_record(self.engine, record)
                record = account_select_record(self.engine, 'account_id', record['account_id'])
                record = self.validator_model(**record)
                record = record.model_dump()
                return_data = {
                    "data": record
                }
                logger.info(f"create_account - {return_data}")
            else:
                return_data = {
                    "error": "create_account - Account already exists"
                }
        except TypeError as e:
            logger.error(f"create_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"create_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: create_account - {return_data}")
            return return_data
    
    def update_account(self, id, obj) -> dict:
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

        

    
