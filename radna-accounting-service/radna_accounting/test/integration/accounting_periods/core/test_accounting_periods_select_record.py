import pytest
from datetime import datetime, timezone, timedelta
from radna_accounting.validators.data_model import DATA_KEY
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

class TestAccountingPeriodsSelectRecord:

    def test_happy_path(self):
        payload = AccountingPeriodsPayloadGenerator().model_dump()
        where_clause_values = {
            "period_month": payload[acp_meta.MONTH],
            "period_year": payload[acp_meta.YEAR]
        }

        while True:
            is_available = check_month_year_period_availability(where_clause_values)
            current_datetime = datetime.now()
            end_datetime = current_datetime + timedelta(seconds=30)
            if is_available:
                payload = AccountingPeriodsPayloadGenerator().model_dump()
                where_clause_values = {
                    "period_month": payload[acp_meta.MONTH],
                    "period_year": payload[acp_meta.YEAR]
                }
                is_available = check_month_year_period_availability(where_clause_values)
        
                if current_datetime >= end_datetime:
                    raise Exception({
                        "error": "Failed to generate new Accounting Period Month and Year"
                    })
            else:
                break

        payload = AccountingPeriodsModel(**payload)
        payload.status = acp_status.OPEN

        AccountingPeriodsCore().insertRecord(payload)
        data = AccountingPeriodsCore().selectRecord(
            month=payload.month,
            year=payload.year
        )

        assert data[DATA_KEY][acp_meta.MONTH] == payload.month
        assert data[DATA_KEY][acp_meta.YEAR] == payload.year
        assert data[DATA_KEY][acp_meta.STATUS] == payload.status

    def test_nonexistent_accounting_period(self):
        payload = AccountingPeriodsPayloadGenerator().model_dump()
        where_clause_values = {
            "period_month": payload[acp_meta.MONTH],
            "period_year": payload[acp_meta.YEAR]
        }

        while True:
            is_available = check_month_year_period_availability(where_clause_values)
            current_datetime = datetime.now()
            end_datetime = current_datetime + timedelta(seconds=30)
            if is_available:
                payload = AccountingPeriodsPayloadGenerator().model_dump()
                where_clause_values = {
                    "period_month": payload[acp_meta.MONTH],
                    "period_year": payload[acp_meta.YEAR]
                }
                is_available = check_month_year_period_availability(where_clause_values)
        
                if current_datetime >= end_datetime:
                    raise Exception({
                        "error": "Failed to generate new Accounting Period Month and Year"
                    })
            else:
                break

        payload = AccountingPeriodsModel(**payload)
        data = AccountingPeriodsCore().selectRecord(
            month=payload.month,
            year=payload.year
        )
        
        assert data is None



