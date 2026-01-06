import copy
import uuid
from datetime import datetime

from ..utils.decorators.error_handling import catchAndLog
from ..configs.config import (
    logger_types,
    loggerOutput,
    engine
)
from ..validators.chart_of_accounts import ChartOfAccountsModel
from ..configs.response_codes.mapping import (
    COA_CODE,
    MESSAGE_KEY,
    error_map
)
from ..core.chart_of_accounts.chart_of_accounts import (
    ChartOfAccountsCore
)
from ..validators.data_model import DATA_KEY
from ..models.chart_of_accounts import coa_meta
from ..core.chart_of_accounts.record_operations import (
    account_record_value_validate,
    account_select_record,
    account_insert_record,
    account_update_record
)

@catchAndLog(Exception, TypeError, ValueError, BaseException)
class ChartOfAccountsController:
    def __init__(self, rrn = None):
        self.validator_model = ChartOfAccountsModel
        self.engine = engine
        self.core_model = ChartOfAccountsCore
        self.rrn = rrn

    def create_account(self, obj) -> dict:
        return_data = {}
        try:
            account_obj = self.validator_model(**obj)
            account_obj = account_obj.model_dump()
            core_model = self.core_model(self.rrn)

            account_id_exists = core_model.selectRecordById(account_obj[coa_meta.ACCOUNT_ID])
            account_name_exists = core_model.selectRecordByName(account_obj[coa_meta.NAME])
            if not account_id_exists and not account_name_exists:
                record = copy.deepcopy(account_obj)
                if record[coa_meta.ACCOUNT_MAPPING] is not None:
                    if record[coa_meta.ACCOUNT_MAPPING] == record[coa_meta.ACCOUNT_ID]:
                        raise Exception("account_mapping should not be the same as Account ID")
                    account_mapping_id_exists = core_model.selectRecordById(account_obj[coa_meta.ACCOUNT_MAPPING])
                    if not account_mapping_id_exists:
                        raise Exception("Account Map Not Found")
                    
                core_model.insertRecord(record)
                record = core_model.selectRecordById(record[coa_meta.ACCOUNT_ID])
                return_data = record
                loggerOutput(message=f"create_account - {return_data}")
            else:
                return_data = {
                    "error": "create_account - Account already exists"
                }
        except TypeError as e:
            loggerOutput(method=logger_types.ERROR, message=f"create_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            loggerOutput(method=logger_types.ERROR, message=f"create_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            loggerOutput(message=f"DONE: create_account - {return_data}")
            return return_data
    
    @catchAndLog(Exception, TypeError, ValueError, BaseException)
    def update_account(self, id, obj) -> dict:
        return_data = {}
        allowed_fields = [
            coa_meta.NAME,
            coa_meta.TYPE,
            coa_meta.DESCRIPTION,
            coa_meta.ACCOUNT_MAPPING
        ]

        loggerOutput(rrn=self.rrn, message=f"ChartOfAccountsController.update_account - Start Updating Account")        
        temp_obj = copy.deepcopy(obj)
        temp_obj[coa_meta.ACCOUNT_ID] = id
        account_obj = self.validator_model(**temp_obj)
        account_obj = account_obj.model_dump()
        core_model = self.core_model(self.rrn)

        account_id_exists = core_model.selectRecordById(id)
        if account_id_exists:
            record = copy.deepcopy(account_id_exists[DATA_KEY])
            record[coa_meta.ACCOUNT_MAPPING] = account_obj[coa_meta.ACCOUNT_MAPPING]
            record = self.validator_model(**record)
            record = record.model_dump()
            for key in obj.keys():
                if key not in allowed_fields:
                    error = copy.deepcopy(error_map.get(f"{COA_CODE}0102"))
                    error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                        key=key
                    )
                    raise Exception(error)
                    
            if account_obj[coa_meta.NAME] != record[coa_meta.NAME]:
                account_name_exists = core_model.selectRecordByName(account_obj[coa_meta.NAME])
                if account_name_exists:
                    error = copy.deepcopy(error_map.get(f"{COA_CODE}0103"))
                    error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                        account_name=account_obj[coa_meta.NAME]
                    )
                    raise Exception(error)
            
            account_mapping_id_exists = core_model.selectRecordById(record[coa_meta.ACCOUNT_MAPPING])
            if not account_mapping_id_exists:
                error = copy.deepcopy(error_map.get(f"{COA_CODE}0104"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    account_mapping=record[coa_meta.ACCOUNT_MAPPING]
                )
                raise Exception(error)
                
            for key in account_obj.keys():
                if key in allowed_fields:
                    record[key] = account_obj[key]
                
            core_model.updateRecordById(id, record)
            record = core_model.selectRecordById(id)
            return_data = record
            loggerOutput(rrn=self.rrn, message=f"ChartOfAccountsController.update_account - {return_data}")
        else:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0101"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                account_id=id
            )
            raise Exception(error)
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
                    loggerOutput(message=f"get_account - {return_data}")
                    break
            else:
                return_data = {
                    "error": "get_account - Account Not Found"
                }
        except TypeError as e:
            loggerOutput(method=logger_types.ERROR, message=f"get_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            loggerOutput(method=logger_types.ERROR, message=f"get_account - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            loggerOutput(message=f"DONE: get_account - {return_data}")
            return return_data

        

    
