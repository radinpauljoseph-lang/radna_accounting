import copy
import pandas as pd
from pandas import DataFrame
from sqlalchemy import text
from ...configs.config  import (
    logger
)
from ...models.chart_of_accounts import chart_of_accounts
from ...validators.chart_of_accounts import ChartOfAccountsModel

def account_record_value_validate(engine, column_name, value, check_count = False) -> bool:
    conn = engine.connect()
    validator = None
    result = None
    with engine.connect() as conn:
        validator = chart_of_accounts\
            .select()\
            .where(text(f"chart_of_accounts.{column_name} = \'{value}\'"))
        
        logger.info(f"account_record_value_validate - SQL: {validator}")
        result = conn.execute(validator)
    if not check_count:
        logger.info("account_record_value_validate - not check_count condition")
        return True if result.first() else False
    else:
        logger.info("account_record_value_validate - check_count condition")
        result = result.scalars()\
        .all()
        return True if len(result) > 0 else False 

def account_select_record(engine, column_name, value) -> dict:
    validator = None
    result = None
    if type(value).__name__ not in ('str', 'UUID', 'NoneType'):
        raise TypeError(f"account_select_record - {type(value).__name__} data type not allowed")
    with engine.connect() as conn:
        validator = chart_of_accounts\
            .select()\
            .where(text(f"chart_of_accounts.{column_name} = \'{value}\'"))
        result = conn.execute(validator)

        logger.info(f"account_select_record - SQL: {validator}")
    
    result = result.first()
    result = dict(result._mapping)
    return result

def account_select_all_account_records(engine) -> DataFrame:
    validator = None
    result = None
    with engine.connect() as conn:
        validator = chart_of_accounts\
            .select()
        result = conn.execute(validator).fetchall()

        logger.info(f"account_select_all_account_records - SQL: {validator}")
    
    result = [dict(row._mapping) for row in result]
    result = pd.DataFrame(result)
    return result

def account_insert_record(engine, obj) -> None:
    with engine.connect() as conn:
        logger.info(f"account_insert_record - Start Insert Account Record {obj}")
        new_record = ChartOfAccountsModel(**obj).model_dump()
        del new_record["created_date"]
        del new_record["updated_date"]

        insert_statement = chart_of_accounts\
            .insert()\
            .values(**new_record)
        logger.info(f"account_insert_record - Insert Account Record {obj}")
        conn.execute(insert_statement)
        conn.commit()

def account_update_record(engine, account_id, obj) -> None:
    with engine.connect() as conn:
        logger.info(f"account_update_record - Start Update Account Record: {account_id}")
        updated_record = copy.deepcopy(obj)
        updated_record['account_id'] = account_id
        updated_record = ChartOfAccountsModel(**updated_record).model_dump()
        
        update_statement = chart_of_accounts\
            .update()\
            .where(chart_of_accounts.c.account_id == account_id)\
            .values(**updated_record)
        logger.info(f"account_update_record - Update Account Record: {account_id}")
        conn.execute(update_statement)
        conn.commit()

