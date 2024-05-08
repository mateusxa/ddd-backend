from logging import warning
import pytest
from uuid import uuid4
from dotenv import load_dotenv
from app import app
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


def test_create_and_get_admins(client):
    token = get_admin_token(client)
    assert token

    admin_id = "hdjskahdjsak"

    response = client.get(f'/admins/{admin_id}', headers={"X-Authorization": token})

    print(response.json)

