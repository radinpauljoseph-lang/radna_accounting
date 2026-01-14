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
    journal_entry
)
from ..models.accounting_periods import (
    accounting_periods
)
from ..models.transaction_id_tracker import (
    transaction_id_tracker
)

table_definitions = [
    chart_of_accounts.name,
    journal_entry.name,
    accounting_periods.name,
    transaction_id_tracker.name
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


