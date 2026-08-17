import copy
from uuid import uuid4
from django.test import RequestFactory
from datetime import datetime
from xhtml2pdf import pisa
from django.template import loader
import json
import os
from radna_accounting.configs.config import (
    ENV,
    config_path,
    CONFIGS
)
from pathlib import Path
from radna_accounting.configs.config import (
    logger_types,
    loggerOutput
)
from radna_accounting.configs.config import engine
from radna_accounting.configs.response_codes.mapping import (
    JNV_CODE,
    error_map
)
from radna_accounting.models.journal_voucher import (
    jv_meta,
    journal_voucher,
    journal_voucher_history
)
from radna_accounting.validators.journal_voucher import (
    jv_data_content_meta,
    JournalVoucherModel,
    JournalVoucherDocumentDataModel,
    JournalVoucherDataContentModel,
    JournalVoucherHistoryModel
)
from radna_accounting.validators.journal_voucher import JournalVoucherDocumentDataModel
from radna_accounting.validators.data_model import (
    DATA_KEY,
    DataModel
)

COMPANY_NAME = CONFIGS[f"{ENV}.company"]['company_name']
JOURNAL_VOUCHER_TEMPLATE_NAME = CONFIGS[f"{ENV}.report"]['journal_voucher_template_name']
JOURNAL_VOUCHER_FOLDER_NAME = CONFIGS[f"{ENV}.report"]['journal_voucher_folder_name']
JOURNAL_VOUCHER_FOLDER_PATH = CONFIGS[f"{ENV}.report"]['journal_voucher_folder_path']
JOURNAL_VOUCHER_FILE_TYPE = CONFIGS[f"{ENV}.report"]['journal_voucher_file_type']
WRITE_BINARY_MODE = "wb"

class JournalVoucherCoreMetaData:
    def __init__(self):
        self.JOURNAL_VOUCHER_CORE = "JournalVoucherCore"
        self.GENERATE_RECORD = "generateRecord"
        self.GENERATE_DOCUMENT_CONTENT = "generateDocumentContent"
        self.INSERT_RECORD = "insertRecord"
        self.SELECT_RECORD_BY_TRANSACTION_ID = "selectRecordByTransactionId"
        self.UPDATE_RECORD = "updateRecord"
    
jv_core_meta = JournalVoucherCoreMetaData()

class JournalVoucherCore:
    def __init__(self, rrn = None) -> None:
        self.__dto_model = JournalVoucherModel
        self.__history_model = JournalVoucherHistoryModel
        self.__engine = engine
        self.__rrn = rrn

    def generateDocumentContent(self, transaction_id: str, content: dict) -> dict:
        data = None
        template = loader.get_template(JOURNAL_VOUCHER_TEMPLATE_NAME)
        factory = RequestFactory()
        request = factory.get('/fake-url/')
        
        template_content = copy.deepcopy(content)
        template_content = JournalVoucherDocumentDataModel(**template_content)
        template_content.companyName = COMPANY_NAME
        template_content.journalVoucherId = f"JV-{transaction_id}"

        html_content = template.render(template_content.model_dump(), request)

        loggerOutput(
            message=f"@@@@@@ content: {template_content}"
        )
        data = JournalVoucherDataContentModel(
            id=template_content.journalVoucherId,
            content=html_content
        )
        return data.model_dump()
    
    def generateDocument(self, data: dict):
        pisa_status = None
        document_folder_path = f"{JOURNAL_VOUCHER_FOLDER_PATH}\\{JOURNAL_VOUCHER_FOLDER_NAME}\\{COMPANY_NAME}"
        document_file_path = f"{document_folder_path}\\{data[jv_data_content_meta.ID]}.{JOURNAL_VOUCHER_FILE_TYPE}"
        folder_path = Path(document_folder_path)
        folder_path.mkdir(parents=True, exist_ok=True)
        with open(document_file_path, WRITE_BINARY_MODE) as pdf_file:
            pisa_status = pisa.CreatePDF(
                data[jv_data_content_meta.CONTENT],
                dest=pdf_file
            )

        return pisa_status
    
    def insertRecord(self, transaction_id: str, obj: dict) -> None:
        new_record = None
        history_record = None

        with self.__engine.connect() as conn:
            doc_data = self.generateDocumentContent(transaction_id, obj)
            doc_name = doc_data[jv_data_content_meta.ID]
            doc_data = self.generateDocument(doc_data)

            loggerOutput(
                message="START",
                rrn=self.__rrn
            )
            temp = {
                "id": uuid4(),
                "transaction_id": transaction_id,
                "document_name": doc_name,
                "document_path": f"{JOURNAL_VOUCHER_FOLDER_PATH}\\{JOURNAL_VOUCHER_FOLDER_NAME}\\{COMPANY_NAME}",
                "document_file_type": JOURNAL_VOUCHER_FILE_TYPE
            }
            new_record = self.__dto_model(
                id=uuid4(),
                transaction_id=transaction_id,
                document_name=doc_name,
                document_path=f"{JOURNAL_VOUCHER_FOLDER_PATH}\\{JOURNAL_VOUCHER_FOLDER_NAME}\\{COMPANY_NAME}",
                document_file_type=JOURNAL_VOUCHER_FILE_TYPE,
                signed_document_name=None,
                signed_document_path=None,
                signed_document_file_type=None
            ).model_dump()
            loggerOutput(
                message="START 2",
                rrn=self.__rrn
            )
            new_record[jv_meta.CREATED_DATE] = datetime.now()
            new_record[jv_meta.UPDATED_DATE] = new_record[jv_meta.CREATED_DATE]

            history_record = copy.deepcopy(new_record)
            history_record[jv_meta.HISTORY_OPERATION] = "I"
            history_record = self.__history_model(**history_record).model_dump()

            loggerOutput(
                message="START 3",
                rrn=self.__rrn
            )
            insert_statement = journal_voucher\
                .insert()\
                .values(**new_record)
            history_insert_statement = journal_voucher_history\
                .insert()\
                .values(**history_record)
            
            conn.execute(insert_statement)
            conn.execute(history_insert_statement)
            loggerOutput(
                message="START 4",
                rrn=self.__rrn
            )
            conn.commit()

    def selectRecordByTransactionId(self, transaction_id: str) -> dict:
        validator = None
        result = []

        loggerOutput(rrn=self.__rrn, message=f"{jv_core_meta.JOURNAL_VOUCHER_CORE}.{jv_core_meta.SELECT_RECORD_BY_TRANSACTION_ID} - Start Select Record By Transaction ID")
        with self.__engine.connect() as conn:
            validator = journal_voucher\
                .select()\
                .where(journal_voucher.c.transaction_id == transaction_id)
            result = conn.execute(validator)
        
        result = result.all()
        result = [row._asdict() for row in result]
        if len(result) > 0:
            result = [self.__dto_model(**data).model_dump() for data in result]
            result = DataModel(data=result).model_dump()
            loggerOutput(rrn=self.__rrn, message=f"{jv_core_meta.JOURNAL_VOUCHER_CORE}.{jv_core_meta.SELECT_RECORD_BY_TRANSACTION_ID} - {result}")
        
        loggerOutput(rrn=self.__rrn, message=f"{jv_core_meta.JOURNAL_VOUCHER_CORE}.{jv_core_meta.SELECT_RECORD_BY_TRANSACTION_ID} - Done Select Record By Transaction ID")
        return result
    
    def updateRecord(self, obj: dict) -> None:
        pass