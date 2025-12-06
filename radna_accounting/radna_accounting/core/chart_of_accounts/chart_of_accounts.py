import copy
import pandas as pd
from datetime import datetime
from pandas import DataFrame
from sqlalchemy import text
from ...configs.config  import (
    logger
)
from ...models.chart_of_accounts import chart_of_accounts
from ...validators.chart_of_accounts import ChartOfAccountsModel
from ...validators.data_model import DataModel
from ...configs.config import engine

class ChartOfAccountsCore:
    def __init__(self) -> None:
        self.dto_model = ChartOfAccountsModel
        self.engine = engine

    def insertRecord(self, obj) -> None:
        new_record = None
        with self.engine.connect() as conn:
            logger.info(f"insertRecord - Start Insert Account Record {obj}")
            new_record = self.dto_model(**obj).model_dump()
            new_record['created_date'] = datetime.now()
            new_record['updated_date'] = datetime.now()

            insert_statement = chart_of_accounts\
                .insert()\
                .values(**new_record)
            logger.info(f"insertRecord - Done Insert Account Record {obj}")
            conn.execute(insert_statement)
            conn.commit()
    
    def selectRecordById(self, account_id) -> dict:
        validator = None
        result = None

        with self.engine.connect() as conn:
            validator = chart_of_accounts\
                .select()\
                .where(chart_of_accounts.c.account_id == account_id)
            result = conn.execute(validator)
            logger.info(f"selectRecordById - SQL: {validator}")
        
        result = result.first()
        result = dict(result._mapping)
        result = self.dto_model(**result).model_dump()
        result = DataModel(data=result).model_dump()
        return result
    
    def selectRecordByName(self, name) -> dict:
        validator = None
        result = None

        with self.engine.connect() as conn:
            validator = chart_of_accounts\
                .select()\
                .where(chart_of_accounts.c.name == name)
            result = conn.execute(validator)
            logger.info(f"selectRecordByName - SQL: {validator}")
        
        result = result.first()
        result = dict(result._mapping)
        result = self.dto_model(**result).model_dump()
        result = DataModel(data=result).model_dump()
        return result
    
    def updateRecordById(self, account_id, obj) -> None:
        logger.info(f"updateRecordById - Start Update Account Record: {account_id}")

        with self.engine.connect() as conn:
            record = copy.deepcopy(obj)
            record['account_id'] = account_id
            record = self.dto_model(**record).model_dump()
            record['updated_date'] = datetime.now()
            update_statement = chart_of_accounts\
                .update()\
                .where(chart_of_accounts.c.account_id == account_id)\
                .values(**record)
            conn.execute(update_statement)
            conn.commit()
            logger.info(f"updateRecordById - Done Update Account Record: {account_id}")
    
    def deleteRecordById(self, account_id):
        logger.info(f"deleteRecordById - Start Delete Account Record: {account_id}")
        with self.engine.connect() as conn:
            delete_statement = chart_of_accounts\
                .delete()\
                .where(chart_of_accounts.c.account_id == account_id)
            conn.execute(delete_statement)
            conn.commit()
            logger.info(f"deleteRecordById - Done Delete Account Record: {account_id}")





