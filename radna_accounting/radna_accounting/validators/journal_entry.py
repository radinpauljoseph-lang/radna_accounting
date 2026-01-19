from pydantic import BaseModel, model_validator, Field
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
    HIS_CODE,
    MESSAGE_KEY,
    error_map
)

supported_currencies = [
    "PHP"
]

model_name = "JournalEntryModel"
transaction_types = je_types.getEntryTypesAsList()

allowed_status = je_status.getStatusAsList()

supported_history_operations = [
    "I",
    "U",
    "D"
]
class JournalEntryModel(BaseModel):
    id: str | UUID | None = None
    transaction_id: str = ""
    transaction_date: str | datetime | None = None
    currency_code: str | None = None
    status: str | None = None
    account_number: str | None = None
    entry_type: str | None = None
    description: str | None = None
    amount: float | int | None = None
    posting_date: str | datetime | None = None
    created_date: str | datetime | None = None
    updated_date: str | datetime | None = None

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
                try:
                    test = datetime.strptime(transaction_date, "%Y-%m-%d")
                except Exception as e:
                    error = copy.deepcopy(error_map.get(f"{JNE_CODE}0023"))
                    error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                        transaction_date=transaction_date
                    )
                    raise Exception(error)
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0011"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(transaction_date).__name__
            )
            raise Exception(error)
        return values
    
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
    
    @model_validator(mode="before")
    def entry_type_validator(cls, values):
        entry_type = values[je_meta.ENTRY_TYPE]
        if not isinstance(entry_type, str):
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0013"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(entry_type).__name__
            )
            raise Exception(error)
        if entry_type not in transaction_types:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0012"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                entry_type=entry_type
            )
            raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def description_validator(cls, values):
        description = values[je_meta.DESCRIPTION]
        if description is not None:
            if not isinstance(description, str):
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0014"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    variable_type=type(description).__name__
                )
                raise Exception(error)
            if len(description) > je_meta.DESCRIPTION_LENGTH:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0015"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    description_length=je_meta.DESCRIPTION_LENGTH
                )
                raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def amount_validator(cls, values):
        amount = values[je_meta.AMOUNT]
        if not isinstance(amount, (float, int)):
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0016"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(amount).__name__
            )
            raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def currency_code_validator(cls, values):
        currency_code = values[je_meta.CURRENCY_CODE]
        if not isinstance(currency_code, str):
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0019"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(currency_code).__name__
            )
            raise Exception(error)
        if len(currency_code) != je_meta.CURRENCY_CODE_LENGTH:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0017"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                currency_code_length=je_meta.CURRENCY_CODE_LENGTH
            )
            raise Exception(error)
        if currency_code not in supported_currencies:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0018"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                currency_code=currency_code
            )
            raise Exception(error)
        return values

    @model_validator(mode="before")
    def posting_date_validator(cls, values):
        posting_date = values[je_meta.POSTING_DATE]
        if isinstance(posting_date, date):
            values[je_meta.POSTING_DATE] = posting_date.strftime("%Y-%m-%d")
        elif isinstance(posting_date, str):
            if not re.search(r"^\d{4}-\d{2}-\d{2}\Z", posting_date):
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0020"))
                raise Exception(error)
            else:
                try:
                    test = datetime.strptime(posting_date, "%Y-%m-%d")
                except Exception as e:
                    error = copy.deepcopy(error_map.get(f"{JNE_CODE}0022"))
                    error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                        posting_date=posting_date
                    )
                    raise Exception(error)
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0021"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(posting_date).__name__
            )
            raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def status_validator(cls, values):
        status = values[je_meta.STATUS]
        if not isinstance(status, str):
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0025"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(status).__name__
            )
            raise Exception(error)
        if status not in allowed_status:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0024"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                status=status
            )
            raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def created_date_converter(cls, values):
        if je_meta.CREATED_DATE in values.keys():
            created_date = values[je_meta.CREATED_DATE]
            if created_date is not None:
                if isinstance(created_date, str):
                    values[je_meta.CREATED_DATE] = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S.%f")
        return values
    
    @model_validator(mode="before")
    def updated_date_converter(cls, values):
        if je_meta.UPDATED_DATE in values.keys():
            updated_date = values[je_meta.UPDATED_DATE]
            if updated_date is not None:
                if isinstance(updated_date, str):
                    values[je_meta.UPDATED_DATE] = datetime.strptime(updated_date, "%Y-%m-%d %H:%M:%S.%f")
        return values

class JournalEntryHistoryModel(JournalEntryModel):
    history_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    history_date: str | datetime | None = Field(default_factory=lambda: datetime.now())
    history_operation: str | None = None
    
    @model_validator(mode="before")
    def history_opertation_validator(cls, values):
        history_operation = values[je_meta.HISTORY_OPERATION]
        if history_operation not in supported_history_operations:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}{HIS_CODE}0001"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                history_operation=history_operation
            )
            raise Exception(error)
        return values

