import copy

from ..utils.decorators.error_handling import catchAndLog
from ..configs.config import (
    logger_types,
    loggerOutput,
    engine
)
from ..configs.response_codes.mapping import (
    ACP_CODE,
    MESSAGE_KEY,
    error_map
)
from ..core.accounting_periods.accounting_periods import AccountingPeriodsCore
from ..core.journal_entry.journal_entry import JournalEntryCore
from ..core.transaction_ids.transaction_ids import TransactionIdsCore
from ..validators.accounting_periods import AccountingPeriodsModel
from ..validators.transaction_ids import TransactionIdsModel
from ..validators.data_model import DATA_KEY
from ..models.accounting_periods import (
    acp_meta,
    acp_status
)
from ..models.journal_entry import (
    je_meta,
    je_status
)
from ..models.transaction_ids import ti_meta

FIRST_ID = "00001"

class AccountingPeriodsControllerMetaData:
    def __init__(self):
        self.ACCOUNTING_PERIODS_CONTROLLER = "AccountingPeriodsController"
        self.CREATE_ACCOUNTING_PERIOD = "createAccountingPeriod"
        self.CLOSE_ACCOUNTING_PERIOD = "closeAccountingPeriod"
    
acp_controller_meta = AccountingPeriodsControllerMetaData()

class AccountingPeriodsController:
    def __init__(self, rrn = None):
        self.validator_model = AccountingPeriodsModel
        self.engine = engine
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
        acp_obj = acp_obj.model_dump()

        core_model = self.core_model(self.rrn)
        ti_core_model = self.ti_core_model(self.rrn)
            
        accounting_period_exists = core_model.selectRecord(
            month=acp_obj[acp_meta.MONTH],
            year=acp_obj[acp_meta.YEAR]
        )
        if accounting_period_exists:
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}0102"))
            raise Exception(error)
        record = copy.deepcopy(acp_obj)

        core_model.insertRecord(record)
        record = core_model.selectRecord(
            month=acp_obj[acp_meta.MONTH],
            year=acp_obj[acp_meta.YEAR]
        )
        ti_core_model.insertRecord(
            TransactionIdsModel(
                month=acp_obj[acp_meta.MONTH],
                year=acp_obj[acp_meta.YEAR],
                id=FIRST_ID
            ).model_dump()
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
        ti_core_model = self.ti_core_model(rrn=self.rrn)

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

        if DATA_KEY in journal_entries.keys():
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

                    


        
                
        
