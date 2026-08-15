import copy
from datetime import datetime
from pydantic import BaseModel, model_validator

from radna_accounting.models.chart_of_accounts import (
    coa_meta,
    coa_types
)
from radna_accounting.configs.response_codes.mapping import (
    COA_CODE,
    MESSAGE_KEY,
    error_map
)

model_name = "ChartOfAccountsModel"
account_types = coa_types.getTypesAsList()

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
        account_id = values[coa_meta.ACCOUNT_ID]
        if not isinstance(account_id, str):
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0001"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(account_id).__name__
            )
            raise Exception(error)
        if len(account_id) < coa_meta.ACCOUNT_ID_MIN_LENGTH:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0002"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY]
            raise Exception(error)
        if len(account_id) > coa_meta.ACCOUNT_ID_LENGTH:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0003"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                account_id_length=coa_meta.ACCOUNT_ID_LENGTH
            )
            raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def account_name_validator(cls, values):
        account_name = values[coa_meta.NAME]
        if not isinstance(account_name, str):
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0004"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(account_name).__name__
            )
            raise Exception(error)
        if len(account_name) > coa_meta.NAME_LENGTH:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0005"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                name_length=coa_meta.NAME_LENGTH
            )
            raise Exception(error)
        if len(account_name) <= 0:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0006"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY]
            raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def account_type_validator(cls, values):
        account_type = values[coa_meta.TYPE]
        if not isinstance(account_type, str):
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0007"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(account_type).__name__
            )
            raise Exception(error)
        if account_type not in account_types:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0008"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                account_type=account_type
            )
            raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def account_description_validator(cls, values):
        if coa_meta.DESCRIPTION in values.keys():
            account_description = values[coa_meta.DESCRIPTION]
            if not isinstance(account_description, str) and account_description is not None:
                error = copy.deepcopy(error_map.get(f"{COA_CODE}0009"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    variable_type=type(account_description).__name__
                )
                raise Exception(error)
            if account_description is not None and len(account_description) > coa_meta.DESCRIPTION_LENGTH:
                error = copy.deepcopy(error_map.get(f"{COA_CODE}0010"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    description_length=coa_meta.DESCRIPTION_LENGTH
                )
                raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def account_mapping_validator(cls, values):
        if coa_meta.ACCOUNT_MAPPING in values.keys():
            account_mapping = values[coa_meta.ACCOUNT_MAPPING]
            if not isinstance(account_mapping, str) and account_mapping is not None:
                error = copy.deepcopy(error_map.get(f"{COA_CODE}0011"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    variable_type=type(account_mapping).__name__
                )
                raise Exception(error)
            if account_mapping is not None and len(account_mapping) > coa_meta.ACCOUNT_ID_LENGTH:
                error = copy.deepcopy(error_map.get(f"{COA_CODE}0012"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    account_id_length=coa_meta.ACCOUNT_ID_LENGTH
                )
                raise Exception(error)
            if isinstance(values[coa_meta.ACCOUNT_ID], str) and account_mapping == values[coa_meta.ACCOUNT_ID]:
                error = copy.deepcopy(error_map.get(f"{COA_CODE}0013"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY]
                raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def created_date_converter(cls, values):
        if coa_meta.CREATED_DATE in values.keys():
            created_date = values[coa_meta.CREATED_DATE]
            if created_date is not None:
                if isinstance(created_date, str):
                    values[coa_meta.CREATED_DATE] = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S.%f")
        return values
    
    @model_validator(mode="before")
    def updated_date_converter(cls, values):
        if coa_meta.UPDATED_DATE in values.keys():
            updated_date = values[coa_meta.UPDATED_DATE]
            if updated_date is not None:
                if isinstance(updated_date, str):
                    values[coa_meta.UPDATED_DATE] = datetime.strptime(updated_date, "%Y-%m-%d %H:%M:%S.%f")
        return values
