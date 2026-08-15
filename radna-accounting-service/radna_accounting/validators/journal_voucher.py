from pydantic import BaseModel, model_validator, Field
from datetime import datetime, date
import uuid
import copy
import re
from uuid import UUID
from radna_accounting.models.journal_entry import je_meta
from radna_accounting.models.journal_voucher import jv_meta

from radna_accounting.configs.response_codes.mapping import (
    JNV_CODE,
    HIS_CODE,
    MESSAGE_KEY,
    error_map
)

model_name = "JournalVoucherModel"

supported_history_operations = [
    "I",
    "U",
    "D"
]

class JournalVoucherModel(BaseModel):
    id: UUID | str | None = None
    transaction_id: str | None = None
    document_name: str | None = None
    document_path: str | None = None
    document_file_type: str | None = None
    signed_document_name: str | None = None
    signed_document_path: str | None = None
    signed_document_file_type: str | None = None
    created_date: str | datetime | None = None
    updated_date: str | datetime | None = None

    @model_validator(mode="before")
    def id_validator(cls, values):
        id = values[jv_meta.ID]
        if id is None:
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0002"))
            raise Exception(error)
        if isinstance(id, str):
            try:
                values[jv_meta.ID] = uuid.UUID(id)
                test = values[jv_meta.ID].version == 4
            except (ValueError, TypeError):
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}0001"))
                raise Exception(error)
        else:
            if not isinstance(id, uuid.UUID):
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}0001"))
                raise Exception(error)
        return values

    @model_validator(mode="before")
    def transaction_id_validator(cls, values):
        transaction_id = values[jv_meta.TRANSACTION_ID]
        if transaction_id is None:
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0009"))
            raise Exception(error)
        if not isinstance(transaction_id, str):
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0003"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(transaction_id).__name__
            )
            raise Exception(error)
        if len(transaction_id) <= 0:
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}0004"))
                raise Exception(error)
        if len(transaction_id) > 30:
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}0005"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    transaction_id_length=je_meta.TRANSACTION_ID_LENGTH
                )
                raise Exception(error)
        if not re.search(r"^\d{4}\d{2}\-\d{5}\Z", transaction_id):
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0006"))
            raise Exception(error)
        else:
            year = transaction_id[:4]
            month = transaction_id[4:6]
            if int(year) < 1000  or int(year) > 9999:
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}0007"))
                raise Exception(error)
            if 1 > int(month) or int(month) > 12:
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}008"))
                raise Exception(error)
        return values

    @model_validator(mode="before")
    def document_name_validator(cls, values):
        document_name = values[jv_meta.DOCUMENT_NAME]
        if not isinstance(document_name, str):
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0010"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(document_name).__name__
            )
            raise Exception(error)
        if len(document_name) > jv_meta.DOCUMENT_NAME_LENGTH:
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0011"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                description_length=jv_meta.DOCUMENT_NAME_LENGTH
            )
            raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def document_path_validator(cls, values):
        document_path = values[jv_meta.DOCUMENT_PATH]
        if not isinstance(document_path, str):
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0012"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(document_path).__name__
            )
            raise Exception(error)
        if len(document_path) > jv_meta.DOCUMENT_PATH_LENGTH:
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0013"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                description_length=jv_meta.DOCUMENT_PATH_LENGTH
            )
            raise Exception(error)
        return values
    @model_validator(mode="before")
    def document_file_type_validator(cls, values):
        document_file_type = values[jv_meta.DOCUMENT_FILE_TYPE]
        if not isinstance(document_file_type, str):
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0014"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(document_file_type).__name__
            )
            raise Exception(error)
        if len(document_file_type) > jv_meta.DOCUMENT_FILE_TYPE_LENGTH:
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0015"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                description_length=jv_meta.DOCUMENT_FILE_TYPE_LENGTH
            )
            raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def signed_document_name_validator(cls, values):
        signed_document_name = values[jv_meta.SIGNED_DOCUMENT_NAME]
        if signed_document_name is not None:
            if not isinstance(signed_document_name, str):
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}016"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    variable_type=type(signed_document_name).__name__
                )
                raise Exception(error)
            if len(signed_document_name) > jv_meta.SIGNED_DOCUMENT_NAME_LENGTH:
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}0017"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    description_length=jv_meta.SIGNED_DOCUMENT_NAME_LENGTH
                )
                raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def signed_document_path_validator(cls, values):
        signed_document_path = values[jv_meta.SIGNED_DOCUMENT_PATH]
        if signed_document_path is not None:
            if not isinstance(signed_document_path, str):
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}0018"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    variable_type=type(signed_document_path).__name__
                )
                raise Exception(error)
            if len(signed_document_path) > jv_meta.SIGNED_DOCUMENT_PATH_LENGTH:
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}0019"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    description_length=jv_meta.SIGNED_DOCUMENT_PATH_LENGTH
                )
                raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def signed_document_file_type_validator(cls, values):
        signed_document_file_type = values[jv_meta.SIGNED_DOCUMENT_FILE_TYPE]
        if signed_document_file_type is not None:
            if not isinstance(signed_document_file_type, str):
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}0020"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    variable_type=type(signed_document_file_type).__name__
                )
                raise Exception(error)
            if len(signed_document_file_type) > jv_meta.SIGNED_DOCUMENT_FILE_TYPE_LENGTH:
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}021"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    description_length=jv_meta.SIGNED_DOCUMENT_FILE_TYPE_LENGTH
                )
                raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def created_date_converter(cls, values):
        if jv_meta.CREATED_DATE in values.keys():
            created_date = values[jv_meta.CREATED_DATE]
            if created_date is not None:
                if isinstance(created_date, str):
                    values[jv_meta.CREATED_DATE] = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S.%f")
        return values
    
    @model_validator(mode="before")
    def updated_date_converter(cls, values):
        if jv_meta.UPDATED_DATE in values.keys():
            updated_date = values[jv_meta.UPDATED_DATE]
            if updated_date is not None:
                if isinstance(updated_date, str):
                    values[jv_meta.UPDATED_DATE] = datetime.strptime(updated_date, "%Y-%m-%d %H:%M:%S.%f")
        return values

