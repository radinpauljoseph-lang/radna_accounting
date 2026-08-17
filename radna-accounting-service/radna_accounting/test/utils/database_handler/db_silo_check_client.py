from abc import ABC, abstractmethod
import copy
import pandas as pd
from sqlalchemy import create_engine, text

class DbSiloCheckClient(ABC):

    def __init__(self, creds: dict = None):
        self.__credentials = creds
        self._engine = None
        self.__command = None
        self.__data = None
        self.__result = None

    @abstractmethod
    def connect(self):
        pass

    def setCommand(self, sql_command: str):
        self.__command = sql_command

        return self
    
    def execute(self, params: dict = None):
        engine = self._engine
        parameters = {} if params is None else copy.deepcopy(params)

        with engine.connect() as conn:
            self.__result = conn.execute(
                text(self.__command),
                parameters
            )
        
        return self
    
    def getData(self, result_type: str = "pandas"):
        if result_type == "pandas":
            self.__data = pd.DataFrame(
                self.__result,
                columns=self.__result.keys()
            )
        if result_type == "dict":
            self.__data = self.__result.mappings().all()
        return self.__data
    
