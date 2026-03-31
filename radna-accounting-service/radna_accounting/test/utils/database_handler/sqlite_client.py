import copy
import pandas as pd
from sqlalchemy import create_engine, text

from radna_accounting.test.utils.database_handler.db_silo_check_client import DbSiloCheckClient
from radna_accounting.test.utils.database_handler.url_handler import sqliteUrlConvert


class SQLiteClient(DbSiloCheckClient):

    def __init__(self, creds: dict = None):
        super().__init__(creds)
        self.credentials = self.credentials if creds is None else\
            sqliteUrlConvert(creds)

    def connect(self, creds=None):
        self.credentials = self.credentials if creds is None else\
            sqliteUrlConvert(creds)
        self.engine = create_engine(self.credentials)

        return self
    
    def setCommand(self, sql_command: str):
        self.command = sql_command

        return self
    
    def execute(self, params: dict = None):
        engine = self.engine
        parameters = {} if params is None else copy.deepcopy(params)

        with engine.connect() as conn:
            self.result = conn.execute(
                text(self.command),
                parameters
            )
        
        return self
    
    def getData(self, result_type: str = "pandas"):
        if result_type == "pandas":
            self.data = pd.DataFrame(
                self.result,
                columns=self.result.keys()
            )
        if result_type == "dict":
            self.data = self.result.mappings().all()
        return self.data
    
    def store(self):
        pass
        

