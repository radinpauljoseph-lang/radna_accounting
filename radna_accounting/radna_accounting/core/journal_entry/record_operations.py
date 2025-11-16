import copy
import uuid
import pandas as pd
from datetime import datetime
from pandas import DataFrame
from sqlalchemy import text, distinct, extract
from ...configs.config  import (
    logger
)
from ...models.journal_entry import journal_entry
from ...models.journal_entry_history import journal_entry_history
from ...validators.journal_entry import JournalEntryModel

def je_record_value_validate(engine, column_name, value, check_count = False) -> bool:
    conn = engine.connect()
    validator = None
    result = None
    with engine.connect() as conn:
        validator = journal_entry\
            .select()\
            .where(text(f"journal_entry.{column_name} = \'{value}\'"))
        
        logger.info(f"je_record_value_validate - SQL: {validator}")
        result = conn.execute(validator)
    if not check_count:
        logger.info("je_record_value_validate - not check_count condition")
        return True if result.first() else False
    else:
        logger.info("je_record_value_validate - check_count condition")
        result = result.scalars()\
        .all()
        return True if len(result) > 0 else False 

def je_select_record(engine, value) -> dict:
    validator = None
    result = None
    with engine.connect() as conn:
        validator = journal_entry\
            .select()\
            .where(journal_entry.c.id == value)
        result = conn.execute(validator)

        logger.info(f"je_select_record - SQL: {validator}")
    
    result = result.first()
    result = dict(result._mapping)
    return result

def je_select_multiple_record(engine, column_name, value) -> DataFrame:
    validator = None
    result = None
    with engine.connect() as conn:
        validator = journal_entry\
            .select()\
            .where(journal_entry.c[f"{column_name}"] == value)
        result = conn.execute(validator).fetchall()

        logger.info(f"je_select_multiple_record - SQL: {validator}")
    
    result = [dict(row._mapping) for row in result]
    result = pd.DataFrame(result)
    return result

def je_select_by_transaction_date_month_year_record(engine, month, year) -> DataFrame:
    validator = None
    result = None
    with engine.connect() as conn:
        validator = journal_entry\
            .select()\
            .where(
                (extract('year', journal_entry.c.transaction_date) == year) &
                (extract('month', journal_entry.c.transaction_date) == month)
            )
        result = conn.execute(validator).fetchall()

        logger.info(f"je_select_by_transaction_date_month_year_record - SQL: {validator}")
    
    result = [dict(row._mapping) for row in result]
    result = pd.DataFrame(result)
    return result

def je_select_by_transaction_id_record(engine, transaction_id) -> DataFrame:
    validator = None
    result = None
    with engine.connect() as conn:
        validator = journal_entry\
            .select()\
            .where(
                journal_entry.c.transaction_id == transaction_id
            )
        result = conn.execute(validator).fetchall()

        logger.info(f"je_select_by_transaction_id_record - SQL: {validator}")
    
    result = [dict(row._mapping) for row in result]
    result = pd.DataFrame(result)
    return result

def je_delete_by_transaction_id_record(engine, transaction_id) -> None:
    validator = None
    with engine.connect() as conn:
        validator = journal_entry\
            .delete()\
            .where(
                journal_entry.c.transaction_id == transaction_id
            )
        conn.execute(validator)
        conn.commit()

        logger.info(f"je_delete_by_transaction_id_record - SQL: {validator}")

def je_select_transaction_id_distinct_values(engine) -> DataFrame:
    validator = None
    result = None
    with engine.connect() as conn:
        validator = journal_entry\
            .select(distinct(journal_entry.c.transaction_id))
        result = conn.execute(validator).fetchall()

        logger.info(f"je_select_multiple_record - SQL: {validator}")
    
    result = [dict(row._mapping) for row in result]
    result = pd.DataFrame(result)
    return result


def je_insert_record(engine, obj) -> None:
    with engine.connect() as conn:
        logger.info(f"je_insert_record - Start Insert Journal Entry Record {obj}")
        new_record = JournalEntryModel(**obj).model_dump()
        history_record = copy.deepcopy(new_record)
        history_record['history_id'] = uuid.uuid4()
        del new_record["created_date"]
        del new_record["updated_date"]

        insert_statement = journal_entry\
            .insert()\
            .values(**new_record)
        logger.info(f"je_insert_record - Insert Account Record {obj}")

        history_insert_statement =journal_entry_history\
            .insert()\
            .values(**new_record)
        
        conn.execute(insert_statement)
        conn.execute(history_insert_statement)
        conn.commit()

def je_update_record(engine, je_id, obj) -> None:
    with engine.connect() as conn:
        logger.info(f"je_update_record - Start Update Journal Entry Record: {je_id}")
        updated_record = copy.deepcopy(obj)
        updated_record = JournalEntryModel(**updated_record).model_dump()
        history_record = copy.deepcopy(updated_record)
        history_record['history_id'] = uuid.uuid4()
        
        update_statement = journal_entry\
            .update()\
            .where(journal_entry.c.id == je_id)\
            .values(**updated_record)
        logger.info(f"je_update_record - Update Journal Entry Record: {je_id}")

        history_insert_statement =journal_entry_history\
            .insert()\
            .values(**updated_record)
        
        conn.execute(update_statement)
        conn.execute(history_insert_statement)
        conn.commit()

def je_update_to_post_record(engine, transaction_id) -> None:
    with engine.connect() as conn:
        logger.info(f"je_update_to_post_record - Start Update Journal Entry To POSTED status Record: {transaction_id}")
        now = datetime.now().date()
        # now = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
        update_statement = journal_entry\
            .update()\
            .where(journal_entry.c.transaction_id == transaction_id)\
            .values(
                status="POSTED",
                posting_date=now,
                updated_date=now
            )
        logger.info(f"je_update_to_post_record - Update Journal Entry To POSTED status Record: {transaction_id}")

        # history_insert_statement =journal_entry_history\
        #     .insert()\
        #     .where(journal_entry.c.transaction_id == transaction_id)\
        #     .values(status="POSTED")
        
        conn.execute(update_statement)
        # conn.execute(history_insert_statement)
        conn.commit()

def je_update_to_post_by_month_year_record(engine, month, year) -> None:
    with engine.connect() as conn:
        logger.info(f"je_update_to_post_by_month_year_record - Start Update Journal Entry To POSTED status Record by {month}-{year}")
        now = datetime.now()
        now_datetime = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
        update_statement = journal_entry\
            .update()\
            .where(
                (extract('year', journal_entry.c.transaction_date) == year) &
                (extract('month', journal_entry.c.transaction_date) == month)
            )\
            .values(
                status="POSTED",
                posting_date=now.date(),
                updated_date=now_datetime
            )
        logger.info(f"je_update_to_post_by_month_year_record - Update Journal Entry To POSTED status Record by {month}-{year}")

        # history_insert_statement =journal_entry_history\
        #     .insert()\
        #     .where(journal_entry.c.transaction_id == transaction_id)\
        #     .values(status="POSTED")
        
        conn.execute(update_statement)
        # conn.execute(history_insert_statement)
        conn.commit()

