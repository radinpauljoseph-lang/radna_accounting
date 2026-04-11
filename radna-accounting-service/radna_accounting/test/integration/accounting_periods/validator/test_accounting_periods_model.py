import pytest
from datetime import datetime
import pandas as pd
from radna_accounting.validators.accounting_periods import AccountingPeriodsModel
from radna_accounting.models.accounting_periods import (
    acp_meta,
    acp_status
)
from radna_accounting.test.data.accounting_periods import AccountingPeriodsPayloadGenerator

class TestAccountingPeriodsModel:

    def test_happy_path(self):
        payload = AccountingPeriodsPayloadGenerator().model_dump()

        payload = AccountingPeriodsModel(**payload)

        assert isinstance(payload, AccountingPeriodsModel) is True

    @pytest.mark.parametrize("param", [1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_month_invalid_data_type(self, param):
        expected = "ACP0001"
        payload = AccountingPeriodsPayloadGenerator(
            month=param
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsModel(**payload)
        assert expected in str(excinfo)
    
    @pytest.mark.parametrize("param", [0, 13])
    def test_month_invalid_range(self, param):
        expected = "ACP0002"
        payload = AccountingPeriodsPayloadGenerator(
            month=param
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_year_invalid_data_type(self, param):
        expected = "ACP0003"
        payload = AccountingPeriodsPayloadGenerator(
            year=param
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsModel(**payload)
        print("@@@@@@@@@@@@@@")
        print(payload)
        print(str(excinfo))
        print("@@@@@@@@@@@@@@")
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [0, 1, 999, 10000])
    def test_year_invalid_range(self, param):
        expected = "ACP0004"
        payload = AccountingPeriodsPayloadGenerator(
            year=param
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, 2, 3])
    def test_month_year_invalid_month(self, param):
        expected = "ACP0005"
        current_datetime = datetime.now()
        future_datetime = current_datetime + pd.DateOffset(months=param)

        payload = AccountingPeriodsPayloadGenerator(
            month=future_datetime.month,
            year=future_datetime.year
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, 2, 3])
    def test_month_year_invalid_year(self, param):
        expected = "ACP0005"
        current_datetime = datetime.now()
        future_datetime = current_datetime + pd.DateOffset(years=param)

        payload = AccountingPeriodsPayloadGenerator(
            month=future_datetime.month,
            year=future_datetime.year
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_status_invalid_data_type(self, param):
        expected = "ACP0007"

        payload = AccountingPeriodsPayloadGenerator().model_dump()
        payload[acp_meta.STATUS] = param

        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", ["open", "closed", "NEW", "REJECTED"])
    def test_status_invalid_status(self, param):
        expected = "ACP0006"

        payload = AccountingPeriodsPayloadGenerator().model_dump()
        payload[acp_meta.STATUS] = param

        with pytest.raises(Exception) as excinfo:
            AccountingPeriodsModel(**payload)
        assert expected in str(excinfo)


