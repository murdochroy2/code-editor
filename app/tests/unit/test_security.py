import pytest
from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash
)

def test_password_hash():
    password = "test123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)

def test_create_access_token():
    email = "test@example.com"
    # Create a dictionary with the email as the 'sub' claim
    data = {"sub": email}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0 