from pydantic import BaseModel, model_validator
from datetime import datetime, date
import uuid
import re
from uuid import UUID

model_name = "JournalEntryModel"
transaction_types = [
    'CREDIT',
    'DEBIT'
]

allowed_status = [
    'UNPOSTED',
    'POSTED'
]
class JournalEntryModel(BaseModel):
    id: str | UUID | None = None
    transaction_id: str | None = None
    transaction_date: str | datetime | None = None
    account_number: str | None = None
    description: str | None = None
    entry_type: str | None = None
    amount: float | None = None
    currency_code: str | None = None
    posting_date: str | datetime | None = None
    status: str | None = None
    created_date: str | datetime | None = None
    updated_date: str | datetime | None = None

    @model_validator(mode="before")
    def id_validator(cls, values):
        error_message = f"{model_name} Error: id field is not a valid UUID"
        if 'id' in values.keys():
            id = values['id']
            if isinstance(id, str):
                try:
                    return uuid.UUID(id).version == 4
                except (ValueError, TypeError):
                    raise ValueError(error_message)
            else:
                if id is not None and not isinstance(id, UUID):
                    raise TypeError(error_message)
        else:
            values['id'] = None
        return values


    @model_validator(mode="before")
    def transaction_id_validator(cls, values):
        if 'transaction_id' in values.keys():
            transaction_id = values['transaction_id']
            if transaction_id is not None and not isinstance(transaction_id, str):
                raise TypeError(f"{model_name} Error: incorrect transaction ID data type \'{type(transaction_id).__name__}\'")
            if transaction_id is not None and len(transaction_id) <= 0:
                raise ValueError(f"{model_name} Error: transaction ID minimum length is 1")
            if transaction_id is not None and len(transaction_id) > 30:
                raise ValueError(f"{model_name} Error: transaction ID maximum length is 30")
            if transaction_id is not None and not re.search("^\d{4}\d{2}\-\d{5}\Z", transaction_id):
                raise ValueError(f"{model_name} Error: transaction ID not in proper format")
            else:
                if transaction_id is not None:
                    year = transaction_id[:4]
                    month = transaction_id[4:6]
                    if int(year) < 1000  or int(year) > 9999:
                        raise ValueError(f"{model_name} Error: year in transaction ID is not a valid year")
                    if 1 > int(month)  or int(month) > 12:
                        raise ValueError(f"{model_name} Error: year in transaction ID is not a valid month")
                else:
                    values['transaction_id'] = None
        else:
            values['transaction_id'] = None
        return values
    
    @model_validator(mode="before")
    def transaction_date_validator(cls, values):
        transaction_date = values['transaction_date']
        if isinstance(transaction_date, date):
            values['transaction_date'] = transaction_date.strftime("%Y-%m-%d")
        elif isinstance(transaction_date, str):
            if not re.search("^\d{4}-\d{2}-\d{2}\Z", transaction_date):
                raise ValueError(f"{model_name} Error: transaction date not in proper format")
            else:
                try:
                    values['transaction_date'] = datetime.strptime(transaction_date, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError(f"{model_name} Error: invalid transaction date")
        else:
            raise TypeError(f"{model_name} Error: transaction date invalid type")
        return values
    
    @model_validator(mode="before")
    def account_number_validator(cls, values):
        account_number = values['account_number']
        if not isinstance(account_number, str):
            raise TypeError(f"{model_name} Error: incorrect account ID data type \'{type(account_number).__name__}\'")
        if len(account_number) < 5:
            raise ValueError(f"{model_name} Error: account number minimum field length not met")
        if len(account_number) > 15:
            raise ValueError(f"{model_name} Error: account number maximum length is 15")
        return values
    
    @model_validator(mode="before")
    def entry_type_validator(cls, values):
        entry_type = values['entry_type']
        if not isinstance(entry_type, str):
            raise TypeError(f"{model_name} Error: incorrect entry type data type \'{type(entry_type).__name__}\'")
        if entry_type not in transaction_types:
            raise ValueError(f"Error: Unknown entry type \'{entry_type}\'")
        return values
    
    @model_validator(mode="before")
    def description_validator(cls, values):
        if 'description' in values.keys():
            description = values['description']
            if not isinstance(description, str) and description is not None:
                raise TypeError(f"{model_name} Error: incorrect description data type \'{type(description).__name__}\'")
            if description is not None and len(description) > 50:
                raise ValueError(f"{model_name} Error: description field maximum length is 50")
        return values
    
    @model_validator(mode="before")
    def amount_validator(cls, values):
        amount = values['amount']
        if isinstance(amount, str):
            raise TypeError(f"{model_name} Error: incorrect amount data type \'{type(amount).__name__}\'")
        return values
    
    @model_validator(mode="before")
    def currency_code_validator(cls, values):
        if 'currency_code' in values.keys():
            currency_code = values['currency_code']
            if len(currency_code) != 3:
                raise ValueError(f"{model_name} Error: currency code required length is 3")
            if currency_code != "PHP":
                raise ValueError(f"{model_name} Error: invalid currency code \'{currency_code}\'")
        else:
            values['currency_code'] = "PHP"
        return values

    @model_validator(mode="before")
    def posting_date_validator(cls, values):
        if 'posting_date' in values.keys():
            posting_date = values['posting_date']
            if isinstance(posting_date, date):
                values['posting_date'] = posting_date.strftime("%Y-%m-%d")
            elif isinstance(posting_date, str):
                if not re.search("^\d{4}\d{2}\-\d{5}\Z", posting_date):
                    raise ValueError(f"{model_name} Error: posting date not in proper format")
                else:
                    try:
                        values['posting_date'] = datetime.strptime(posting_date, "%Y-%m-%d").date()
                    except ValueError:
                        raise ValueError(f"{model_name} Error: invalid posting date")
            elif isinstance(posting_date, type(None)):
                values['posting_date'] = None
            else:
                raise TypeError(f"{model_name} Error: posting date invalid type")
        else:
            values['posting_date'] = None
        return values
    
    @model_validator(mode="before")
    def status_validator(cls, values):
        if 'status' in values.keys():
            status = values['status']
            if not isinstance(status, type(None)) and status not in allowed_status:
                raise ValueError(f"{model_name} Error: invalid status \'{status}\'")
        else:
            values['status'] = None
        return values
    
    @model_validator(mode="before")
    def created_date_validator(cls, values):
        if 'created_date' in values.keys():
            created_date = values['created_date']
            if created_date is not None:
                if isinstance(created_date, datetime):
                    values['created_date'] = created_date.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(created_date.microsecond / 1000):03d}"
                else:
                    values['created_date'] = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S.%f")
        return values
    
    @model_validator(mode="before")
    def updated_date_validator(cls, values):
        if 'updated_date' in values.keys():
            updated_date = values['updated_date']
            if updated_date is not None:
                if isinstance(updated_date, datetime):
                    values['updated_date'] = updated_date.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(updated_date.microsecond / 1000):03d}"
                else:
                    values['updated_date'] = datetime.strptime(updated_date, "%Y-%m-%d %H:%M:%S.%f")
        return values
