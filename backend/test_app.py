"""
Simple test to verify the backend structure works
"""
import pytest
from fastapi.testclient import TestClient
from main import app


def test_read_main():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Welcome to the Todo API"


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert "status" in response.json()
        assert response.json()["status"] == "healthy"
        assert "timestamp" in response.json()


# Note: Actual task tests would require authentication which is implemented in Phase 2
# These are just basic structural tests