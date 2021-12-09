import datetime
import random
import string
from typing import Dict

from fastapi.testclient import TestClient
from app.core.config import settings


def random_string(length: int = 32, only_lower: bool = False) -> str:
    choices = string.ascii_letters
    if only_lower:
        choices = string.ascii_lowercase
    return "".join(random.choices(choices, k=length))


def random_email() -> str:
    return f"{random_string(only_lower=True)}@{random_string(only_lower=True)}.com"


def random_float(precision: int = 2) -> float:
    return round(random.uniform(0, 1000), precision)


def random_date(want_iso: bool = False) -> str:
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1970, 2020)
    date_str = f"{day}.{month}.{year}"
    if want_iso:
        date_str = datetime.date(year, month, day).isoformat()
    return date_str


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
