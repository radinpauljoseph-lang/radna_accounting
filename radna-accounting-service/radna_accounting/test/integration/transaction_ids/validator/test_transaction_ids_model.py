import pytest
import string
import random
from datetime import datetime
from radna_accounting.validators.transaction_ids import (
    TransactionIdsModel,
    FIRST_ID
)
from radna_accounting.test.data.transaction_ids import TransactionIdsPayloadGenerator


current_month_year_skip_condition = datetime.now()
class TestTransactionIdsModel:

    def test_happy_path_current_year(self):
        current_datetime = datetime.now()

        payload = TransactionIdsPayloadGenerator(
            month=random.randint(1, current_datetime.month),
            year=current_datetime.year,
            id=FIRST_ID
        ).model_dump()

        payload = TransactionIdsModel(**payload)

        assert isinstance(payload, TransactionIdsModel) is True

    @pytest.mark.parametrize("param", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    def test_happy_path_previous_year(self, param):
        current_datetime = datetime.now()
        previous_year = random.randint(1001, current_datetime.year - 1)

        payload = TransactionIdsPayloadGenerator(
            month=param,
            year=previous_year,
            id=FIRST_ID
        ).model_dump()
        
        payload = TransactionIdsModel(**payload)
        
        assert isinstance(payload, TransactionIdsModel) is True

    @pytest.mark.skipif(current_month_year_skip_condition.month == 12, reason="Reached maximum month")
    def test_month_future_month_in_current_year(self):
        expected = "TIS0005"
        current_datetime = datetime.now()

        payload = TransactionIdsPayloadGenerator(
            month=random.randint(current_datetime.month + 1, 12),
            year=current_datetime.year,
            id=FIRST_ID
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            TransactionIdsModel(**payload)
        assert expected in str(excinfo)

    def test_year_future_year(self):
        expected = "TIS0005"
        current_datetime = datetime.now()

        payload = TransactionIdsPayloadGenerator(
            month=1,
            year=current_datetime.year + 1,
            id=FIRST_ID
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            TransactionIdsModel(**payload)
        assert expected in str(excinfo)

    def test_id_invalid_length(self):
        expected = "TIS0007"

        payload = TransactionIdsPayloadGenerator(
            month=1,
            year=datetime.now().year,
            id=''.join(random.choices(string.digits, k=6))
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            TransactionIdsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", ["ascii_lowercase", "ascii_uppercase", "punctuation"])
    def test_id_invalid_pattern(self, param):
        expected = "TIS0008"

        string_patterns = {
            "ascii_lowercase": string.ascii_lowercase,
            "ascii_uppercase": string.ascii_uppercase,
            "punctuation": string.punctuation
        }

        payload = TransactionIdsPayloadGenerator(
            month=1,
            year=datetime.now().year,
            id=''.join(random.choices(string_patterns[param], k=5))
        ).model_dump()
        
        with pytest.raises(Exception) as excinfo:
            TransactionIdsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1.11, -1.11, True, {'key', 1}, (1, 2), [1, 2], None])
    def test_month_invalid_data_type(self, param):
        expected = "TIS0001"
        payload = TransactionIdsPayloadGenerator(
            month=param,
            year=datetime.now().year - 1,
            id=FIRST_ID
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            TransactionIdsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1.11, -1.11, True, {'key', 1}, (1, 2), [1, 2], None])
    def test_year_invalid_data_type(self, param):
        expected = "TIS0003"
        payload = TransactionIdsPayloadGenerator(
            month=1,
            year=param,
            id=FIRST_ID
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            TransactionIdsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [None, True, 1, 1.1, -1, -1.1, {'key': 1}, (1, 2), [1, 2]])
    def test_id_invalid_data_type(self, param):
        expected = "TIS0006"
        payload = TransactionIdsPayloadGenerator(
            month=1,
            year=datetime.now().year - 1,
            id=param
        ).model_dump()
        
        with pytest.raises(Exception) as excinfo:
            TransactionIdsModel(**payload)
        assert expected in str(excinfo)


        