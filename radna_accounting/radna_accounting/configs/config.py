import logging
from uuid import uuid4
from datetime import datetime, timezone
import os
import configparser
from pathlib import Path

from sqlalchemy import (
    create_engine,
    MetaData
)

logger = logging.getLogger(__name__)

class LoggerType():
    def __init__(self):
        self.INFO = "INFO"
        self.ERROR = "ERROR"

logger_types = LoggerType()

def loggerOutput(rrn: str = None, method: str = logger_types.INFO, message: str = ""):
    rrn = str(uuid4()) if rrn is None else rrn
    logger_type_map = {
        logger_types.INFO: logger.info,
        logger_types.ERROR: logger.error
    }
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")

    logger_type_map[method](f"[{now}][{rrn}] - {message}")

BASE_DIR = Path(__file__).resolve().parent
config_path = f"{str(BASE_DIR)}\\config.ini"

ENV = os.environ['ENV']
CONFIGS = configparser.ConfigParser()
# CONFIGS.read("C:\\radna_accounting\\radna_accounting\\radna_accounting\\configs\\config.ini")

CONFIGS.read(config_path)
DB_CONNECTION = CONFIGS[f"{ENV}.database"]['connection_string']

engine = create_engine(DB_CONNECTION, echo=True)

meta = MetaData()