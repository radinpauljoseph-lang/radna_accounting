import copy
from datetime import datetime
from uuid import uuid4
from ...configs.config  import (
    logger_types,
    loggerOutput
)
from ...configs.config import engine
from ...configs.response_codes.mapping import (
    JNE_CODE,
    error_map
)
from ...models.journal_entry import (
    journal_entry,
    journal_entry_history,
    je_meta,
    je_status,
    je_types
)
from ...validators.journal_entry import (
    JournalEntryModel,
    JournalEntryHistoryModel
)
from ...validators.data_model import (
    DATA_KEY,
    DataModel
)

from sqlalchemy import extract

class JournalEntryCoreMetaData:
    def __init__(self):
        self.JOURNAL_ENTRY_CORE = "JournalEntryCore"
        self.INSERT_RECORD = "insertRecord"
        self.SELECT_RECORD_BY_ID = "selectRecordById"
        self.SELECT_RECORD_BY_TRANSACTION_ID = "selectRecordByTransactionId"
        self.UPDATE_RECORD_STATUS_BY_TRANSACTION_ID = "updateRecordStatusByTransactionId"
        self.UPDATE_RECORD_BY_ID = "updateRecordById"
        self.DELETE_RECORD_BY_ID = "deleteRecordById"
        self.POST_RECORDS_BY_TRANSACTION_ID = "postRecordsByTransactionId"
        self.SELECT_RECORDS_BY_MONTH_YEAR = "selectRecordsByMonthYear"

