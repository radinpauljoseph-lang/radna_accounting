from sqlalchemy import MetaData
import logging
import os
import configparser
from pathlib import Path

from sqlalchemy import (
    create_engine,
    MetaData
)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
config_path = f"{str(BASE_DIR)}\\config.ini"

ENV = os.environ['ENV']
CONFIGS = configparser.ConfigParser()
# CONFIGS.read("C:\\radna_accounting\\radna_accounting\\radna_accounting\\configs\\config.ini")

CONFIGS.read(config_path)
DB_CONNECTION = CONFIGS[f"{ENV}.database"]['connection_string']

engine = create_engine(DB_CONNECTION, echo=True)

meta = MetaData()