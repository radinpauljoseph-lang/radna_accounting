import pytest
from datetime import datetime, timezone
from radna_accounting.validators.accounting_periods import AccountingPeriodsModel
from radna_accounting.models.accounting_periods import (
    acp_meta,
    acp_status
)
from radna_accounting.core.accounting_periods.accounting_periods import AccountingPeriodsCore
from radna_accounting.test.data.accounting_periods import AccountingPeriodsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.test.helpers.helpers import check_month_year_period_availability

creds = {
    "database": "temp_state.db"
}

class TestAccountingPeriodsInsertRecord:

    def test_happy_path(self):
        payload = AccountingPeriodsPayloadGenerator().model_dump()
        where_clause_values = {
            "period_month": payload[acp_meta.MONTH],
            "period_year": payload[acp_meta.YEAR]
        }
        is_available = check_month_year_period_availability(where_clause_values)

        while is_available:
            payload = AccountingPeriodsPayloadGenerator().model_dump()
            where_clause_values = {
                "period_month": payload[acp_meta.MONTH],
                "period_year": payload[acp_meta.YEAR]
            }
            is_available = check_month_year_period_availability(where_clause_values)

        payload = AccountingPeriodsModel(**payload)
        payload.status = acp_status.OPEN

        AccountingPeriodsCore().insertRecord(payload)

        where_clause_values = {
            "period_month": payload.month,
            "period_year": payload.year,
            "period_status": payload.status
        }

        db_obj = SQLiteClient(creds)\
            .connect(creds)\
            .setCommand(f"""
            select
                month,
                year,
                status
            from accounting_periods
            where 1=1
            and month = :period_month
            and year = :period_year
            and status = :period_status
        """
        )\
        .execute(where_clause_values)

        result = db_obj.getData()
        del db_obj

        assert result.shape[0] == 1

    def test_accounting_period_exists_error(self):
        expected = "ACP0102"
        payload = AccountingPeriodsPayloadGenerator().model_dump()
        where_clause_values = {
            "period_month": payload[acp_meta.MONTH],
            "period_year": payload[acp_meta.YEAR]
        }
        is_available = check_month_year_period_availability(where_clause_values)

        while is_available:
            payload = AccountingPeriodsPayloadGenerator().model_dump()
            where_clause_values = {
                "period_month": payload[acp_meta.MONTH],
                "period_year": payload[acp_meta.YEAR]
            }
            is_available = check_month_year_period_availability(where_clause_values)

        payload = AccountingPeriodsModel(**payload)
        payload.status = acp_status.OPEN

        AccountingPeriodsCore().insertRecord(payload)
        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsCore().insertRecord(payload)
        assert expected in str(excinfo)




