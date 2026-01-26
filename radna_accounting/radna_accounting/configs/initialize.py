from sqlalchemy import inspect
from .config import (
    loggerOutput,
    meta,
    engine
)
from ..models.chart_of_accounts import (
    chart_of_accounts
)
from ..models.journal_entry import (
    journal_entry,
    journal_entry_history
)
from ..models.accounting_periods import (
    accounting_periods
)
from ..models.transaction_ids import transaction_ids

table_definitions = [
    chart_of_accounts.name,
    journal_entry.name,
    journal_entry_history.name,
    accounting_periods.name,
    transaction_ids.name
]
def initialize():
    inspector = inspect(engine)
    for index in range(len(table_definitions)):
        if inspector.has_table(table_definitions[index]):
            loggerOutput(message=f"{table_definitions[index]} table already exists")
            continue
        else:
            loggerOutput(message="Execute meta.create_all")
            meta.create_all(engine)
            loggerOutput(message="SUCCESS meta.create_all")
            break


