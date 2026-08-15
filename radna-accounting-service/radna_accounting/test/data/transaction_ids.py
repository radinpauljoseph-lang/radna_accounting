import pytest
import string
import random
from typing import Any
from faker import Faker
from datetime import datetime
from pydantic import BaseModel, model_validator, Field

fake = Faker()

class TransactionIdsPayloadGenerator(BaseModel):
    month: Any = None
    year: Any = None
    id: Any = None