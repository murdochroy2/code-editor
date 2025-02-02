import pytest
from fastapi import status

def test_create_collaboration_session(client, test_user_token):
    response = client.post(
        "/api/v1/collaboration/sessions",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={
            "file_name": "test.py",
            "language": "python"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "session_id" in data
    assert data["file_name"] == "test.py"

def test_join_session_unauthorized(client):
    response = client.post(
        "/api/v1/collaboration/sessions/123/join",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_join_session(client, test_user_token):
    # First create a session
    create_response = client.post(
        "/api/v1/collaboration/sessions",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={
            "file_name": "test.py",
            "language": "python"
        }
    )
    session_id = create_response.json()["session_id"]
    
    # Try joining the session
    response = client.post(
        f"/api/v1/collaboration/sessions/{session_id}/join",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK 