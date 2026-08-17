import copy
import pandas as pd
from sqlalchemy import create_engine, text

from radna_accounting.test.utils.database_handler.db_silo_check_client import DbSiloCheckClient
from radna_accounting.test.utils.database_handler.url_handler import sqliteUrlConvert


class SQLiteClient(DbSiloCheckClient):

    def __init__(self, creds: dict = None):
        super().__init__(creds)
        self.__credentials = self.__credentials if creds is None else\
            sqliteUrlConvert(creds)

    def connect(self, creds=None):
        self.__credentials = self.__credentials if creds is None else\
            sqliteUrlConvert(creds)
        self._engine = create_engine(self.__credentials)

        return self
    