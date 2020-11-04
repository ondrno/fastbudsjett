import json
import mock
import pytest
from app.api import crud


@mock.patch('app.api.crud.post')
def test_create_note(mock_post, test_app):
    test_request_payload = {"title": "foo", "description": "bar"}
    test_response_payload = {"id": 1, "title": "foo", "description": "bar"}
    mock_post.return_value = 1

    response = test_app.post("/notes/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


@mock.patch('app.api.crud.get')
def test_read_note2(mock_get, test_app):
    test_data = {"id": 1, "title": "foo", "description": "bar"}
    mock_get.return_value = test_data

    response = test_app.get("/notes/1")
    assert response.status_code == 200
    assert response.json() == test_data


@mock.patch('app.api.crud.get')
def test_read_note_incorrect_id2(mock_get, test_app):
    mock_get.return_value = None
    response = test_app.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


@mock.patch('app.api.crud.get_all')
def test_read_all_notes(mock_get_all, test_app):
    test_data = [
        {"title": "something", "description": "something else", "id": 1},
        {"title": "someone", "description": "someone else", "id": 2},
    ]
    mock_get_all.return_value = test_data

    response = test_app.get("/notes/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_create_note_invalid_json(test_app):
    response = test_app.post("/notes/", data=json.dumps({"title": "something"}))
    assert response.status_code == 422

