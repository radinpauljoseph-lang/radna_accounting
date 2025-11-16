import copy
import uuid
import pandas as pd
from pandas import DataFrame
from sqlalchemy import text, distinct
from ...configs.config  import (
    logger
)
from ...models.transaction_id_tracker import transaction_id_tracker
from ...validators.transaction_id_tracker import TransactionIdTrackerModel

def transaction_id_tracker_insert_record(engine, obj) -> None:
    with engine.connect() as conn:
        logger.info(f"transaction_id_tracker_insert_record - Start Insert Transaction ID Tracker Record {obj}")
        new_record = TransactionIdTrackerModel(**obj).model_dump()

        insert_statement = transaction_id_tracker\
            .insert()\
            .values(**new_record)
        logger.info(f"transaction_id_tracker_insert_record - Insert Transaction ID Tracker Record {obj}")
        
        conn.execute(insert_statement)
        conn.commit()

def transaction_id_tracker_select_by_month_year_record(engine, month, year) -> DataFrame:
    validator = None
    result = None
    with engine.connect() as conn:
        validator = transaction_id_tracker\
            .select()\
            .where(
                (transaction_id_tracker.c.month == month) &
                (transaction_id_tracker.c.year == year)
            )
        result = conn.execute(validator).fetchall()

        logger.info(f"je_select_multiple_record - SQL: {validator}")
    
    result = [dict(row._mapping) for row in result]
    result = pd.DataFrame(result)
    return result



