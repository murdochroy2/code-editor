import pytest
from fastapi import status

def test_user_signup(client, test_user):
    # Modify test data to match the expected schema
    user_data = {
        "email": test_user["email"],
        "username": test_user["email"].split("@")[0],  # Create username from email
        "password": test_user["password"]
    }
    
    response = client.post(
        "/api/v1/auth/register",
        json=user_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user["email"]
    assert "id" in data
    assert "password" not in data

def test_user_login(client, test_user):
    # First create a user
    client.post("/api/v1/auth/signup", json=test_user)
    
    # Try logging in
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_invalid_login(client):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 