import re
from datetime import datetime
import copy
from pydantic import BaseModel, model_validator

from ..models.transaction_ids import ti_meta
from ..configs.response_codes.mapping import (
     TIS_CODE,
     MESSAGE_KEY,
     error_map
)

model_name = "TransactionIdsModel"

class TransactionIdsModel(BaseModel):
    month: int | None = None
    year: int | None = None
    id: str | None = None

    @model_validator(mode="before")
    def month_validator(cls, values):
        month = values[ti_meta.MONTH]
        if not isinstance(month, int):
            error = copy.deepcopy(error_map.get(f"{TIS_CODE}0001"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(month).__name__
            )
            raise Exception(error)
        if int(month) < 1  or int(month) > 12:
          error = copy.deepcopy(error_map.get(f"{TIS_CODE}0002"))
          raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def year_validator(cls, values):
        year = values[ti_meta.YEAR]
        if not isinstance(year, int):
            error = copy.deepcopy(error_map.get(f"{TIS_CODE}0003"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(year).__name__
            )
            raise Exception(error)
        if int(year) < 1000  or int(year) > 9999:
          error = copy.deepcopy(error_map.get(f"{TIS_CODE}0004"))
          raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def month_year_validator(cls, values):
        year = values[ti_meta.YEAR]
        month = values[ti_meta.MONTH]
        current_date = datetime.now()
        if year > current_date.year:
          error = copy.deepcopy(error_map.get(f"{TIS_CODE}0005"))
          raise Exception(error)
        else:
             if year == current_date.year:
                  if month > current_date.month:
                    error = copy.deepcopy(error_map.get(f"{TIS_CODE}0005"))
                    raise Exception(error)
        return values
    
    @model_validator(mode="before")
    def id_validator(cls, values):
         id = values[ti_meta.ID]
         if not isinstance(id, str):
            error = copy.deepcopy(error_map.get(f"{TIS_CODE}0006"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                variable_type=type(id).__name__
            )
            raise Exception(error)
         if len(id) > 5:
          error = copy.deepcopy(error_map.get(f"{TIS_CODE}0007"))
          error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
               id_length=ti_meta.ID_LENGTH
          )
          raise Exception(error)
         if not re.search("^\d{5}\Z", id):
              error = copy.deepcopy(error_map.get(f"{TIS_CODE}0008"))
              raise Exception(error)
         return values

    