import logging
from .config import (
    meta,
    engine
)
from ..models.chart_of_accounts import (
    chart_of_accounts
)
from ..models.journal_entry import (
    journal_entry
)
from ..models.journal_entry_history import (
    journal_entry_history
)
from ..models.accounting_periods import (
    accounting_periods
)
from ..models.transaction_id_tracker import (
    transaction_id_tracker
)
from sqlalchemy import inspect
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
table_definitions = [
    chart_of_accounts.name,
    journal_entry.name,
    journal_entry_history.name,
    accounting_periods.name,
    transaction_id_tracker.name
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


