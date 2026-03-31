import copy
from datetime import datetime

from ...configs.config  import (
    logger_types,
    loggerOutput
)
from ...configs.config import engine
from ...configs.response_codes.mapping import (
    COA_CODE,
    MESSAGE_KEY,
    error_map
)
from ...models.chart_of_accounts import (
    chart_of_accounts,
    coa_meta
)
from ...validators.chart_of_accounts import ChartOfAccountsModel
from ...validators.data_model import (
    DATA_KEY,
    DataModel
)

class ChartOfAccountsCoreMetaData:
    def __init__(self):
        self.CHART_OF_ACCOUNTS_CORE = "ChartOfAccountsCore"
        self.INSERT_RECORD = "insertRecord"
        self.SELECT_RECORD_BY_ID = "selectRecordById"
        self.SELECT_RECORD_BY_NAME = "selectRecordByName"
        self.UPDATE_RECORD_BY_ID = "updateRecordById"
        self.DELETE_RECORD_BY_ID = "deleteRecordById"

coa_core_meta = ChartOfAccountsCoreMetaData()
class ChartOfAccountsCore:
    def __init__(self, rrn = None) -> None:
        self.dto_model = ChartOfAccountsModel
        self.engine = engine
        self.rrn = rrn

    def insertRecord(self, obj: ChartOfAccountsModel) -> None:
        new_record = None

        self.dto_model(**obj.model_dump())

        with self.engine.connect() as conn:
            loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.INSERT_RECORD} - Start Insert Account Record {obj}")
            new_record = copy.deepcopy(obj)
            new_record.created_date = datetime.now()
            new_record.updated_date = new_record.created_date

            insert_statement = chart_of_accounts\
                .insert()\
                .values(**new_record.model_dump())
            loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.INSERT_RECORD} - Done Insert Account Record {obj}")
            conn.execute(insert_statement)
            conn.commit()
    
    def selectRecordById(self, account_id: str) -> dict:
        validator = None
        result = None

        loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.SELECT_RECORD_BY_ID} - Start Select Record By ID")
        with self.engine.connect() as conn:
            validator = chart_of_accounts\
                .select()\
                .where(chart_of_accounts.c.account_id == account_id)
            result = conn.execute(validator)
        
        result = result.first()
        if result is not None:
            result = dict(result._mapping)
            result = self.dto_model(**result).model_dump()
            result = DataModel(data=result).model_dump()
            loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.SELECT_RECORD_BY_ID} - {result}")
        
        loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.SELECT_RECORD_BY_ID} - Done Select Record By ID")
        return result
    
    def selectRecordByName(self, name: str) -> dict:
        validator = None
        result = None
        
        loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.SELECT_RECORD_BY_NAME} - Start Select Record By Name")
        with self.engine.connect() as conn:
            validator = chart_of_accounts\
                .select()\
                .where(chart_of_accounts.c.name == name)
            result = conn.execute(validator)
        
        result = result.first()
        if result is not None:
            result = dict(result._mapping)
            result = self.dto_model(**result).model_dump()
            result = DataModel(data=result).model_dump()
        
        loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.SELECT_RECORD_BY_NAME} - Start Select Record By Name")
        return result
    
    def updateRecordById(self, account_id: str, obj: dict) -> None:
        loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.UPDATE_RECORD_BY_ID} - Start Update Account Record: {account_id}")
        record = copy.deepcopy(obj)
        record[coa_meta.ACCOUNT_ID] = account_id
        record = self.dto_model(**record).model_dump()
        record[coa_meta.UPDATED_DATE] = datetime.now()

        query_result = self.selectRecordById(account_id)
        if query_result is not None:
            with self.engine.connect() as conn:
                record[coa_meta.CREATED_DATE] = query_result[DATA_KEY][coa_meta.CREATED_DATE]
                update_statement = chart_of_accounts\
                    .update()\
                    .where(chart_of_accounts.c.account_id == account_id)\
                    .values(**record)
                conn.execute(update_statement)
                conn.commit()
                loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.UPDATE_RECORD_BY_ID} - Done Update Account Record: {account_id}")
        else:
            loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.UPDATE_RECORD_BY_ID} - Account Record Not Found: {account_id}")
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0101"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                account_id=account_id
            )
            raise Exception(error)
    
    def deleteRecordById(self, account_id: str) -> None:
        loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.DELETE_RECORD_BY_ID} - Start Delete Account Record: {account_id}")
        with self.engine.connect() as conn:
            delete_statement = chart_of_accounts\
                .delete()\
                .where(chart_of_accounts.c.account_id == account_id)
            conn.execute(delete_statement)
            conn.commit()
            loggerOutput(rrn=self.rrn, message=f"{coa_core_meta.CHART_OF_ACCOUNTS_CORE}.{coa_core_meta.DELETE_RECORD_BY_ID} - Start Done Account Record: {account_id}")





