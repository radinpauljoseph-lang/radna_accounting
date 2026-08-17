import copy
import re
from datetime import datetime
from radna_accounting.configs.config  import (
    logger_types,
    loggerOutput
)

from radna_accounting.configs.config import engine
from radna_accounting.configs.response_codes.mapping import (
    ACP_CODE,
    MESSAGE_KEY,
    error_map
)
from radna_accounting.models.accounting_periods import (
    acp_meta,
    acp_status,
    accounting_periods,
    accounting_periods_history
)
from radna_accounting.validators.accounting_periods import (
    AccountingPeriodsModel,
    AccountingPeriodsHistoryModel
)
from radna_accounting.validators.data_model import (
    DATA_KEY,
    DataModel
)

class AccountingPeriodsCoreMetaData:
    def __init__(self):
        self.ACCOUNTING_PERIODS_CORE = "AccountingPeriodsCore"
        self.INSERT_RECORD = "insertRecord"
        self.SELECT_RECORD = "selectRecord"
        self.CLOSE_ACCOUNTING_PERIOD = "closeAccountingPeriod"

acp_core_meta = AccountingPeriodsCoreMetaData()

class AccountingPeriodsCore:
    def __init__(self, rrn = None):
        self.__dto_model = AccountingPeriodsModel
        self.__history_model = AccountingPeriodsHistoryModel
        self.__engine = engine
        self.__rrn = rrn

    def insertRecord(self, obj: AccountingPeriodsModel) -> None:
        new_record = None

        self.__dto_model(**obj.model_dump())

        loggerOutput(rrn=self.__rrn, message=f"{acp_core_meta.ACCOUNTING_PERIODS_CORE}.{acp_core_meta.INSERT_RECORD} - Start Insert Accounting Period Record {obj}")

        accounting_period_exists = self.selectRecord(
            month=obj.month,
            year=obj.year
        )
        if accounting_period_exists:
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}0102"))
            raise Exception(error)
        
        with self.__engine.connect() as conn:
            new_record = copy.deepcopy(obj)
            new_record.created_date = datetime.now()
            new_record.updated_date = new_record.created_date

            history_record = copy.deepcopy(new_record.model_dump())
            history_record[acp_meta.HISTORY_OPERATION] = "I"
            history_record = self.__history_model(**history_record)

            insert_statement = accounting_periods\
                .insert()\
                .values(**new_record.model_dump())
            
            history_insert_statement = accounting_periods_history\
                .insert()\
                .values(**history_record.model_dump())
            
            conn.execute(insert_statement)
            conn.execute(history_insert_statement)
            conn.commit()
        
        loggerOutput(rrn=self.__rrn, message=f"{acp_core_meta.ACCOUNTING_PERIODS_CORE}.{acp_core_meta.INSERT_RECORD} - Done Insert Accounting Period Record {obj}")
    
    def selectRecord(self, month: int, year: int) -> dict:
        validator = None
        result = None

        loggerOutput(rrn=self.__rrn, message=f"{acp_core_meta.ACCOUNTING_PERIODS_CORE}.{acp_core_meta.SELECT_RECORD} - Start Select Record")

        ti_obj = AccountingPeriodsModel(
            month=month,
            year=year
        ).model_dump()
        with self.__engine.connect() as conn:
            validator = accounting_periods\
                .select()\
                .where(
                    (accounting_periods.c.month == ti_obj[acp_meta.MONTH]) &
                    (accounting_periods.c.year == ti_obj[acp_meta.YEAR])
                )
            result = conn.execute(validator)

        result = result.first()
        if result is not None:
            result = dict(result._mapping)
            result = self.__dto_model(**result).model_dump()
            result = DataModel(data=result).model_dump()
            loggerOutput(rrn=self.__rrn, message=f"{acp_core_meta.ACCOUNTING_PERIODS_CORE}.{acp_core_meta.SELECT_RECORD} - {result}")
        return result
    
    def closeAccountingPeriod(self, month: int, year: int) -> None:
        loggerOutput(rrn=self.__rrn, message=f"{acp_core_meta.ACCOUNTING_PERIODS_CORE}.{acp_core_meta.CLOSE_ACCOUNTING_PERIOD} - Start Close Accounting Period Record")
        record = self.selectRecord(
            month=month,
            year=year
        )

        if record is None:
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}0103"))
            raise Exception(error)
        
        record = record[DATA_KEY]
        
        if record[acp_meta.STATUS] != acp_status.CLOSED:
            record[acp_meta.UPDATED_DATE] = datetime.now()
            record[acp_meta.STATUS] = acp_status.CLOSED

            history_record = copy.deepcopy(record)
            history_record[acp_meta.HISTORY_OPERATION] = "U"
            history_record = self.__history_model(**history_record).model_dump()
            with self.__engine.connect() as conn:
                history_record[acp_meta.CREATED_DATE] = record[acp_meta.CREATED_DATE]

                update_statement = accounting_periods\
                    .update()\
                    .where(
                        (accounting_periods.c.month == record[acp_meta.MONTH]) &
                        (accounting_periods.c.year == record[acp_meta.YEAR])
                    )\
                    .values(**record)
                history_insert_statement = accounting_periods_history\
                    .insert()\
                    .values(**history_record)
                
                conn.execute(update_statement)
                conn.execute(history_insert_statement)
                conn.commit()
                loggerOutput(rrn=self.__rrn, message=f"{acp_core_meta.ACCOUNTING_PERIODS_CORE}.{acp_core_meta.CLOSE_ACCOUNTING_PERIOD} - Done Close Accounting Period Record")
        else:
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}0101"))
            raise Exception(error)
    

        

