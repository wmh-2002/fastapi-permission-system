import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI Permission Management System"}

def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_redoc():
    response = client.get("/redoc")
    assert response.status_code == 200