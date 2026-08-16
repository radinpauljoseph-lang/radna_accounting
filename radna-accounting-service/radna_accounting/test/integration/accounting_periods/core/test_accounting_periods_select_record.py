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
from radna_accounting.test.helpers.helpers import checkMonthYearPeriodAvailability

class TestAccountingPeriodsSelectRecord:

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
        data = AccountingPeriodsCore().selectRecord(
            month=payload.month,
            year=payload.year
        )

        assert data[DATA_KEY][acp_meta.MONTH] == payload.month
        assert data[DATA_KEY][acp_meta.YEAR] == payload.year
        assert data[DATA_KEY][acp_meta.STATUS] == payload.status

    def test_nonexistent_accounting_period(self):
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
        data = AccountingPeriodsCore().selectRecord(
            month=payload.month,
            year=payload.year
        )
        
        assert data is None



