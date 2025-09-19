"""
Task endpoints integration tests.

This module contains comprehensive integration tests for task management endpoints
including CRUD operations, search, filtering, and error handling.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta

from src.api.main import app
from src.core.database import get_db, Base
from src.models.user import User
from src.models.task import Task, TaskStatus
from src.repositories.user_repository import UserRepository
from src.repositories.task_repository import TaskRepository
from src.services.authentication.password_service import password_service


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tasks.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def setup_database():
    """Set up test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Create database session for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db_session):
    """Create test user."""
    user_repo = UserRepository()
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": password_service.hash_password("TestPassword123!"),
        "full_name": "Test User",
        "is_active": True,
        "is_verified": False
    }
    user = user_repo.create_user(db_session, user_data)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers."""
    login_data = {
        "email": "test@example.com",
        "password": "TestPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat()
    }


class TestTaskCreation:
    """Test task creation functionality."""
    
    def test_create_task_success(self, client, auth_headers, sample_task_data):
        """Test successful task creation."""
        response = client.post("/api/v1/tasks/", json=sample_task_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["description"] == sample_task_data["description"]
        assert data["status"] == TaskStatus.TODO
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_task_without_auth(self, client, sample_task_data):
        """Test task creation without authentication."""
        response = client.post("/api/v1/tasks/", json=sample_task_data)
        
        assert response.status_code == 403
        assert "Not authenticated" in response.json()["detail"]
    
    def test_create_task_empty_title(self, client, auth_headers):
        """Test task creation with empty title."""
        task_data = {"title": "", "description": "Test description"}
        response = client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_task_past_due_date(self, client, auth_headers):
        """Test task creation with past due date."""
        past_date = (datetime.utcnow() - timedelta(days=1)).isoformat()
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "due_date": past_date
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        
        assert response.status_code == 422  # Validation error


class TestTaskRetrieval:
    """Test task retrieval functionality."""
    
    def test_get_tasks_success(self, client, auth_headers, sample_task_data):
        """Test successful task retrieval."""
        # Create a task first
        client.post("/api/v1/tasks/", json=sample_task_data, headers=auth_headers)
        
        # Get tasks
        response = client.get("/api/v1/tasks/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data
        assert len(data["tasks"]) >= 1
    
    def test_get_tasks_with_pagination(self, client, auth_headers, sample_task_data):
        """Test task retrieval with pagination."""
        # Create multiple tasks
        for i in range(5):
            task_data = {**sample_task_data, "title": f"Task {i}"}
            client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        
        # Get tasks with pagination
        response = client.get("/api/v1/tasks/?skip=2&limit=2", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 2
        assert data["skip"] == 2
        assert data["limit"] == 2
    
    def test_get_tasks_by_status(self, client, auth_headers, sample_task_data):
        """Test task retrieval filtered by status."""
        # Create a task
        client.post("/api/v1/tasks/", json=sample_task_data, headers=auth_headers)
        
        # Get tasks by status
        response = client.get("/api/v1/tasks/?status=TODO", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) >= 1
        for task in data["tasks"]:
            assert task["status"] == TaskStatus.TODO
    
    def test_get_task_by_id_success(self, client, auth_headers, sample_task_data):
        """Test successful task retrieval by ID."""
        # Create a task
        create_response = client.post("/api/v1/tasks/", json=sample_task_data, headers=auth_headers)
        task_id = create_response.json()["id"]
        
        # Get task by ID
        response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == sample_task_data["title"]
    
    def test_get_task_by_id_not_found(self, client, auth_headers):
        """Test task retrieval by non-existent ID."""
        response = client.get("/api/v1/tasks/99999", headers=auth_headers)
        
        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]
    
    def test_get_tasks_without_auth(self, client):
        """Test task retrieval without authentication."""
        response = client.get("/api/v1/tasks/")
        
        assert response.status_code == 403
        assert "Not authenticated" in response.json()["detail"]


class TestTaskUpdate:
    """Test task update functionality."""
    
    def test_update_task_success(self, client, auth_headers, sample_task_data):
        """Test successful task update."""
        # Create a task
        create_response = client.post("/api/v1/tasks/", json=sample_task_data, headers=auth_headers)
        task_id = create_response.json()["id"]
        
        # Update task
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated description",
            "status": TaskStatus.IN_PROGRESS
        }
        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["status"] == update_data["status"]
    
    def test_update_task_partial(self, client, auth_headers, sample_task_data):
        """Test partial task update."""
        # Create a task
        create_response = client.post("/api/v1/tasks/", json=sample_task_data, headers=auth_headers)
        task_id = create_response.json()["id"]
        
        # Update only title
        update_data = {"title": "Only Title Updated"}
        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == sample_task_data["description"]  # Unchanged
    
    def test_update_task_not_found(self, client, auth_headers):
        """Test task update with non-existent ID."""
        update_data = {"title": "Updated Title"}
        response = client.put("/api/v1/tasks/99999", json=update_data, headers=auth_headers)
        
        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]
    
    def test_update_task_without_auth(self, client, sample_task_data):
        """Test task update without authentication."""
        update_data = {"title": "Updated Title"}
        response = client.put("/api/v1/tasks/1", json=update_data)
        
        assert response.status_code == 403
        assert "Not authenticated" in response.json()["detail"]


class TestTaskDeletion:
    """Test task deletion functionality."""
    
    def test_delete_task_success(self, client, auth_headers, sample_task_data):
        """Test successful task deletion."""
        # Create a task
        create_response = client.post("/api/v1/tasks/", json=sample_task_data, headers=auth_headers)
        task_id = create_response.json()["id"]
        
        # Delete task
        response = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        
        assert response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_task_not_found(self, client, auth_headers):
        """Test task deletion with non-existent ID."""
        response = client.delete("/api/v1/tasks/99999", headers=auth_headers)
        
        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]
    
    def test_delete_task_without_auth(self, client):
        """Test task deletion without authentication."""
        response = client.delete("/api/v1/tasks/1")
        
        assert response.status_code == 403
        assert "Not authenticated" in response.json()["detail"]


class TestTaskSearch:
    """Test task search functionality."""
    
    def test_search_tasks_success(self, client, auth_headers, sample_task_data):
        """Test successful task search."""
        # Create a task with specific title
        task_data = {**sample_task_data, "title": "Important Meeting"}
        client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        
        # Search for tasks
        search_data = {"search_term": "Important"}
        response = client.post("/api/v1/tasks/search", json=search_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) >= 1
        assert "Important" in data["tasks"][0]["title"]
    
    def test_search_tasks_empty_term(self, client, auth_headers):
        """Test task search with empty search term."""
        search_data = {"search_term": ""}
        response = client.post("/api/v1/tasks/search", json=search_data, headers=auth_headers)
        
        assert response.status_code == 422  # Validation error
    
    def test_search_tasks_without_auth(self, client):
        """Test task search without authentication."""
        search_data = {"search_term": "test"}
        response = client.post("/api/v1/tasks/search", json=search_data)
        
        assert response.status_code == 403
        assert "Not authenticated" in response.json()["detail"]


class TestTaskSpecialEndpoints:
    """Test special task endpoints."""
    
    def test_get_overdue_tasks(self, client, auth_headers):
        """Test getting overdue tasks."""
        # Create a task with past due date
        past_date = (datetime.utcnow() - timedelta(days=1)).isoformat()
        task_data = {
            "title": "Overdue Task",
            "description": "This task is overdue",
            "due_date": past_date
        }
        client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        
        # Get overdue tasks
        response = client.get("/api/v1/tasks/overdue/list", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) >= 1
    
    def test_get_tasks_by_due_date(self, client, auth_headers, sample_task_data):
        """Test getting tasks ordered by due date."""
        # Create multiple tasks with different due dates
        for i in range(3):
            due_date = (datetime.utcnow() + timedelta(days=i+1)).isoformat()
            task_data = {**sample_task_data, "title": f"Task {i}", "due_date": due_date}
            client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        
        # Get tasks by due date
        response = client.get("/api/v1/tasks/due/list", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) >= 3
        
        # Verify they are ordered by due date
        due_dates = [task["due_date"] for task in data["tasks"] if task["due_date"]]
        assert due_dates == sorted(due_dates)
