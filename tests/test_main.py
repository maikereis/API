# async bug: "ValueError: set_wakeup_fd only works in main thread"
import pytest

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def get_token():
    response = client.post(
        "/token",
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            "grant_type": "",
            "username": 'johndoe',
            "password": "secret",
            "scope": "",
            "client_id": "",
            "client_secret": ""
        }
    )
    assert response.status_code == 200
    return response.json()['access_token']


def test_request_new_token():
    response = client.post(
        "/token",
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            "grant_type": "",
            "username": 'johndoe',
            "password": "secret",
            "scope": "",
            "client_id": "",
            "client_secret": ""
        }
    )
    assert response.status_code == 200


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"CashBack API": "Hello World!"}


def test_read_users_me(get_token):
    response = client.get(
        "/users/me/",
        headers={
            'accept': 'application/json',
            'Authorization': f"Bearer {get_token}",
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "full_name": "John Doe",
        "disabled": False
    }


def test_read_own_items(get_token):
    response = client.get(
        "/users/me/items",
        headers={
            'accept': 'application/json',
            'Authorization': f"Bearer {get_token}",
        }
    )
    assert response.status_code == 200
    assert response.json() == [{
        "item_id": "Foo",
        "owner": "johndoe"
    }]
