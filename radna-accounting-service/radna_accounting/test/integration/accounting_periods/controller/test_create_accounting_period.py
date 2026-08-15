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
from radna_accounting.test.configs.config import SQLiteTestDatabaseCredentials

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

        acp_db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
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
            "period_month": payload[acp_meta.MONTH],
            "period_year": payload[acp_meta.YEAR],
            "period_status": acp_status.OPEN
        })

        ti_db_obj = SQLiteClient(SQLiteTestDatabaseCredentials().model_dump())\
            .connect()\
            .setCommand(f"""
            select
                month,
                year
                id
            from transaction_ids
            where 1=1
            and month = :ti_month
            and year = :ti_year
            and id = :ti_id
            """
            )\
            .execute({
                "ti_month": payload[acp_meta.MONTH],
                "ti_year": payload[acp_meta.YEAR],
                "ti_id": FIRST_ID
            })

        error_messages = []

        db_checks = [
            (acp_db_obj, "accounting_periods"),
            (ti_db_obj, "transaction_ids"),
        ]
        for db_obj, table_name in db_checks:
            if len(db_obj.getData()) != 1:
                error_messages.append(
                    f"Data Issue encountered in {table_name} table"
                )

        assert len(error_messages) == 0, ", ".join(error_messages)
