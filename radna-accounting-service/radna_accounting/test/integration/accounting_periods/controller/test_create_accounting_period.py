import pytest
from datetime import datetime, timedelta
from radna_accounting.models.accounting_periods import (
    acp_meta,
    acp_status
)
from radna_accounting.controller.accounting_periods import AccountingPeriodsController
from radna_accounting.test.data.accounting_periods import AccountingPeriodsPayloadGenerator
from radna_accounting.test.utils.database_handler.sqlite_client import SQLiteClient
from radna_accounting.test.helpers.helpers import checkMonthYearPeriodAvailability
from radna_accounting.validators.transaction_ids import FIRST_ID
from radna_accounting.validators.data_model import DATA_KEY
from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials
from radna_accounting.test.data.db.accounting_periods.queries import SelectAccountingPeriodDetails
from radna_accounting.test.data.db.transaction_ids.queries import SelectTransactionIdsDetails
from radna_accounting.test.data.db.constants import SQL_TEXT_FIELD

class TestAccountingPeriodsControllerCreateAccountingPeriod:

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

        result = AccountingPeriodsController().createAccountingPeriod(payload)

        acp_sql_query_details = SelectAccountingPeriodDetails(
            period_month=payload[acp_meta.MONTH],
            period_year=payload[acp_meta.YEAR],
            period_status=acp_status.OPEN
        )
        ti_sql_query_details = SelectTransactionIdsDetails(
            ti_month=payload[acp_meta.MONTH],
            ti_year=payload[acp_meta.YEAR],
            ti_id=FIRST_ID
        )

        acp_db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(acp_sql_query_details.text)\
            .execute(acp_sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        ti_db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(ti_sql_query_details.text)\
            .execute(ti_sql_query_details.model_dump(exclude=SQL_TEXT_FIELD))

        assert acp_db_obj.getData().shape[0] == 1
        assert ti_db_obj.getData().shape[0] == 1
        assert result[DATA_KEY][acp_meta.MONTH] == payload[acp_meta.MONTH]
        assert result[DATA_KEY][acp_meta.YEAR] == payload[acp_meta.YEAR]
        assert result[DATA_KEY][acp_meta.STATUS] == acp_status.OPEN
