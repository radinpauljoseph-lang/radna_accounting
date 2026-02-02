import copy
import re
from sqlalchemy import cast, Integer, desc
from ...configs.config  import (
    logger_types,
    loggerOutput
)
from ...configs.config import engine
from ...configs.response_codes.mapping import (
    TIS_CODE,
    MESSAGE_KEY,
    error_map
)
from ...models.transaction_ids import (
    ti_meta,
    transaction_ids
)
from ...validators.transaction_ids import TransactionIdsModel
from ...validators.data_model import (
    DATA_KEY,
    DataModel
)

class TransactionIdsCoreMetaData:
    def __init__(self):
        self.TRANSACTION_IDS_CORE = "TransactionIdsCore"
        self.INSERT_RECORD = "insertRecord"
        self.SELECT_IDS_BY_MONTH_YEAR = "selectIdsByMonthYear"
        self.SELECT_RECORD = "selectRecord"
        self.PARSE_TRNASCTION_ID = "parseTransactionId"

ti_core_meta = TransactionIdsCoreMetaData()

class TransactionIdsCore:
    def __init__(self, rrn = None):
        self.dto_model = TransactionIdsModel
        self.engine = engine
        self.rrn = rrn

    def insertRecord(self, obj: dict) -> None:
        new_record = None

        loggerOutput(rrn=self.rrn, message=f"{ti_core_meta.TRANSACTION_IDS_CORE}.{ti_core_meta.INSERT_RECORD} - Start Insert Transaction ID Record {obj}")

        with self.engine.connect() as conn:
            new_record = self.dto_model(**obj).model_dump()

            insert_statement = transaction_ids\
                .insert()\
                .values(**new_record)
            conn.execute(insert_statement)
            conn.commit()
        
        loggerOutput(rrn=self.rrn, message=f"{ti_core_meta.TRANSACTION_IDS_CORE}.{ti_core_meta.INSERT_RECORD} - Done Insert Transaction ID Record {obj}")

    ## Refactor: get latest transaction ID
    # def selectIdsByMonthYear(self, month: int, year: int) -> dict:
    #     validator = None
    #     result = None

    #     loggerOutput(rrn=self.rrn, message=f"{ti_core_meta.TRANSACTION_IDS_CORE}.{ti_core_meta.INSERT_RECORD} - Done Select Transaction IDs By Month & Year")
    #     if not isinstance(month, int):
    #         error = copy.deepcopy(error_map.get(f"{TIS_CODE}0001"))
    #         error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
    #             variable_type=type(month).__name__
    #         )
    #         raise Exception(error)
    #     if int(month) < 1  or int(month) > 12:
    #       error = copy.deepcopy(error_map.get(f"{TIS_CODE}0002"))
    #       raise Exception(error)
        
    #     if not isinstance(year, int):
    #         error = copy.deepcopy(error_map.get(f"{TIS_CODE}0003"))
    #         error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
    #             variable_type=type(year).__name__
    #         )
    #         raise Exception(error)
    #     if int(year) < 1000  or int(year) > 9999:
    #       error = copy.deepcopy(error_map.get(f"{TIS_CODE}0004"))
    #       raise Exception(error)
        
    #     with self.engine.connect() as conn:
    #         validator = transaction_ids\
    #             .select()\
    #             .where(
    #                 (transaction_ids.c.month == month) &
    #                 (transaction_ids.c.year == year)
    #             )
    #         result = conn.execute(validator).fetchall()

    #     result = [dict(row._mapping) for row in result]
    #     result = pd.DataFrame(result)
    #     loggerOutput(rrn=self.rrn, message=f"{ti_core_meta.TRANSACTION_IDS_CORE}.{ti_core_meta.INSERT_RECORD} - Done Select Transaction IDs By Month & Year")
    #     return result
    
    def selectRecord(self, month: int, year: int, id: str) -> dict:
        validator = None
        result = None

        loggerOutput(rrn=self.rrn, message=f"{ti_core_meta.TRANSACTION_IDS_CORE}.{ti_core_meta.SELECT_RECORD} - Start Select Record")

        ti_obj = TransactionIdsModel(
            month=month,
            year=year,
            id=id
        ).model_dump()
        with self.engine.connect() as conn:
            validator = transaction_ids\
                .select()\
                .where(
                    (transaction_ids.c.month == ti_obj[ti_meta.MONTH]) &
                    (transaction_ids.c.year == ti_obj[ti_meta.YEAR]) &
                    (transaction_ids.c.id == ti_obj[ti_meta.ID])
                )
            result = conn.execute(validator)

        result = result.first()
        if result is not None:
            result = dict(result._mapping)
            result = self.dto_model(**result).model_dump()
            result = DataModel(data=result).model_dump()
            loggerOutput(rrn=self.rrn, message=f"{ti_core_meta.TRANSACTION_IDS_CORE}.{ti_core_meta.SELECT_RECORD} - {result}")
        return result
    
    def selectCurrentId(self, month: int, year: int) -> dict:
        validator = None
        result = None

        loggerOutput(rrn=self.rrn, message=f"{ti_core_meta.TRANSACTION_IDS_CORE}.{ti_core_meta.SELECT_RECORD} - Start Select Record")

        with self.engine.connect() as conn:
            validator = transaction_ids\
                .select()\
                .where(
                    (transaction_ids.c.month == month) &
                    (transaction_ids.c.year == year)
                )\
                .order_by(
                    desc(cast(transaction_ids.c.id, Integer))
                )\
                .limit(1)
            result = conn.execute(validator)

        result = result.first()
        if result is not None:
            result = dict(result._mapping)
            result = self.dto_model(**result).model_dump()
            result = DataModel(data=result).model_dump()
            loggerOutput(rrn=self.rrn, message=f"{ti_core_meta.TRANSACTION_IDS_CORE}.{ti_core_meta.SELECT_RECORD} - {result}")
        return result
    
    def parseTransactionId(self, transaction_id: str) -> dict:
        result = {}
        try:
            if not isinstance(transaction_id, str):
                raise Exception()
            if re.search(r"^\d{4}\d{2}\-\d{5}\Z", transaction_id):
                result = self.dto_model(
                    year=int(transaction_id[:4]),
                    month=int(transaction_id[4:6]),
                    id=str(transaction_id[7:12])
                ).model_dump()
            else:
                error = copy.deepcopy(error_map.get(f"{TIS_CODE}0009"))
                raise Exception(error)
        except Exception as err:
            loggerOutput(
                rrn=self.rrn,
                message=f"{ti_core_meta.TRANSACTION_IDS_CORE}.{ti_core_meta.PARSE_TRNASCTION_ID} - {err}"
            )
        finally:
            return result
        


        

