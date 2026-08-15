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
from radna_accounting.test.helpers.helpers import checkMonthYearPeriodAvailability

from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials

class TestAccountingPeriodsInsertRecord:

    def test_happy_path(self):
        payload = AccountingPeriodsPayloadGenerator().model_dump()

        while True:
            is_available = checkMonthYearPeriodAvailability(month=payload[acp_meta.MONTH], year=payload[acp_meta.YEAR])
            current_datetime = datetime.now()
            end_datetime = current_datetime + timedelta(seconds=30)
            if is_available:
                payload = AccountingPeriodsPayloadGenerator().model_dump()
                is_available = checkMonthYearPeriodAvailability(month=payload[acp_meta.MONTH], year=payload[acp_meta.YEAR])

                if current_datetime >= end_datetime:
                    raise Exception({
                        "error": "Failed to generate new Accounting Period Month and Year"
                    })
            else:
                break

        payload = AccountingPeriodsModel(**payload)
        payload.status = acp_status.OPEN

        AccountingPeriodsCore().insertRecord(payload)

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

    def test_accounting_period_exists_error(self):
        expected = "ACP0102"
        payload = AccountingPeriodsPayloadGenerator().model_dump()

        while True:
            is_available = checkMonthYearPeriodAvailability(month=payload[acp_meta.MONTH], year=payload[acp_meta.YEAR])
            current_datetime = datetime.now()
            end_datetime = current_datetime + timedelta(seconds=30)
            if is_available:
                payload = AccountingPeriodsPayloadGenerator().model_dump()
                is_available = checkMonthYearPeriodAvailability(month=payload[acp_meta.MONTH], year=payload[acp_meta.YEAR])
        
                if current_datetime >= end_datetime:
                    raise Exception({
                        "error": "Failed to generate new Accounting Period Month and Year"
                    })
            else:
                break

        payload = AccountingPeriodsModel(**payload)
        payload.status = acp_status.OPEN

        AccountingPeriodsCore().insertRecord(payload)
        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsCore().insertRecord(payload)
        assert expected in str(excinfo)




