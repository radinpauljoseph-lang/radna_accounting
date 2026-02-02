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
from ..core.transaction_ids.transaction_ids import TransactionIdsCore
from ..validators.accounting_periods import AccountingPeriodsModel
from ..validators.transaction_ids import TransactionIdsModel
from ..validators.data_model import DATA_KEY
from ..models.accounting_periods import (
    acp_meta,
    acp_status
)

FIRST_ID = "00001"
class AccountingPeriodsControllerMetaData:
    def __init__(self):
        self.ACCOUNTING_PERIODS_CONTROLLER = "AccountingPeriodsController"
        self.CREATE_ACCOUNTING_PERIOD = "createAccountingPeriod"
    
acp_controller_meta = AccountingPeriodsControllerMetaData()

class AccountingPeriodsController:
    def __init__(self, rrn = None):
        self.validator_model = AccountingPeriodsModel
        self.engine = engine
        self.core_model = AccountingPeriodsCore
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
        if not accounting_period_exists:
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
        else:
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}0102"))
            del core_model
            raise Exception(error)
        loggerOutput(rrn=self.rrn, message=f"{acp_controller_meta.ACCOUNTING_PERIODS_CONTROLLER}.{acp_controller_meta.CREATE_ACCOUNTING_PERIOD} - Done Creating Accounting Period")
        del core_model
        return return_data