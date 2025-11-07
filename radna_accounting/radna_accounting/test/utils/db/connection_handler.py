import psycopg2 as psy
import sqlite3 as sqlite
from sqlite3 import Error as sqliteError
from psycopg2 import Error as psyError
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

'''
connects to postgres/RDS database
- Parameters:
    - credentials: dictionary containing ff. fields
        - host
        - port
        - database
        - user
        - password
'''
def postgres_connect(credentials):
    try:
        credential_obj = {
            'host': credentials['host'],
            'port': credentials['port'],
            'database': credentials['database'],
            'user': credentials['user'],
            'password': credentials['password']
        }

        return psy.connect(
            host=credential_obj['host'], 
            port=credential_obj['port'], 
            database=credential_obj['database'], 
            user=credential_obj['user'], 
            password=credential_obj['password']
            )
    except (Exception, psyError) as error:
        logging.info("Failed to connect to Postgres: {} \n".format(error))
        raise

'''
connects to sqlite database
- Parameters:
    - credentials: dictionary containing ff. fields
        - file_name
'''

def sqlite_connect(credentials):
    try:
        credential_obj = {
            "file_name": credentials['file_name']
        }

        return sqlite.connect(credential_obj['file_name'])
    except (Exception, sqliteError) as error:
        logging.info("Failed to connect to SQLite: {} \n".format(error))
        raise

'''
closes connection & cursor object
'''
def close_all(conn, cursor):
    cursor.close()
    conn.close()

'''
executes SQL command provided in the parameter
- Parameters:
    - cursor: cursor object used to call its execute method
    - query: input SQL command
'''
def execute(cursor, query):
    try:
        logging.info("Running SQL: {}".format(query))
        cursor.execute(query)
    except Exception as error:
        logging.info("Error while running command: {} \n".format(error))
        raise

'''
returns all data inside a cursor object
'''
def fetch_result(cursor):
    return cursor.fetchall()