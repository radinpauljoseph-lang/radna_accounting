from datetime import datetime
import uuid
import copy
from uuid import UUID
from pydantic import BaseModel, model_validator, Field

from ..models.accounting_periods import (
    acp_meta,
    acp_status
)
from ..configs.response_codes.mapping import (
     ACP_CODE,
     HIS_CODE,
     MESSAGE_KEY,
     error_map
)

model_name = "AccountingPeriodsModel"

accounting_period_statuses = acp_status.getStatusAsList()

supported_history_operations = [
    "I",
    "U",
    "D"
]

class AccountingPeriodsModel(BaseModel):
    month: int | None = None
    year: int | None = None
    status: str | None = None
    created_date: str | datetime | None = None
    updated_date: str | datetime | None = None

    @model_validator(mode="before")
    def month_validator(cls, values):
        month = values[acp_meta.MONTH]
        if not isinstance(month, int):
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}0001"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(month).__name__
            )
            raise Exception(error)
        if int(month) < 1  or int(month) > 12:
          error = copy.deepcopy(error_map.get(f"{ACP_CODE}0002"))
          raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def year_validator(cls, values):
        year = values[acp_meta.YEAR]
        if not isinstance(year, int):
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}0003"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(year).__name__
            )
            raise Exception(error)
        if int(year) < 1000  or int(year) > 9999:
          error = copy.deepcopy(error_map.get(f"{ACP_CODE}0004"))
          raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def month_year_validator(cls, values):
        year = int(values[acp_meta.YEAR]) if isinstance(values[acp_meta.YEAR], str) else values[acp_meta.YEAR]
        month = int(values[acp_meta.MONTH]) if isinstance(values[acp_meta.MONTH], str) else values[acp_meta.MONTH]
        current_date = datetime.now()
        if year > current_date.year:
          error = copy.deepcopy(error_map.get(f"{ACP_CODE}0005"))
          raise Exception(error)
        else:
             if year == current_date.year:
                  if month > current_date.month:
                    error = copy.deepcopy(error_map.get(f"{ACP_CODE}0005"))
                    raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def status_validator(cls, values):
        if acp_meta.STATUS in values.keys():
            status = values[acp_meta.STATUS]
            if not isinstance(status, str):
                error = copy.deepcopy(error_map.get(f"{ACP_CODE}0007"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    variable_type=type(status).__name__
                )
                raise Exception(error)
            if status not in accounting_period_statuses:
                error = copy.deepcopy(error_map.get(f"{ACP_CODE}0006"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    status=status
                )
                raise Exception(error)
        return values
    

    @model_validator(mode="before")
    def created_date_converter(cls, values):
        if acp_meta.CREATED_DATE in values.keys():
            created_date = values[acp_meta.CREATED_DATE]
            if created_date is not None:
                if isinstance(created_date, str):
                    values[acp_meta.CREATED_DATE] = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S.%f")
        return values
    
    @model_validator(mode="before")
    def updated_date_converter(cls, values):
        if acp_meta.UPDATED_DATE in values.keys():
            updated_date = values[acp_meta.UPDATED_DATE]
            if updated_date is not None:
                if isinstance(updated_date, str):
                    values[acp_meta.UPDATED_DATE] = datetime.strptime(updated_date, "%Y-%m-%d %H:%M:%S.%f")
        return values
    
class AccountingPeriodsHistoryModel(AccountingPeriodsModel):
    history_id: UUID = Field(default_factory=lambda: uuid.uuid4())
    history_date: str | datetime | None = Field(default_factory=lambda: datetime.now())
    history_operation: str | None = None
    
    @model_validator(mode="before")
    def history_opertation_validator(cls, values):
        history_operation = values[acp_meta.HISTORY_OPERATION]
        if history_operation not in supported_history_operations:
            error = copy.deepcopy(error_map.get(f"{ACP_CODE}{HIS_CODE}0001"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                history_operation=history_operation
            )
            raise Exception(error)
        return values

    