import copy
import uuid
from datetime import datetime

from ..configs.config import (
    logger_types,
    loggerOutput,
    engine
)
from ..validators.accounting_periods import (
    AccountingPeriodsModel
)
from ..validators.transaction_id_tracker import (
    TransactionIdTrackerModel
)
from ..core.accounting_periods.record_operations import (
    accounting_period_select_all_account_records,
    accounting_period_insert_record,
    accounting_period_update_record
)
from ..core.transaction_id_tracker.record_operations import (
    transaction_id_tracker_insert_record
)
from ..core.journal_entry.record_operations import (
    je_select_by_transaction_date_month_year_record
)
class AccountingPeriodsController:
    def __init__(self):
        self.validator_model = AccountingPeriodsModel
        self.transaction_id_tracker_model = TransactionIdTrackerModel
        self.engine = engine
        
    def create_accounting_period(self, obj) -> dict:
        return_data = {}
        is_accounting_period_exists = False
        transaction_id = "00001"
        try:
            accounting_period_obj = self.validator_model(**obj)
            accounting_period_obj = accounting_period_obj.model_dump()
            accounting_periods_df =  accounting_period_select_all_account_records(self.engine)
            if accounting_periods_df.shape[0] >= 1:
                accounting_periods_df = accounting_periods_df[accounting_periods_df['year'] == accounting_period_obj['year']]
                if accounting_periods_df.shape[0] >= 1:
                    accounting_periods_df = accounting_periods_df[accounting_periods_df['month'] == accounting_period_obj['month']]
                is_accounting_period_exists = False if accounting_periods_df.shape[0] == 0 else True

            if not is_accounting_period_exists:
                record = copy.deepcopy(accounting_period_obj)
                record['status'] = "OPEN"
                transaction_id_tracker_record = self.transaction_id_tracker_model(
                    month=record['month'],
                    year=record['year'],
                    id=transaction_id
                ).model_dump()

                accounting_period_insert_record(self.engine, record)
                transaction_id_tracker_insert_record(self.engine, transaction_id_tracker_record)
                return_data = {
                    "data": record
                }
                loggerOutput(message=f"create_accounting_period - {return_data}")
            else:
                return_data = {
                    "error": "create_accounting_period - Accounting Period already exists"
                }
        except TypeError as e:
            loggerOutput(method=logger_types.ERROR, message=f"create_accounting_period - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            loggerOutput(method=logger_types.ERROR, message=f"create_accounting_period - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            loggerOutput(message=f"DONE: create_accounting_period - {return_data}")
            return return_data
    
    def close_accounting_period(self, obj) -> dict:
        return_data = {}
        is_accounting_period_exists = False
        is_accounting_period_closed = True
        try:
            accounting_period_obj = self.validator_model(**obj)
            accounting_period_obj = accounting_period_obj.model_dump()
            accounting_periods_df =  accounting_period_select_all_account_records(self.engine)

            if accounting_periods_df.shape[0] >= 1:
                accounting_periods_df = accounting_periods_df[accounting_periods_df['year'] == accounting_period_obj['year']]
                if accounting_periods_df.shape[0] >= 1:
                    accounting_periods_df = accounting_periods_df[accounting_periods_df['month'] == accounting_period_obj['month']]
                is_accounting_period_exists = False if accounting_periods_df.shape[0] == 0 else True

            if is_accounting_period_exists:
                accounting_periods_df = accounting_periods_df[accounting_periods_df['status'] == 'CLOSED']
                is_accounting_period_closed = True if accounting_periods_df.shape[0] > 0 else False
                    

            if is_accounting_period_exists and not is_accounting_period_closed:
                record = copy.deepcopy(accounting_period_obj)
                record['status'] = "CLOSED"
                je_records = je_select_by_transaction_date_month_year_record(self.engine, record['month'], record['year'])
                if je_records.shape[0] > 0:
                    je_records = je_records[je_records['status'] == "UNPOSTED"]
                    if je_records.shape[0] > 0:
                        raise Exception(f"close_accounting_period - Accounting Period {record['month']:02}-{record['year']} has unposted journal entries")
                
                accounting_period_update_record(self.engine, record)
                return_data = {
                    "data": record
                }
                loggerOutput(message=f"close_accounting_period - {return_data}")
            else:
                return_data = {
                    "error": "close_accounting_period - Accounting Period Not Found or already closed"
                }
        except TypeError as e:
            loggerOutput(method=logger_types.ERROR, message=f"close_accounting_period - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except ValueError as e:
            loggerOutput(method=logger_types.ERROR, message=f"close_accounting_period - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            loggerOutput(method=logger_types.ERROR, message=f"close_accounting_period - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            loggerOutput(message=f"DONE: close_accounting_period - {return_data}")
            return return_data

    