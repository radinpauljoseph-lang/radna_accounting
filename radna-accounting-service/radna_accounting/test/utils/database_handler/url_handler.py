from sqlalchemy.engine import URL
import copy

postgres_keys = [
    "host",
    "port",
    "username",
    "password",
    "database"
]
sqlite_keys = [
    "database"
]

def postgreUrlConvert(data):
    if type(data) is not dict:
        raise Exception({
            "error": "invalid data type"
        })
    url = copy.deepcopy(data)
    url["drivername"] = "postgresql+psycopg2"
    url = URL.create(**url)

    return url

def sqliteUrlConvert(data):
    if type(data) is not dict:
        raise Exception({
            "error": "invalid data type"
        })
    url = copy.deepcopy(data)
    url["drivername"] = "sqlite"
    url = URL.create(**url)
    
    return url
