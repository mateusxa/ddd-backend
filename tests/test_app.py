from logging import warning
import pytest
from uuid import uuid4
from dotenv import load_dotenv
from main import app
from domain.entites.admin import Admin
from domain.services.admin_service import AdminService


load_dotenv()


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

name = str(uuid4())
email = str(uuid4())
password = str(uuid4())

AdminService.create(AdminService(), admin=Admin(name=name, email=email, password=password))

def get_admin_token(client):
    response = client.post('/admins/token', json={
        "email": email,
        "password": password,
    })
    return response.json['token']


def test_create_admin_token(client):
    response = client.post('/admins/token', json={
        "email": email,
        "password": password
    })
    assert response.status_code == 201
    assert response.json['token']


def test_get_admins(client):
    token = get_admin_token(client)
    assert token
    cursor = None
    while True:
        response = client.get(f"/admins?cursor={cursor}&limit=10", headers={"X-Authorization": token})

        cursor = response.json.get("cursor")
        admins = response.json["admins"]

        assert response.status_code == 200

        if cursor is None:
            break


def test_create_and_get_admins(client):
    token = get_admin_token(client)
    assert token
    name = f"name{str(uuid4())}"
    email = f"email{str(uuid4())}"
    password = f"password{str(uuid4())}"

    response = client.post('/admins', json={
        "name": name,
        "email": email,
        "password": password
    }, headers={"X-Authorization": token})

    admin_id = response.json["id"]
    assert admin_id
    assert name == response.json["name"]
    assert email == response.json["email"]

    response = client.get(f'/admins/{admin_id}', headers={"X-Authorization": token})

    assert admin_id == response.json["id"]
    assert name == response.json["name"]
    assert email == response.json["email"]


def test_create_and_get_admins_fail(client):
    name = f"name{str(uuid4())}"
    email = f"email{str(uuid4())}"
    password = f"password{str(uuid4())}"

    response = client.post('/admins', json={
        "name": name,
        "email": email,
        "password": password
    })

    assert response.status_code == 401
    assert response.json['error'] == 'Missing token'
