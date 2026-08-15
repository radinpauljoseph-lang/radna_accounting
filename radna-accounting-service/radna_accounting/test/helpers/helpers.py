
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials

def check_month_year_period_availability(month: int, year: int):
    db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
        .connect()\
        .setCommand(f"""
        select
            month,
            year
        from accounting_periods
        where 1=1
        and month = :period_month
        and year = :period_year
        """
        )\
        .execute({
            "period_month": month,
            "period_year": year
        })

    result = db_obj.getData()
    return True if result.shape[0] > 0 else False