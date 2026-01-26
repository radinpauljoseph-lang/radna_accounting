import copy
import uuid
import pandas as pd
from pandas import DataFrame
from sqlalchemy import text, distinct
from ...configs.config  import (
    logger
)
from ...models.transaction_ids import transaction_ids
from ...validators.transaction_ids import TransactionIdsModel

def transaction_ids_insert_record(engine, obj) -> None:
    with engine.connect() as conn:
        loggerOutput(message=f"transaction_ids_insert_record - Start Insert Transaction ID Tracker Record {obj}")
        new_record = TransactionIdsModel(**obj).model_dump()

        insert_statement = transaction_ids\
            .insert()\
            .values(**new_record)
        loggerOutput(message=f"transaction_ids_insert_record - Insert Transaction ID Tracker Record {obj}")
        
        conn.execute(insert_statement)
        conn.commit()

def transaction_ids_select_by_month_year_record(engine, month, year) -> DataFrame:
    validator = None
    result = None
    with engine.connect() as conn:
        validator = transaction_ids\
            .select()\
            .where(
                (transaction_ids.c.month == month) &
                (transaction_ids.c.year == year)
            )
        result = conn.execute(validator).fetchall()

        loggerOutput(message=f"je_select_multiple_record - SQL: {validator}")
    
    result = [dict(row._mapping) for row in result]
    result = pd.DataFrame(result)
    return result



