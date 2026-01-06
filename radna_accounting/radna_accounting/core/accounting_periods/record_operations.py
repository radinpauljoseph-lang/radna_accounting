import copy
import uuid
import pandas as pd
from pandas import DataFrame
from sqlalchemy import text, distinct
from ...configs.config  import (
    logger
)
from ...models.accounting_periods import accounting_periods
from ...validators.accounting_periods import AccountingPeriodsModel

def accounting_period_select_all_account_records(engine) -> DataFrame:
    validator = None
    result = None
    with engine.connect() as conn:
        validator = accounting_periods\
            .select()
        result = conn.execute(validator).fetchall()

        loggerOutput(message=f"accounting_period_select_all_account_records - SQL: {validator}")
    
    result = [dict(row._mapping) for row in result]
    result = pd.DataFrame(result)
    return result

def accounting_period_insert_record(engine, obj) -> None:
    with engine.connect() as conn:
        loggerOutput(message=f"accounting_period_insert_record - Start Insert Account Period Record {obj}")
        new_record = AccountingPeriodsModel(**obj).model_dump()

        insert_statement = accounting_periods\
            .insert()\
            .values(**new_record)
        loggerOutput(message=f"accounting_period_insert_record - Insert Account Period Record {obj}")
        
        conn.execute(insert_statement)
        conn.commit()

def accounting_period_update_record(engine, obj) -> None:
    with engine.connect() as conn:
        loggerOutput(message=f"accounting_period_update_record - Start Update Account Period Record: {obj}")
        updated_record = copy.deepcopy(obj)
        updated_record = AccountingPeriodsModel(**updated_record).model_dump()
        
        update_statement = accounting_periods\
            .update()\
            .where(
                (accounting_periods.c.month  == updated_record['month']) &
                (accounting_periods.c.year  == updated_record['year'])
            )\
            .values(**updated_record)
        loggerOutput(message=f"accounting_period_update_record - Update Account Period Record: {obj}")
        
        conn.execute(update_statement)
        conn.commit()