je_core_meta = JournalEntryCoreMetaData()
class JournalEntryCore:
    def __init__(self, rrn = None) -> None:
        self.dto_model = JournalEntryModel
        self.history_model = JournalEntryHistoryModel
        self.engine = engine
        self.rrn = rrn

    def insertRecord(self, obj: dict) -> None:
        new_record = None
        history_record = None
        with self.engine.connect() as conn:
            loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.INSERT_RECORD} - Start Insert Journal Entry Record {obj}")
            new_record = self.dto_model(**obj).model_dump()
            new_record[je_meta.CREATED_DATE] = datetime.now()
            new_record[je_meta.UPDATED_DATE] = new_record[je_meta.CREATED_DATE]

            history_record = copy.deepcopy(new_record)
            history_record[je_meta.HISTORY_OPERATION] = "I"
            history_record = self.history_model(**history_record).model_dump()

            insert_statement = journal_entry\
                .insert()\
                .values(**new_record)
            history_insert_statement = journal_entry_history\
                .insert()\
                .values(**history_record)
            
            conn.execute(insert_statement)
            conn.execute(history_insert_statement)
            conn.commit()
            loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.INSERT_RECORD} - Done Insert Journal Entry Record {obj}")
    
    def selectRecordById(self, id: str) -> dict:
        validator = None
        result = None

        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.SELECT_RECORD_BY_ID} - Start Select Record By ID")
        with self.engine.connect() as conn:
            validator = journal_entry\
                .select()\
                .where(journal_entry.c.id == id)
            result = conn.execute(validator)
        
        result = result.first()
        if result is not None:
            result = dict(result._mapping)
            result = self.dto_model(**result).model_dump()
            result = DataModel(data=result).model_dump()
            loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.SELECT_RECORD_BY_ID} - {result}")
        
        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.SELECT_RECORD_BY_ID} - Done Select Record By ID")
        return result
    
    def selectRecordByTransactionId(self, transaction_id: str) -> dict:
        validator = None
        result = None

        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.SELECT_RECORD_BY_TRANSACTION_ID} - Start Select Record By Transaction ID")
        with self.engine.connect() as conn:
            validator = journal_entry\
                .select()\
                .where(journal_entry.c.transaction_id == transaction_id)
            query_result = conn.execute(validator)
        
        query_result = query_result.all()
        query_result = [row._asdict() for row in query_result]
        if len(query_result) > 0:
            result = [self.dto_model(**data).model_dump() for data in query_result]
            result = DataModel(data=result).model_dump()
            loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.SELECT_RECORD_BY_TRANSACTION_ID} - {result}")
        
        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.SELECT_RECORD_BY_TRANSACTION_ID} - Done Select Record By Transaction ID")
        return result
    
    def updateRecordById(self, id: str, obj: dict) -> None:
        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.UPDATE_RECORD_BY_ID} - Start Update Journal Entry Record: {id}")
        record = copy.deepcopy(obj)
        record[je_meta.ID] = id
        record = self.dto_model(**record).model_dump()
        record[je_meta.UPDATED_DATE] = datetime.now()

        history_record = copy.deepcopy(record)
        history_record[je_meta.HISTORY_OPERATION] = "U"
        history_record = self.history_model(**history_record).model_dump()
        

        query_result = self.selectRecordById(id)
        if query_result is not None:
            with self.engine.connect() as conn:
                record[je_meta.CREATED_DATE] = query_result[DATA_KEY][je_meta.CREATED_DATE]
                history_record[je_meta.CREATED_DATE] = record[je_meta.CREATED_DATE]

                update_statement = journal_entry\
                    .update()\
                    .where(journal_entry.c.id == id)\
                    .values(**record)
                history_insert_statement = journal_entry_history\
                    .insert()\
                    .values(**history_record)
                
                conn.execute(update_statement)
                conn.execute(history_insert_statement)
                conn.commit()
                loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.UPDATE_RECORD_BY_ID} - Done Update Journal Entry Record: {id}")
        else:
            loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.UPDATE_RECORD_BY_ID} - Journal Entry Record Not Found: {id}")
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0026"))
            raise Exception(error)
    
    def deleteRecordById(self, id: str) -> None:
        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.DELETE_RECORD_BY_ID} - Start Delete Journal Entry Record: {id}")
        query_result = self.selectRecordById(id)

        if query_result is not None:
            
            current_status = query_result[DATA_KEY][je_meta.STATUS]
            if current_status not in [je_status.NEW, je_status.REJECTED]:
                loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.UPDATE_RECORD_BY_ID} - Invalid Journal Entry Record Status: {id}")
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0027"))
                raise Exception(error)
            
            history_record = copy.deepcopy(query_result[DATA_KEY])
            history_record[je_meta.HISTORY_OPERATION] = "D"
            history_record = self.history_model(**history_record).model_dump()
            
            with self.engine.connect() as conn:
                delete_statement = journal_entry\
                    .delete()\
                    .where(journal_entry.c.id == id)
                
                history_insert_statement = journal_entry_history\
                    .insert()\
                    .values(**history_record)
                
                conn.execute(delete_statement)
                conn.execute(history_insert_statement)
                conn.commit()
                loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.DELETE_RECORD_BY_ID} - Done Delete Journal Entry Record: {id}")
        else:
            loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.UPDATE_RECORD_BY_ID} - Journal Entry Record Not Found: {id}")
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0026"))
            raise Exception(error)
        
    def updateRecordStatusByTransactionId(self, transaction_id: str, status: str) -> None:
        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.UPDATE_RECORD_STATUS_BY_TRANSACTION_ID} - Start Update Journal Entry Record Status {transaction_id}: {status}")
        query_result = self.selectRecordByTransactionId(transaction_id)

        if len(query_result[DATA_KEY]) > 0:
            record = {
                je_meta.STATUS: status,
                je_meta.UPDATED_DATE: datetime.now()
            }

            with self.engine.connect() as conn:
                update_statement = journal_entry\
                    .update()\
                    .where(journal_entry.c.transaction_id == transaction_id)\
                    .values(**record)
                conn.execute(update_statement)

                query_result = self.selectRecordByTransactionId(transaction_id)
                query_result = query_result[DATA_KEY]

                for item in query_result:
                    history_record = copy.deepcopy(item)
                    history_record[je_meta.STATUS] = status
                    history_record[je_meta.HISTORY_OPERATION] = "U"
                    history_record[je_meta.UPDATED_DATE] = record[je_meta.UPDATED_DATE]
                    history_record[je_meta.HISTORY_DATE] = datetime.now()
                    history_record = self.history_model(**history_record).model_dump()

                    history_insert_statement = journal_entry_history\
                        .insert()\
                        .values(**history_record)
                    conn.execute(history_insert_statement)

                conn.commit()
                loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.UPDATE_RECORD_STATUS_BY_TRANSACTION_ID} - Done Update Journal Entry Record Status {id}: {status}")
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0010"))
            raise Exception(error)
        
    def postRecordsByTransactionId(self, transaction_id: str) -> None:
        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.POST_RECORDS_BY_TRANSACTION_ID} - Start Post Journal Entry Record")
        query_result = self.selectRecordByTransactionId(transaction_id)

        current_datetime = datetime.now()
        if len(query_result[DATA_KEY]) > 0:
            record = {
                je_meta.STATUS: je_status.POSTED,
                je_meta.POSTING_DATE: current_datetime.date(),
                je_meta.UPDATED_DATE: current_datetime
            }

            with self.engine.connect() as conn:
                update_statement = journal_entry\
                    .update()\
                    .where(journal_entry.c.transaction_id == transaction_id)\
                    .values(**record)
                conn.execute(update_statement)

                query_result = self.selectRecordByTransactionId(transaction_id)
                query_result = query_result[DATA_KEY]

                for item in query_result:
                    history_record = copy.deepcopy(item)
                    history_record[je_meta.STATUS] = je_status.POSTED
                    history_record[je_meta.POSTING_DATE] = record[je_meta.POSTING_DATE]
                    history_record[je_meta.HISTORY_OPERATION] = "U"
                    history_record[je_meta.UPDATED_DATE] = record[je_meta.UPDATED_DATE]
                    history_record[je_meta.HISTORY_DATE] = datetime.now()
                    history_record = self.history_model(**history_record).model_dump()

                    history_insert_statement = journal_entry_history\
                        .insert()\
                        .values(**history_record)
                    conn.execute(history_insert_statement)

                conn.commit()
                loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.POST_RECORDS_BY_TRANSACTION_ID} - Done Post Journal Entry Record")
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0010"))
            raise Exception(error)
        
    def getTransactionIdAmount(self, transaction_id: str) -> dict:
        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.DELETE_RECORD_BY_ID} - Start Get Transaction ID Amount: {transaction_id}")
        query_result = self.selectRecordByTransactionId(transaction_id)

        counter = {
            je_types.CREDIT: 0,
            je_types.DEBIT: 0
        }

        if len(query_result) > 0:
            journal_entries = query_result[DATA_KEY]
            for entry in journal_entries:
                entry_type = entry[je_meta.ENTRY_TYPE]
                amount = entry[je_meta.AMOUNT]
                counter[entry_type] = counter[entry_type] + amount
                    
        else:
            loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.UPDATE_RECORD_BY_ID} - Done Get Transaction ID Amount: {transaction_id}")
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0010"))
            raise Exception(error)
        
        return counter
    
    def selectRecordsByMonthYear(self, month: int, year: int) -> dict:
        validator = None
        result = []
        TRANSACTION_YEAR = "year"
        TRANSACTION_MONTH = "month"

        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.SELECT_RECORDS_BY_MONTH_YEAR} - Start Select Record By Transaction ID By Month & Year")
        with self.engine.connect() as conn:
            validator = journal_entry\
                .select()\
                .where(
                    extract(TRANSACTION_YEAR, journal_entry.c.transaction_date) == year,
                    extract(TRANSACTION_MONTH, journal_entry.c.transaction_date) == month
                )
            result = conn.execute(validator)
        
        result = result.all()
        result = [row._asdict() for row in result]
        if len(result) > 0:
            result = [self.dto_model(**data).model_dump() for data in result]
            result = DataModel(data=result).model_dump()
            loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.SELECT_RECORDS_BY_MONTH_YEAR} - {result}")
        
        loggerOutput(rrn=self.rrn, message=f"{je_core_meta.JOURNAL_ENTRY_CORE}.{je_core_meta.SELECT_RECORDS_BY_MONTH_YEAR} - Done Select Record By Transaction ID By Month & Year")
        return result






