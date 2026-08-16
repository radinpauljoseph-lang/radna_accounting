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
from radna_accounting.test.data.db.accounting_periods.queries import SelectAccountingPeriodDetails
from radna_accounting.test.data.db.constants import SQL_TEXT_FIELD

class TestAccountingPeriodsCloseAccountingPeriod:

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

        AccountingPeriodsCore().closeAccountingPeriod(
            month=payload.month,
            year=payload.year
        )

        payload.status = acp_status.CLOSED

        sql_query_details = SelectAccountingPeriodDetails(
            period_month=payload.month,
            period_year=payload.year,
            period_status=payload.status
        )

        db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
                    .connect()\
                    .setCommand(sql_query_details.text)\
                    .execute(sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))
        result = db_obj.getData()
        
        assert result.shape[0] == 1

    def test_close_nonexistent_period(self):
        expected = "ACP0103"
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

