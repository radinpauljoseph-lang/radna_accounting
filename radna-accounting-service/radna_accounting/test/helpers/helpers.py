
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials
from radna_accounting.test.data.db.accounting_periods.queries import SelectAccountingPeriodByMonthYear
from radna_accounting.test.data.db.constants import SQL_TEXT_FIELD

def checkMonthYearPeriodAvailability(month: int, year: int):
    sql_query_details = SelectAccountingPeriodByMonthYear(
        period_month=month,
        period_year=year
    )
    db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
        .connect()\
        .setCommand(sql_query_details.text)\
        .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

    result = db_obj.getData()
    return True if result.shape[0] > 0 else False