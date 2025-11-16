from pydantic import BaseModel, model_validator
from datetime import datetime
import re

model_name = "TransactionIdTrackerModel"

accounting_period_statuses = [
     "OPEN",
     "CLOSED"
]
class TransactionIdTrackerModel(BaseModel):
    month: int | None = None
    year: int | None = None
    id: str | None = None

    @model_validator(mode="before")
    def month_validator(cls, values):
        month = values['month']
        if not isinstance(month, int):
            raise TypeError(f"{model_name} Error: incorrect month data type \'{type(month).__name__}\'")
        if 1 > int(month)  or int(month) > 12:
             raise ValueError(f"{model_name} Error: value is not a valid month")
        return values
    
    @model_validator(mode="before")
    def year_validator(cls, values):
        year = values['year']
        if not isinstance(year, int):
            raise TypeError(f"{model_name} Error: incorrect year data type \'{type(year).__name__}\'")
        if int(year) < 1000  or int(year) > 9999:
                raise ValueError(f"{model_name} Error: value is not a valid year")
        return values
    
    @model_validator(mode="before")
    def month_year_validator(cls, values):
        year = values['year']
        month = values['month']
        current_date = datetime.now()
        if year > current_date.year:
             raise ValueError(f"{model_name} Error: future accounting period is not allowed")
        else:
             if year == current_date.year:
                  if month > current_date.month:
                       raise ValueError(f"{model_name} Error: future accounting period is not allowed")
        return values
    
    @model_validator(mode="before")
    def id_validator(cls, values):
         id = values['id']
         if not isinstance(id, str):
            raise TypeError(f"{model_name} Error: incorrect account ID data type \'{type(id).__name__}\'")
         if len(id) > 5:
              raise ValueError(f"{model_name} Error: ID length should not be greater than 5")
         if not re.search("^\d{5}\Z", id):
              raise ValueError(f"{model_name} Error: ID not in proper format")
         return values

    