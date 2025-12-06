from pydantic import BaseModel, model_validator
from datetime import datetime
import uuid
from uuid import UUID

model_name = "ChartOfAccountsModel"
account_types = [
    'ASSET',
    'LIABILITY',
    'EQUITY',
    'REVENUE',
    'EXPENSES'
]

class ChartOfAccountsModel(BaseModel):
    account_id: str = ""
    name: str = ""
    type: str = ""
    description: str | None = None
    account_mapping: str | None = None
    created_date: str | datetime | None = None
    updated_date: str | datetime | None = None

    @model_validator(mode="before")
    def account_id_validator(cls, values):
        account_id = values['account_id']
        if not isinstance(account_id, str):
            raise TypeError(f"{model_name} Error: incorrect account ID data type \'{type(account_id).__name__}\'")
        if len(account_id) < 5:
            raise ValueError(f"{model_name} Error: account ID minimum field length not met")
        if len(account_id) > 15:
            raise ValueError(f"{model_name} Error: account ID maximum length is 15")
        return values
    
    @model_validator(mode="before")
    def account_name_validator(cls, values):
        account_name = values['name']
        if not isinstance(account_name, str):
            raise TypeError(f"{model_name} Error: incorrect account name data type \'{type(account_name).__name__}\'")
        if len(account_name) > 150:
            raise ValueError(f"{model_name} Error: account name maximum length is 150")
        if len(account_name) <= 0:
            raise ValueError(f"{model_name} Error: account name minimum length is 1")
        return values
    
    @model_validator(mode="before")
    def account_type_validator(cls, values):
        account_type = values['type']
        if not isinstance(account_type, str):
            raise TypeError(f"{model_name} Error: incorrect account type data type \'{type(account_type).__name__}\'")
        if account_type not in account_types:
            raise ValueError(f"Error: Unknown account type \'{account_type}\'")
        return values
    
    @model_validator(mode="before")
    def account_description_validator(cls, values):
        if 'description' in values.keys():
            account_description = values['description']
            if not isinstance(account_description, str) and account_description is not None:
                raise TypeError(f"{model_name} Error: incorrect account description data type \'{type(account_description).__name__}\'")
            if account_description is not None and len(account_description) > 300:
                raise ValueError(f"{model_name} Error: account description field maximum length is 300")
        return values
    
    @model_validator(mode="before")
    def account_mapping_validator(cls, values):
        if 'account_mapping' in values.keys():
            account_mapping = values['account_mapping']
            if not isinstance(account_mapping, str) and account_mapping is not None:
                raise TypeError(f"{model_name} Error: incorrect account mapping data type \'{type(account_mapping).__name__}\'")
            if account_mapping is not None and len(account_mapping) > 50:
                raise ValueError(f"{model_name} Error: account mapping field maximum length is 50")
            if isinstance(values['account_id'], str) and account_mapping == values['account_id']:
                raise ValueError(f"{model_name} Error: account mapping value should not be the same as its account ID")
        return values
    
    @model_validator(mode="before")
    def created_date_validator(cls, values):
        if 'created_date' in values.keys():
            created_date = values['created_date']
            if created_date is not None:
                if isinstance(created_date, str):
                    values['created_date'] = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S.%f")
        return values
    
    @model_validator(mode="before")
    def updated_date_validator(cls, values):
        if 'updated_date' in values.keys():
            updated_date = values['updated_date']
            if updated_date is not None:
                if isinstance(updated_date, str):
                    values['updated_date'] = datetime.strptime(updated_date, "%Y-%m-%d %H:%M:%S.%f")
        return values
