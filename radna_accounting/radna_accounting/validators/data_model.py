from pydantic import BaseModel

model_name = "DataModel"

class DataModel(BaseModel):
    data: dict = {}