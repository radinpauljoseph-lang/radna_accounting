import pytest
from datetime import datetime, timezone, timedelta
from radna_accounting.validators.accounting_periods import AccountingPeriodsModel
from radna_accounting.models.accounting_periods import (
    acp_meta,
    acp_status
)
from radna_accounting.core.accounting_periods.accounting_periods import AccountingPeriodsCore
from radna_accounting.test.data.accounting_periods import AccountingPeriodsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.test.helpers.helpers import check_month_year_period_availability

from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials

class TestAccountingPeriodsCloseAccountingPeriod:

    def test_happy_path(self):
        payload = AccountingPeriodsPayloadGenerator().model_dump()
        
        while True:
            is_available = check_month_year_period_availability(month=payload[acp_meta.MONTH], year=payload[acp_meta.YEAR])
            current_datetime = datetime.now()
            end_datetime = current_datetime + timedelta(seconds=30)
            if is_available:
                payload = AccountingPeriodsPayloadGenerator().model_dump()
                is_available = check_month_year_period_availability(month=payload[acp_meta.MONTH], year=payload[acp_meta.YEAR])
        
                if current_datetime >= end_datetime:
                    raise Exception({
                        "error": "Failed to generate new Accounting Period Month and Year"
                    })
            else:
                break
        
        payload = AccountingPeriodsModel(**payload)
        payload.status = acp_status.OPEN
        
        AccountingPeriodsCore().insertRecord(payload)

        AccountingPeriodsCore().closeAccountingPeriod(
            month=payload.month,
            year=payload.year
        )

        payload.status = acp_status.CLOSED

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
                    .connect()\
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
                .execute({
                    "period_month": payload.month,
                    "period_year": payload.year,
                    "period_status": payload.status
                })
        
        result = db_obj.getData()
        
        assert result.shape[0] == 1

    def test_close_nonexistent_period(self):
        expected = "ACP0103"
        payload = AccountingPeriodsPayloadGenerator().model_dump()
        
        while True:
            is_available = check_month_year_period_availability(month=payload[acp_meta.MONTH], year=payload[acp_meta.YEAR])
            current_datetime = datetime.now()
            end_datetime = current_datetime + timedelta(seconds=30)
            if is_available:
                payload = AccountingPeriodsPayloadGenerator().model_dump()
                is_available = check_month_year_period_availability(month=payload[acp_meta.MONTH], year=payload[acp_meta.YEAR])
                
                if current_datetime >= end_datetime:
                    raise Exception({
                        "error": "Failed to generate new Accounting Period Month and Year"
                    })
            else:
                break

        payload = AccountingPeriodsModel(**payload)
        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsCore().closeAccountingPeriod(
                month=payload.month,
                year=payload.year
            )
        assert expected in str(excinfo)

    def test_close_closed_period(self):
        expected = "ACP0101"
        payload = AccountingPeriodsPayloadGenerator().model_dump()
        
        while True:
            is_available = check_month_year_period_availability(month=payload[acp_meta.MONTH], year=payload[acp_meta.YEAR])
            current_datetime = datetime.now()
            end_datetime = current_datetime + timedelta(seconds=30)
            if is_available:
                payload = AccountingPeriodsPayloadGenerator().model_dump()
                is_available = check_month_year_period_availability(month=payload[acp_meta.MONTH], year=payload[acp_meta.YEAR])
        
                if current_datetime >= end_datetime:
                    raise Exception({
                        "error": "Failed to generate new Accounting Period Month and Year"
                    })
            else:
                break
        
        payload = AccountingPeriodsModel(**payload)
        payload.status = acp_status.OPEN
        
        AccountingPeriodsCore().insertRecord(payload)

        AccountingPeriodsCore().closeAccountingPeriod(
            month=payload.month,
            year=payload.year
        )
        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsCore().closeAccountingPeriod(
                month=payload.month,
                year=payload.year
            )
        assert expected in str(excinfo)

