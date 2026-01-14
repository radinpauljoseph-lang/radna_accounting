from pydantic import BaseModel, model_validator
from datetime import datetime, date
import uuid
import copy
import re
from uuid import UUID
from ..models.chart_of_accounts import coa_meta
from ..models.journal_entry import (
    je_meta,
    je_status,
    je_types
)

from ..configs.response_codes.mapping import (
    COA_CODE,
    JNE_CODE,
    MESSAGE_KEY,
    error_map
)

model_name = "JournalEntryModel"
transaction_types = je_types.getEntryTypesAsList()

allowed_status = je_status.getStatusAsList()

class JournalEntryModel(BaseModel):
    id: str | UUID | None = None
    transaction_id: str = ""
    transaction_date: str | datetime | None = None
    # currency_code: str | None = None
    # status: str | None = None
    account_number: str | None = None
    # entry_type: str | None = None
    # description: str | None = None
    # amount: float | None = None
    # posting_date: str | datetime | None = None
    # created_date: str | datetime | None = None
    # updated_date: str | datetime | None = None

    @model_validator(mode="before")
    def id_validator(cls, values):
        id = values[je_meta.ID]
        if id is None:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0008"))
            raise Exception(error)
        if isinstance(id, str):
            try:
                test = uuid.UUID(id).version == 4
            except (ValueError, TypeError):
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0001"))
                raise Exception(error)
        else:
            if not isinstance(id, uuid.UUID):
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0001"))
                raise Exception(error)
            else:
                values[je_meta.ID] = str(id)
        return values


    @model_validator(mode="before")
    def transaction_id_validator(cls, values):
        transaction_id = values[je_meta.TRANSACTION_ID]
        if transaction_id is None:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0009"))
            raise Exception(error)
        if not isinstance(transaction_id, str):
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0005"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(transaction_id).__name__
            )
            raise Exception(error)
        if len(transaction_id) <= 0:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0003"))
                raise Exception(error)
        if len(transaction_id) > 30:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0004"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    transaction_id_length=je_meta.TRANSACTION_ID_LENGTH
                )
                raise Exception(error)
        if not re.search(r"^\d{4}\d{2}\-\d{5}\Z", transaction_id):
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0005"))
            raise Exception(error)
        else:
            year = transaction_id[:4]
            month = transaction_id[4:6]
            if int(year) < 1000  or int(year) > 9999:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0006"))
                raise Exception(error)
            if 1 > int(month) or int(month) > 12:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0007"))
                raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def transaction_date_validator(cls, values):
        transaction_date = values[je_meta.TRANSACTION_DATE]
        if isinstance(transaction_date, date):
            values[je_meta.TRANSACTION_DATE] = transaction_date.strftime("%Y-%m-%d")
        elif isinstance(transaction_date, str):
            if not re.search(r"^\d{4}-\d{2}-\d{2}\Z", transaction_date):
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0010"))
                raise Exception(error)
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0011"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(transaction_date).__name__
            )
            raise Exception(error)
        return values
    
    # remove model name interpolation to all error codes
    @model_validator(mode="before")
    def account_number_validator(cls, values):
        account_number = values[je_meta.ACCOUNT_NUMBER]
        if not isinstance(account_number, str):
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0001"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                model_name="ChartOfAccountsModel",
                variable_type=type(account_number).__name__
            )
            raise Exception(error)
        if len(account_number) < coa_meta.ACCOUNT_ID_MIN_LENGTH:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0002"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                model_name="ChartOfAccountsModel"
            )
            raise Exception(error)
        if len(account_number) > coa_meta.ACCOUNT_ID_LENGTH:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0003"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                model_name="ChartOfAccountsModel",
                account_id_length=coa_meta.ACCOUNT_ID_LENGTH
            )
            raise Exception(error)
        return values
    
    # @model_validator(mode="before")
    # def entry_type_validator(cls, values):
    #     entry_type = values[je_meta.ENTRY_TYPE]
    #     if not isinstance(entry_type, str):
    #         raise TypeError(f"{model_name} Error: incorrect entry type data type \'{type(entry_type).__name__}\'")
    #     if entry_type not in transaction_types:
    #         raise ValueError(f"Error: Unknown entry type \'{entry_type}\'")
    #     return values
    
    # @model_validator(mode="before")
    # def description_validator(cls, values):
    #     if je_meta.DESCRIPTION in values.keys():
    #         description = values[je_meta.DESCRIPTION]
    #         if not isinstance(description, str) and description is not None:
    #             raise TypeError(f"{model_name} Error: incorrect description data type \'{type(description).__name__}\'")
    #         if description is not None and len(description) > je_meta.DESCRIPTION_LENGTH:
    #             raise ValueError(f"{model_name} Error: description field maximum length is {je_meta.DESCRIPTION_LENGTH}")
    #     return values
    
    # @model_validator(mode="before")
    # def amount_validator(cls, values):
    #     amount = values[je_meta.AMOUNT]
    #     if isinstance(amount, str):
    #         raise TypeError(f"{model_name} Error: incorrect amount data type \'{type(amount).__name__}\'")
    #     return values
    
    # @model_validator(mode="before")
    # def currency_code_validator(cls, values):
    #     if je_meta.CURRENCY_CODE in values.keys():
    #         currency_code = values[je_meta.CURRENCY_CODE_LENGTH]
    #         if len(currency_code) != je_meta.CURRENCY_CODE_LENGTH:
    #             raise ValueError(f"{model_name} Error: currency code required length is {je_meta.CURRENCY_CODE_LENGTH}")
    #         if currency_code != "PHP":
    #             raise ValueError(f"{model_name} Error: invalid currency code \'{currency_code}\'")
    #     return values

    # @model_validator(mode="before")
    # def posting_date_validator(cls, values):
    #     if je_meta.POSTING_DATE in values.keys():
    #         posting_date = values[je_meta.POSTING_DATE]
    #         if isinstance(posting_date, date):
    #             values[je_meta.POSTING_DATE] = posting_date.strftime("%Y-%m-%d")
    #         elif isinstance(posting_date, str):
    #             if not re.search("^\d{4}\d{2}\-\d{5}\Z", posting_date):
    #                 raise ValueError(f"{model_name} Error: posting date not in proper format")
    #             else:
    #                 try:
    #                     values[je_meta.POSTING_DATE] = datetime.strptime(posting_date, "%Y-%m-%d").date()
    #                 except ValueError:
    #                     raise ValueError(f"{model_name} Error: invalid posting date")
    #         elif isinstance(posting_date, type(None)):
    #             values[je_meta.POSTING_DATE] = None
    #         else:
    #             raise TypeError(f"{model_name} Error: posting date invalid type")
    #     else:
    #         values[je_meta.POSTING_DATE] = None
    #     return values
    
    # @model_validator(mode="before")
    # def status_validator(cls, values):
    #     if je_meta.STATUS in values.keys():
    #         status = values[je_meta.STATUS]
    #         if not isinstance(status, type(None)) and status not in allowed_status:
    #             raise ValueError(f"{model_name} Error: invalid status \'{status}\'")
    #     return values
    
    # @model_validator(mode="before")
    # def created_date_validator(cls, values):
    #     if 'created_date' in values.keys():
    #         created_date = values['created_date']
    #         if created_date is not None:
    #             if isinstance(created_date, datetime):
    #                 values['created_date'] = created_date.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(created_date.microsecond / 1000):03d}"
    #             else:
    #                 values['created_date'] = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S.%f")
    #     return values
    
    # @model_validator(mode="before")
    # def updated_date_validator(cls, values):
    #     if 'updated_date' in values.keys():
    #         updated_date = values['updated_date']
    #         if updated_date is not None:
    #             if isinstance(updated_date, datetime):
    #                 values['updated_date'] = updated_date.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(updated_date.microsecond / 1000):03d}"
    #             else:
    #                 values['updated_date'] = datetime.strptime(updated_date, "%Y-%m-%d %H:%M:%S.%f")
    #     return values

class JournalEntryHistoryModel(BaseModel):
    id: str | UUID | None = None
    transaction_id: str | None = None
    transaction_date: str | datetime | None = None
    currency_code: str | None = None
    status: str | None = None
    account_number: str | None = None
    entry_type: str | None = None
    description: str | None = None
    amount: float | None = None
    posting_date: str | datetime | None = None
    history_id: str | UUID | None = None
    history_date: str | datetime | None = None
    history_operation: str | None = None
    created_date: str | datetime | None = None
    updated_date: str | datetime | None = None