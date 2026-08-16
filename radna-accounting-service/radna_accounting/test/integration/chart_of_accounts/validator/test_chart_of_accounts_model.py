import pytest
import string
import random
from radna_accounting.validators.chart_of_accounts import ChartOfAccountsModel
from radna_accounting.test.data.chart_of_accounts import ChartOfAccountsPayloadGenerator
from radna_accounting.models.chart_of_accounts import coa_meta

class TestChartOfAccountsModel:

    def test_happy_path(self):
        payload = ChartOfAccountsPayloadGenerator().model_dump()

        payload = ChartOfAccountsModel(**payload)

        assert isinstance(payload, ChartOfAccountsModel) is True

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_account_id_invalid_data_type(self, param):
        expected = "COA0001"
        payload = ChartOfAccountsPayloadGenerator(
            account_id=param
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)
    
    def test_account_id_invalid_min_length(self):
        expected = "COA0002"
        payload = ChartOfAccountsPayloadGenerator(
            account_id=''.join(random.choices(string.digits, k=coa_meta.ACCOUNT_ID_MIN_LENGTH - 1))
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)

    def test_account_id_invalid_max_length(self):
        expected = "COA0003"
        payload = ChartOfAccountsPayloadGenerator(
            account_id=''.join(random.choices(string.digits, k=coa_meta.ACCOUNT_ID_LENGTH + 1))
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_account_name_invalid_data_type(self, param):
        expected = "COA0004"
        payload = ChartOfAccountsPayloadGenerator(
            name=param
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)
    
    def test_account_name_invalid_max_length(self):
        expected = "COA0005"
        payload = ChartOfAccountsPayloadGenerator(
            name=''.join(random.choices(string.digits, k=coa_meta.NAME_LENGTH + 1))
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)

    def test_account_name_invalid_min_length(self):
        expected = "COA0006"
        payload = ChartOfAccountsPayloadGenerator(
            name=""
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}, None])
    def test_account_type_invalid_data_type(self, param):
        expected = "COA0007"
        payload = ChartOfAccountsPayloadGenerator(
            type=param
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", ["", "SAMPLE", "DISBURSEMENT", "asset", "liability"])
    def test_account_type_invalid_types(self, param):
        expected = "COA0008"
        payload = ChartOfAccountsPayloadGenerator(
            type=param
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)

    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}])
    def test_account_description_invalid_data_type(self, param):
        expected = "COA0009"
        payload = ChartOfAccountsPayloadGenerator(
            description=param
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)

    def test_account_description_invalid_max_length(self):
        expected = "COA0010"
        payload = ChartOfAccountsPayloadGenerator(
            description=''.join(random.choices(string.digits, k=coa_meta.DESCRIPTION_LENGTH + 1))
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)


    @pytest.mark.parametrize("param", [1, -1, 1.11, -1.11, True, {'key', 1}, {'key': 1}])
    def test_account_mapping_invalid_data_type(self, param):
        expected = "COA0011"
        payload = ChartOfAccountsPayloadGenerator(
            account_mapping=param
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)

    def test_account_mapping_invalid_max_length(self):
        expected = "COA0012"
        payload = ChartOfAccountsPayloadGenerator(
            account_mapping=''.join(random.choices(string.digits, k=coa_meta.ACCOUNT_ID_LENGTH + 1))
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)

    def test_account_mapping_equal_to_account_id(self):
        expected = "COA0013"
        account_id = ChartOfAccountsPayloadGenerator().model_dump()[coa_meta.ACCOUNT_ID]
        payload = ChartOfAccountsPayloadGenerator(
            account_id=account_id,
            account_mapping=account_id
        ).model_dump()

        with pytest.raises(Exception) as excinfo:
            ChartOfAccountsModel(**payload)
        assert expected in str(excinfo)



