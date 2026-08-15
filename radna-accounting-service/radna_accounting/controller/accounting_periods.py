import copy

from radna_accounting.utils.decorators.error_handling import catchAndLog
from radna_accounting.configs.config import (
    logger_types,
    loggerOutput,
    engine
)
from radna_accounting.configs.response_codes.mapping import (
    ACP_CODE,
    MESSAGE_KEY,
    error_map
)
from radna_accounting.core.accounting_periods.accounting_periods import AccountingPeriodsCore
from radna_accounting.core.journal_entry.journal_entry import JournalEntryCore
from radna_accounting.core.transaction_ids.transaction_ids import TransactionIdsCore
from radna_accounting.validators.accounting_periods import AccountingPeriodsModel
from radna_accounting.validators.transaction_ids import (
    TransactionIdsModel,
    FIRST_ID
)
from radna_accounting.validators.data_model import DATA_KEY
from radna_accounting.models.accounting_periods import (
    acp_meta,
    acp_status
)
from radna_accounting.models.journal_entry import (
    je_meta,
    je_status
)
from radna_accounting.models.transaction_ids import ti_meta

class AccountingPeriodsControllerMetaData:
    def __init__(self):
        self.ACCOUNTING_PERIODS_CONTROLLER = "AccountingPeriodsController"
        self.CREATE_ACCOUNTING_PERIOD = "createAccountingPeriod"
        self.CLOSE_ACCOUNTING_PERIOD = "closeAccountingPeriod"
    
acp_controller_meta = AccountingPeriodsControllerMetaData()

class AccountingPeriodsController:
    def __init__(self, rrn = None):
        self.validator_model = AccountingPeriodsModel
        self.core_model = AccountingPeriodsCore
        self.je_core_model = JournalEntryCore
        self.ti_core_model = TransactionIdsCore
        self.rrn = rrn

    @catchAndLog(Exception)
    def createAccountingPeriod(self, obj) -> dict:
        loggerOutput(rrn=self.rrn, message=f"{acp_controller_meta.ACCOUNTING_PERIODS_CONTROLLER}.{acp_controller_meta.CREATE_ACCOUNTING_PERIOD} - Start Creating Accounting Period")
        return_data = {}
        acp_obj = copy.deepcopy(obj)
        acp_obj[acp_meta.STATUS] = acp_status.OPEN

        acp_obj = self.validator_model(**acp_obj)

        core_model = self.core_model(self.rrn)
        ti_core_model = self.ti_core_model(self.rrn)
            
        accounting_period_exists = core_model.selectRecord(
            month=acp_obj.month,
            year=acp_obj.year
        )
        if accounting_period_exists:
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}0102"))
            raise Exception(error)
        record = copy.deepcopy(acp_obj)

        core_model.insertRecord(record)
        ti_core_model.insertRecord(
            TransactionIdsModel(
                month=acp_obj.month,
                year=acp_obj.year,
                id=FIRST_ID
            ).model_dump()
        )
        record = core_model.selectRecord(
            month=acp_obj.month,
            year=acp_obj.year
        )
        return_data = record

        loggerOutput(rrn=self.rrn, message=f"{acp_controller_meta.ACCOUNTING_PERIODS_CONTROLLER}.{acp_controller_meta.CREATE_ACCOUNTING_PERIOD} - Done Creating Accounting Period")
        return return_data
    
    @catchAndLog(Exception)
    def closeAccountingPeriod(self, obj: dict) -> dict:
        return_data = {}
        temp_obj = copy.deepcopy(obj)
        acp_obj = self.validator_model(
            month=temp_obj[acp_meta.MONTH],
            year=temp_obj[acp_meta.YEAR]
        ).model_dump()
        core_model = self.core_model(rrn=self.rrn)
        je_core_model = self.je_core_model(rrn=self.rrn)

        data = core_model.selectRecord(
            month=acp_obj[acp_meta.MONTH],
            year=acp_obj[acp_meta.YEAR]
        )

        if data is None:
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}0103"))
            raise Exception(error)
        
        data = data[DATA_KEY]

        if data[acp_meta.STATUS] == acp_status.CLOSED:
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}0101"))
            raise Exception(error)
        
        journal_entries = je_core_model.selectRecordsByMonthYear(
            month=data[acp_meta.MONTH],
            year=data[acp_meta.YEAR]
        )
        
        journal_entries = journal_entries[DATA_KEY]
        for entry in journal_entries:
            if entry[je_meta.STATUS] != je_status.POSTED:
                error = copy.deepcopy(error_map.get(f"{ACP_CODE}0104"))
                raise Exception(error)
                    
        core_model.closeAccountingPeriod(
            month=acp_obj[acp_meta.MONTH],
            year=acp_obj[acp_meta.YEAR]
        )
        record = core_model.selectRecord(
            month=acp_obj[acp_meta.MONTH],
            year=acp_obj[acp_meta.YEAR]
        )
        return_data = record

        loggerOutput(rrn=self.rrn, message=f"{acp_controller_meta.ACCOUNTING_PERIODS_CONTROLLER}.{acp_controller_meta.CREATE_ACCOUNTING_PERIOD} - Done Creating Accounting Period")
        return return_data

                    


        
                
        
