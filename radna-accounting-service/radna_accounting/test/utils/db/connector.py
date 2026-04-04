import logging
from .connection_handler import *
from .db_utils import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

'''
DB connector base class
- properties:
    - credentials: dictionary containing db credentials
    - columns: list containing column names to be assigned to a dataframe
    - data: pandas Dataframe containing data generated from executing SQL script
    - query_string: string of input SQL command
- methods:
    - connect
        initialize values and sets credential values to self.credentials
        - parameters:
            - creds: input credentials
    - set_sql_command:
        sets SQL command to self.query_string
        - parameters:
            - sql_script: input SQL command
    - set_columns:
        sets list of column names to self.columns
        parameters:
            - cols: input column names list
    - get_columns:
        returns list of columns
    - get_sql_command:
        returns input SQL command
    - execute:
        executes SQL commands
    - get_data:
        returns Dataframe data generated from execute method
    - create_copy:
        returns copy of DB client class along with all the information assoc. to the class used
'''
class BaseDBClient:
    def __init__(self, creds):
        logging.info("Connecting to Database...")
        self.credentials = creds
        self.query_string = str()
        self.data = None

    def connect(self, creds):
        logging.info("Connecting to Database...")
        self.credentials = creds
        self.query_string = str()
        self.data = None
        return self

    def set_sql_command(self, sql_script):
        self.query_string = sql_script
        return self
    
    def get_sql_command(self):
        return self.query_string

    def execute(self):
        execute(self.cursor, self.query_string)
        return self

    def get_data(self):
        cols = [desc[0] for desc in self.cursor.description]
        data = fetch_result(self.cursor)
        data = convert_to_dict(data, cols)
        data = convert_to_df(data, cols)
        self.data = data
        logging.info(f"SQL Result:\n{data.head()}")
        
        close_all(self.connection, self.cursor)
        return self.data
    
    def close(self):
        close_all(self.connection, self.cursor)
    def create_copy(self):
        pass

'''
DB connector for Postgres/RDS tables
- properties:
    - connection: psycopg2 connection object
    - cursor: cursor object derived from connect function
    - credentials: dictionary containing db credentials
    - columns: list containing column names to be assigned to a dataframe
    - data: pandas Dataframe containing data generated from executing SQL script
    - query_string: string of input SQL command
- methods:
    - connect
        initialize values and sets credential values to self.credentials
        sets connection and cursor to postgres database using input credentials
        - parameters:
            - creds: input credentials
    - set_sql_command:
        sets SQL command to self.query_string
        - parameters:
            - sql_script: input SQL command
    - set_columns:
        sets list of column names to self.columns
        parameters:
            - cols: input column names list
    - get_columns:
        returns list of columns
    - get_sql_command:
        returns input SQL command
    - execute:
        executes SQL commands
    - get_data:
        returns Dataframe data generated from execute method
    - create_copy:
        returns copy of DB client class along with all the information assoc. to the class used
'''
class PostgreSQLClient(BaseDBClient):
    def __init__(self, creds):
        super().__init__(creds)
        self.connection = postgres_connect(creds)
        self.cursor = self.connection.cursor()
        logging.info("Connected to PostgreSQL Database successfully")

    def connect(self, creds):
        super().connect(creds)
        self.connection = postgres_connect(creds)
        self.cursor = self.connection.cursor()
        logging.info("Connected to PostgreSQL Database successfully")
        return self

    def create_copy(self):
        return PostgreSQLClient(self.credentials)

'''
DB connector for SQLite tables
- properties:
    - connection: SQLite sql connection object
    - cursor: cursor object derived from connect function
    - credentials: dictionary containing db credentials
    - columns: list containing column names to be assigned to a dataframe
    - data: pandas Dataframe containing data generated from executing SQL script
    - query_string: string of input SQL command
- methods:
    - connect
        initialize values and sets credential values to self.credentials
        sets connection and cursor to databricks database using input credentials
        - parameters:
            - creds: input credentials
    - set_sql_command:
        sets SQL command to self.query_string
        - parameters:
            - sql_script: input SQL command
    - set_columns:
        sets list of column names to self.columns
        parameters:
            - cols: input column names list
    - get_columns:
        returns list of columns
    - get_sql_command:
        returns input SQL command
    - execute:
        executes SQL commands
    - get_data:
        returns Dataframe data generated from execute method
    - create_copy:
        returns copy of DB client class along with all the information assoc. to the class used
'''
class SQLiteClient(BaseDBClient):
    def __init__(self, creds):
        super().__init__(creds)
        self.connection = sqlite_connect(creds)
        self.cursor = self.connection.cursor()
        logging.info("Connected to SQLite successfully")

    def connect(self, creds):
        super().connect(creds)
        self.connection = sqlite_connect(creds)
        self.cursor = self.connection.cursor()
        logging.info("Connected to SQLite successfully")
        return self

    def create_copy(self):
        return SQLiteClient(self.credentials)