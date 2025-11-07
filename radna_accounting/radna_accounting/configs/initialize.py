import logging
from .config import (
    meta,
    engine
)
from ..models.chart_of_accounts import (
    chart_of_accounts
)
from sqlalchemy import inspect
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
table_definitions = [
    chart_of_accounts.name
]
def initialize():
    inspector = inspect(engine)
    for index in range(len(table_definitions)):
        if inspector.has_table(table_definitions[index]):
            logger.info(f"{table_definitions[index]} table already exists")
            continue
        else:
            logging.info("Execute meta.create_all")
            meta.create_all(engine)
            logging.info("SUCCESS meta.create_all")
            break


