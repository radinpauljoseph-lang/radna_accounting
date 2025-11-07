from sqlalchemy import MetaData
import logging
import os
import configparser
from sqlalchemy import (
    create_engine,
    MetaData
)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

ENV = os.environ['ENV']
CONFIGS = configparser.ConfigParser()
CONFIGS.read("C:\\radna_accounting\\radna_accounting\\radna_accounting\\configs\\config.ini")

DB_CONNECTION = CONFIGS[f"{ENV}.database"]['connection_string']

engine = create_engine(DB_CONNECTION, echo=True)

meta = MetaData()