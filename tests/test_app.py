import pytest
import requests
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_missing_token(client):
    response = client.get('/protected')
    assert response.status_code == 401
    assert response.json['error'] == 'Missing token'

def test_invalid_token(client):
    response = client.get('/protected', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid token'

def test_expired_token(client):
    expired_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIxQGV4YW1wbGUuY29tIiwiaWF0IjoxNjE3MzA2MjY1LCJleHAiOjE2MTczMDYyNjd9.rjGw0m_SycHL-Tn9Tbq7YORPUi7hXmGhxlEV_CSlC_Y'
    response = client.get('/protected', headers={'Authorization': f'Bearer {expired_token}'})
    assert response.status_code == 401
    assert response.json['error'] == 'Token expired'

def test_valid_token(client):
    valid_token = 'valid_token'  # Replace with your valid token
    response = client.get('/protected', headers={'Authorization': f'Bearer {valid_token}'})
    assert response.status_code == 200
    assert 'message' in response.json
