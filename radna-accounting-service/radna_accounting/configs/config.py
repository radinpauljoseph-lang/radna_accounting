import logging
from uuid import uuid4
from datetime import datetime, timezone
import os
import platform
import configparser
from pathlib import Path

from sqlalchemy import (
    create_engine,
    MetaData
)

logger = logging.getLogger(__name__)

NO_ID = "NO_ID"

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

    logger_msg = f"[{now}][{rrn}] - {message}" if rrn != NO_ID else f"[{now}] - {message}"
    logger_type_map[method](logger_msg)

config_path = Path(__file__).parent / "config.ini"

BASE_DIR = Path(__file__).resolve().parent
ENV = os.environ['ENV']
CONFIGS = configparser.ConfigParser()

CONFIGS.read(config_path)
DB_CONNECTION = CONFIGS[f"{ENV}.database"]['connection_string']
engine = create_engine(DB_CONNECTION, echo=False)

meta = MetaData()