import random
import string
import datetime
from typing import Dict

from fastapi.testclient import TestClient
from app.core.config import settings


def random_lower_string(max_chars: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=max_chars))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_float(precision: int = 2) -> float:
    return round(random.uniform(-1000, +1000), precision)


def random_date() -> str:
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1970, 2020)
    return datetime.date(year, month, day).isoformat()


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
