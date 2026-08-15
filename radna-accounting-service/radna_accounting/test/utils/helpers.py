import pytest
from faker import Faker
import uuid
import string
import random
import copy
from datetime import datetime, timezone
from radna_accounting.validators.chart_of_accounts import (
    account_types
)
from pathlib import Path
BASE_DIR = str(Path(__file__).resolve().parent)

fake = Faker()

@pytest.fixture(scope="function")
def generate_account_request_payload():
    current_datetime = datetime.now()
    input_values = {
        "account_id": ''.join(random.choices(string.digits, k=6)),
        "name": fake.bs(),
        "type": account_types[random.randrange(0, len(account_types))],
        "description": fake.bs(),
        "account_mapping": None,
        "created_date": current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}",
        "updated_date": current_datetime.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(current_datetime.microsecond / 1000):03d}"
    }
    return input_values