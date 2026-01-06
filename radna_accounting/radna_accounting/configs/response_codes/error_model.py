from pydantic import BaseModel

model_name = "ErrorModel"

class ErrorModel(BaseModel):
    status: int = 0
    code: str = ""
    message: str = ""
    details: str | None = None