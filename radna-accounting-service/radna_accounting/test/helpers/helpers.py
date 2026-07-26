
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
creds = {
    "database": "temp_state.db"
}

def check_month_year_period_availability(month: int, year: int):
    where_clause_values = {
        "period_month": month,
        "period_year": year
    }
    db_obj = SQLiteClient(creds)\
        .connect(creds)\
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
        .execute(where_clause_values)

    result = db_obj.getData()
    return True if result.shape[0] > 0 else False