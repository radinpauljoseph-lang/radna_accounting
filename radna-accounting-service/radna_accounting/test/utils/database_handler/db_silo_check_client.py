from abc import ABC, abstractmethod
import copy
import pandas as pd
from sqlalchemy import create_engine, text

class DbSiloCheckClient(ABC):

    def __init__(self, creds: dict = None):
        self.credentials = creds
        self.engine = None
        self.command = None
        self.data = None
        self.result = None

    @abstractmethod
    def connect(self):
        pass

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
