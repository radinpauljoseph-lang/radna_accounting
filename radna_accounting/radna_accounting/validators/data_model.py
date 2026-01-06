from pydantic import BaseModel

model_name = "DataModel"

DATA_KEY = 'data'
class DataModel(BaseModel):
    data: dict = {}