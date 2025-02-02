import pytest
from fastapi.testclient import TestClient

def test_websocket_connection(client, test_user_token):
    with client.websocket_connect(
        f"/api/v1/collaboration/ws?token={test_user_token}"
    ) as websocket:
        # Test connection is established
        data = websocket.receive_json()
        assert data["type"] == "connection_established"

def test_websocket_unauthorized(client):
    with pytest.raises(Exception):
        with client.websocket_connect("/api/v1/collaboration/ws") as websocket:
            pass 