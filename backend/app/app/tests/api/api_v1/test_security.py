import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


@pytest.mark.parametrize("path", ["categories", "items", "payments", "users"])
def test_get_without_token_returns_401(client: TestClient, db: Session, path) -> None:
    response = client.get(f"{settings.API_V1_STR}/{path}/")
    assert response.status_code == 401
    content = response.json()
    assert content["detail"] == "Not authenticated"
