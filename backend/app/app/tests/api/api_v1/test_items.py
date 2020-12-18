import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item


def test_create_item(client: TestClient, superuser_token_headers: dict, db: Session,
                     test_itemtype, test_payment, test_category) -> None:
    data = {"description": "this_is_a_long_text", "amount": 9.95, "date": "01.01.2020",
            "itemtype_id": test_itemtype.id, "payment_id": test_payment.id, "category_id": test_category.id}
    response = client.post(
        f"{settings.API_V1_STR}/items/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["description"] == data["description"]
    assert content["amount"] == data["amount"]
    assert "id" in content


@pytest.mark.parametrize("wrong_date", ["01-01-2020", "1-12-2020"])
def test_create_item_wrong_date_returns_422(
        client: TestClient, superuser_token_headers: dict,
        db: Session, test_payment, test_category, wrong_date
) -> None:
    data = {"description": "this_is_a_long_text", "amount": 9.95, "date": wrong_date,
            "payment_id": test_payment.id, "category_id": test_category.id}
    response = client.post(
        f"{settings.API_V1_STR}/items/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 422
    content = response.json()['detail'][0]
    assert "Wrong date format" in str(content["msg"])


def test_read_item(
        client: TestClient, superuser_token_headers: dict, db: Session,
        test_itemtype, test_category, test_payment
) -> None:
    item = create_random_item(db, test_itemtype.id, test_category.id, test_payment.id)
    response = client.get(
        f"{settings.API_V1_STR}/items/{item.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["description"] == item.description
    assert content["amount"] == item.amount
    assert content["category_id"] == test_category.id
    assert content["payment_id"] == test_payment.id
    assert content["id"] == item.id
    assert content["owner_id"] == item.owner_id


def test_remove_item_with_invalid_id_returns_404(client: TestClient, superuser_token_headers: dict,
                                                 db: Session) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/items/-1", headers=superuser_token_headers,
    )
    assert r.status_code == 404
    content = r.json()
    assert "Item not found" in content['detail']
