from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.main import app
from app.tests.utils.category import create_random_category
from app.tests.utils.payment import create_random_payment
from app.tests.utils.itemtype import create_random_itemtype
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="session")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )


@pytest.fixture(scope="session")
def test_itemtype(db):
    yield create_random_itemtype(db=db)


@pytest.fixture(scope="session")
def test_payment(db):
    yield create_random_payment(db=db)


@pytest.fixture(scope="session")
def test_category(db, test_itemtype):
    yield create_random_category(db=db, itemtype=test_itemtype)


