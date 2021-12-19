from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.category import create_random_category
from app.tests.utils.utils import random_string


BASE_URL = f"{settings.API_V1_STR}/categories/"


def _generate_valid_data(test_itemtype) -> dict:
    return {"title_en": random_string(length=25), "itemtype_id": test_itemtype.id}


def _assert_error(response, code: int, detail: str) -> None:
    assert response.status_code == code
    content = response.json()
    assert detail in content["detail"]


def test_create_category(client: TestClient, test_itemtype, superuser_token_headers: dict, db: Session) -> None:
    data = _generate_valid_data(test_itemtype)

    response = client.post(BASE_URL, headers=superuser_token_headers, json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["title_en"] == data["title_en"]
    assert "id" in content


def test_create_category_with_existing_name_returns_422(client: TestClient,
                                                        test_itemtype,
                                                        superuser_token_headers: dict,
                                                        db: Session) -> None:
    data = _generate_valid_data(test_itemtype)
    response = client.post(BASE_URL, headers=superuser_token_headers, json=data)
    assert response.status_code == 200

    response = client.post(BASE_URL, headers=superuser_token_headers, json=data)
    assert response.status_code == 422
    content = response.json()
    assert "Database integrity error" in content["message"]


def test_create_category_with_too_short_name_returns_422(client: TestClient, superuser_token_headers: dict,
                                                         db: Session) -> None:
    data = {"title_en": random_string(length=1)}
    response = client.post(BASE_URL, headers=superuser_token_headers, json=data)
    assert response.status_code == 422
    content = response.json()
    assert "at least 3 characters" in content["detail"][0]["msg"]


def test_create_category_with_too_long_name_returns_422(client: TestClient, superuser_token_headers: dict,
                                                        db: Session) -> None:
    data = {"title_en": random_string(length=31)}
    response = client.post(BASE_URL, headers=superuser_token_headers, json=data)
    assert response.status_code == 422
    content = response.json()
    assert "at most 30 characters" in content["detail"][0]["msg"]


def test_read_category(client: TestClient, test_itemtype, superuser_token_headers: dict, db: Session) -> None:
    category = create_random_category(db, test_itemtype)
    response = client.get(BASE_URL + f"{category.id}", headers=superuser_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["title_en"] == category.title_en
    assert content["id"] == category.id


def test_update_category(client: TestClient, test_itemtype, superuser_token_headers: dict, db: Session) -> None:
    category = create_random_category(db, test_itemtype)

    update_data = {"title_en": random_string(length=25)}
    response = client.put(BASE_URL + f"{category.id}", headers=superuser_token_headers, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["title_en"] == update_data["title_en"]


def test_update_category_with_same_name(client: TestClient, test_itemtype,
                                        superuser_token_headers: dict, db: Session) -> None:
    category = create_random_category(db, test_itemtype)

    update_data = {"title_en": category.title_en}
    response = client.put(BASE_URL + f"{category.id}", headers=superuser_token_headers, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["title_en"] == update_data["title_en"]


def test_update_category_with_too_short_name_returns_422(client: TestClient, test_itemtype,
                                                         superuser_token_headers: dict,
                                                         db: Session) -> None:
    category = create_random_category(db, test_itemtype)

    update_data = {"title_en": random_string(length=2)}
    response = client.put(BASE_URL + f"{category.id}", headers=superuser_token_headers, json=update_data)
    assert response.status_code == 422
    content = response.json()
    assert "at least 3 characters" in content["detail"][0]["msg"]


def test_update_category_with_invalid_id_returns_404(client: TestClient, test_itemtype,
                                                     superuser_token_headers: dict,
                                                     db: Session) -> None:
    data = {"title_en": random_string(length=25), "itemtype_id": test_itemtype.id}
    response = client.put(BASE_URL + "-1", headers=superuser_token_headers, json=data)
    assert response.status_code == 404
    content = response.json()
    assert "Category not found" in content['detail']


def test_remove_category_as_superuser_returns_200(client: TestClient, test_itemtype,
                                                  superuser_token_headers: dict, db: Session) -> None:
    category = create_random_category(db, test_itemtype)

    response = client.delete(BASE_URL + f"{category.id}", headers=superuser_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["title_en"] == category.title_en
    assert content["id"] == category.id
    assert content["itemtype_id"] == test_itemtype.id


def test_remove_category_as_normal_user_returns_400(client: TestClient, test_itemtype,
                                                    normal_user_token_headers: dict, db: Session) -> None:
    category = create_random_category(db, test_itemtype)

    response = client.delete(BASE_URL + f"{category.id}", headers=normal_user_token_headers)
    _assert_error(response, 400, "Not enough permissions")


def test_remove_category_with_invalid_id_returns_404(client: TestClient, superuser_token_headers: dict,
                                                     db: Session) -> None:
    response = client.delete(BASE_URL + "-1", headers=superuser_token_headers)
    assert response.status_code == 404
    content = response.json()
    assert "Category not found" in content['detail']
