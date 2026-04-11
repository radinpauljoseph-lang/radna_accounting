import copy

from radna_accounting.utils.decorators.error_handling import catchAndLog
from radna_accounting.configs.config import (
    logger_types,
    loggerOutput,
    engine
)
from radna_accounting.configs.response_codes.mapping import (
    COA_CODE,
    MESSAGE_KEY,
    error_map
)
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.validators.chart_of_accounts import ChartOfAccountsModel
from radna_accounting.validators.data_model import DATA_KEY
from radna_accounting.models.chart_of_accounts import coa_meta

class ChartOfAccountsControllerMetaData:
    def __init__(self):
        self.CHART_OF_ACCOUNTS_CONTROLLER = "ChartOfAccountsController"
        self.CREATE_ACCOUNT = "createAccount"
        self.UPDATE_ACCOUNT = "updateAccount"
        self.GET_ACCOUNT = "getAccount"

coa_controller_meta = ChartOfAccountsControllerMetaData()

class ChartOfAccountsController:
    def __init__(self, rrn = None):
        self.validator_model = ChartOfAccountsModel
        self.core_model = ChartOfAccountsCore
        self.rrn = rrn

    @catchAndLog(Exception)
    def createAccount(self, obj: dict) -> dict:
        loggerOutput(rrn=self.rrn, message=f"{coa_controller_meta.CHART_OF_ACCOUNTS_CONTROLLER}.{coa_controller_meta.CREATE_ACCOUNT} - Start Creating Account")
        return_data = {}
        account_obj = self.validator_model(**obj)
        core_model = self.core_model(self.rrn)
        
        account_id_exists = core_model.selectRecordById(account_obj.account_id)
        account_name_exists = core_model.selectRecordByName(account_obj.name)
        if not account_id_exists and not account_name_exists:
            record = copy.deepcopy(account_obj)

            account_mapping_id_exists = core_model.selectRecordById(record.account_mapping)
            if not account_mapping_id_exists and record.account_mapping is not None:
                error = copy.deepcopy(error_map.get(f"{COA_CODE}0104"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    account_mapping=record.account_mapping
                )
                del core_model
                raise Exception(error)
                    
            core_model.insertRecord(record)
            record = core_model.selectRecordById(record.account_id)
            return_data = record
        else:
            del core_model
            if account_name_exists:
                error = copy.deepcopy(error_map.get(f"{COA_CODE}0103"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    account_name=account_obj.name
                )
                raise Exception(error)
            else:
                error = copy.deepcopy(error_map.get(f"{COA_CODE}0105"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    account_id=account_obj.account_id
                )
                raise Exception(error)
            
        loggerOutput(rrn=self.rrn, message=f"{coa_controller_meta.CHART_OF_ACCOUNTS_CONTROLLER}.{coa_controller_meta.CREATE_ACCOUNT} - Done Creating Account")
        del core_model
        return return_data
    
    @catchAndLog(Exception)
    def updateAccount(self, id: str, obj: dict) -> dict:
        return_data = {}
        allowed_fields = [
            coa_meta.NAME,
            coa_meta.TYPE,
            coa_meta.DESCRIPTION,
            coa_meta.ACCOUNT_MAPPING
        ]

        loggerOutput(rrn=self.rrn, message=f"{coa_controller_meta.CHART_OF_ACCOUNTS_CONTROLLER}.{coa_controller_meta.UPDATE_ACCOUNT} - Start Updating Account")  
        core_model = self.core_model(self.rrn)

        account_id_exists = core_model.selectRecordById(id)
        if account_id_exists:
            temp_obj = copy.deepcopy(obj)
            temp_obj[coa_meta.ACCOUNT_ID] = id
            account_obj = self.validator_model(**temp_obj).model_dump()

            record = copy.deepcopy(account_id_exists[DATA_KEY])
            record[coa_meta.ACCOUNT_MAPPING] = account_obj[coa_meta.ACCOUNT_MAPPING]
            
            for key in obj.keys():
                if key not in allowed_fields:
                    error = copy.deepcopy(error_map.get(f"{COA_CODE}0102"))
                    error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                        key=key
                    )
                    del core_model
                    raise Exception(error)
                
            if account_obj[coa_meta.NAME] != record[coa_meta.NAME]:
                account_name_exists = core_model.selectRecordByName(account_obj[coa_meta.NAME])
                if account_name_exists:
                    error = copy.deepcopy(error_map.get(f"{COA_CODE}0103"))
                    error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                        account_name=account_obj[coa_meta.NAME]
                    )
                    del core_model
                    raise Exception(error)
            
            account_mapping_id_exists = core_model.selectRecordById(record[coa_meta.ACCOUNT_MAPPING])
            if not account_mapping_id_exists and record[coa_meta.ACCOUNT_MAPPING] is not None:
                error = copy.deepcopy(error_map.get(f"{COA_CODE}0104"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    account_mapping=record[coa_meta.ACCOUNT_MAPPING]
                )
                del core_model
                raise Exception(error)
            
            for key in account_obj.keys():
                if key in allowed_fields:
                    record[key] = account_obj[key]

            record = self.validator_model(**record)
            core_model.updateRecordById(id, record)
            record = core_model.selectRecordById(id)
            return_data = record
            loggerOutput(rrn=self.rrn, message=f"{coa_controller_meta.CHART_OF_ACCOUNTS_CONTROLLER}.{coa_controller_meta.UPDATE_ACCOUNT} - {return_data}")
        else:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0101"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                account_id=id
            )
            del core_model
            raise Exception(error)
        del core_model
        return return_data
    
    @catchAndLog(Exception)
    def getAccount(self, id: str) -> dict:
        return_data = {}
        core_model = self.core_model(self.rrn)
        loggerOutput(rrn=self.rrn, message=f"{coa_controller_meta.CHART_OF_ACCOUNTS_CONTROLLER}.{coa_controller_meta.GET_ACCOUNT} - Start Get Account")  
        record = core_model.selectRecordById(id)
        if record is not None:
            return_data = record
        else:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0106"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                account_id=id
            )
            del core_model
            raise Exception(error)
        loggerOutput(rrn=self.rrn, message=f"{coa_controller_meta.CHART_OF_ACCOUNTS_CONTROLLER}.{coa_controller_meta.GET_ACCOUNT} - Done Get Account")  
        del core_model
        return return_data

        

    
