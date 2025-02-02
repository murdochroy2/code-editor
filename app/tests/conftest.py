import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.config import settings
from app.db.base import Base
from app.core.security import create_access_token
from app.db.base import get_db
from app.models.user import User  # Add this import
import os

# Use test database URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace("/prod_db", "/test_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create all database tables before running tests"""
    Base.metadata.drop_all(bind=engine)  # Clear existing tables
    Base.metadata.create_all(bind=engine)  # Create fresh tables
    yield
    Base.metadata.drop_all(bind=engine)  # Clean up after tests

@pytest.fixture
def db():
    """Get database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User"
    }

@pytest.fixture
def test_user_token(test_user):
    # Fix: Pass email as a dict with 'sub' key
    return create_access_token({"sub": test_user["email"]}) 