class JournalVoucherHistoryModel(JournalVoucherModel):
    history_id: UUID = Field(default_factory=lambda: uuid.uuid4())
    history_date: str | datetime | None = Field(default_factory=lambda: datetime.now())
    history_operation: str | None = None
    
    @model_validator(mode="before")
    def history_opertation_validator(cls, values):
        history_operation = values[jv_meta.HISTORY_OPERATION]
        if history_operation not in supported_history_operations:
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}{HIS_CODE}0001"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                history_operation=history_operation
            )
            raise Exception(error)
        return values

class JournalVoucherDocumentDataMetaData:
    def __init__(self):
        self.JOURNAL_VOUCHER_ID = "journalVoucherId"
        self.COMPANY_NAME = "companyName"
        self.TRANSACTION_DATE = "transactionDate"
        self.CURRENCY_CODE = "currencyCode"
        self.JOURNAL_ENTRY = "journalEntry"

jv_document_data_meta = JournalVoucherDocumentDataMetaData()

class JournalVoucherDocumentDataModel(BaseModel):
    companyName: str = ""
    journalVoucherId: str = ""
    transactionDate: str = ""
    currencyCode: str = ""
    creditTotal: float = 0.0
    debitTotal: float = 0.0
    journalEntry: list = []

class JournalVoucherDataContentMetaData:
    def __init__(self):
        self.ID = "id"
        self.CONTENT = "content"

jv_data_content_meta = JournalVoucherDataContentMetaData()

class JournalVoucherDataContentModel(BaseModel):
    id: str = ""
    content: str = ""

