import pytest
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
import random
import configparser
from faker import Faker

faker = Faker()
config = configparser.ConfigParser()
config.read("C:\\radna_accounting\\radna_accounting\\radna_accounting\\configs\\config.ini")

test_url = config['local']['url']

class TestPostAccounts:
    def test_post_accounts(self):
        endpoint = f"{test_url}/accounts"
        payload = {
            "account_id": ''.join(random.choices('0123456789', k=15)),
            "name": faker.name(),
            "type": "ASSET"
        }
        response = requests.post(
            endpoint,
            json=payload
        )
        logging.info(response.json())
        assert response.status_code == 200