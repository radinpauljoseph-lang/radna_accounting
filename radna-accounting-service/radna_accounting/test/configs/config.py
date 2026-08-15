from pydantic import BaseModel

class SQLiteTestDatabaseCredentials(BaseModel):
    database: str = "temp_state.db"
