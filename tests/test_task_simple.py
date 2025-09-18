"""
Task service unit tests.

This module contains unit tests for the task service and repository
including business logic validation and data access operations.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta
from fastapi import HTTPException

from src.models.task import Task, TaskStatus
from src.repositories.task_repository import TaskRepository
from src.services.task_management.task_service import TaskService


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_task_unit.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def setup_database():
    """Set up test database."""
    from src.core.database import Base
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Create database session for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def task_repository():
    """Create task repository for testing."""
    return TaskRepository()


@pytest.fixture
def task_service(task_repository):
    """Create task service for testing."""
    return TaskService(task_repository)


@pytest.fixture
def sample_user_id():
    """Sample user ID for testing."""
    return 1


class TestTaskRepository:
    """Test task repository functionality."""
    
    def test_create_task(self, db_session, task_repository, sample_user_id):
        """Test task creation."""
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": TaskStatus.TODO,
            "owner_id": sample_user_id
        }
        
        task = task_repository.create_task(db_session, task_data)
        
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.status == TaskStatus.TODO
        assert task.owner_id == sample_user_id
    
    def test_get_task_by_id(self, db_session, task_repository, sample_user_id):
        """Test getting task by ID."""
        # Create a task
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": TaskStatus.TODO,
            "owner_id": sample_user_id
        }
        created_task = task_repository.create_task(db_session, task_data)
        
        # Get task by ID
        task = task_repository.get_task_by_id(db_session, created_task.id, sample_user_id)
        
        assert task is not None
        assert task.id == created_task.id
        assert task.title == "Test Task"
    
    def test_get_task_by_id_wrong_owner(self, db_session, task_repository, sample_user_id):
        """Test getting task by ID with wrong owner."""
        # Create a task
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": TaskStatus.TODO,
            "owner_id": sample_user_id
        }
        created_task = task_repository.create_task(db_session, task_data)
        
        # Try to get task with different owner
        task = task_repository.get_task_by_id(db_session, created_task.id, 999)
        
        assert task is None
    
    def test_get_tasks_by_owner(self, db_session, task_repository, sample_user_id):
        """Test getting tasks by owner."""
        # Create multiple tasks
        for i in range(3):
            task_data = {
                "title": f"Test Task {i}",
                "description": f"Test description {i}",
                "status": TaskStatus.TODO,
                "owner_id": sample_user_id
            }
            task_repository.create_task(db_session, task_data)
        
        # Get tasks by owner
        tasks = task_repository.get_tasks_by_owner(db_session, sample_user_id)
        
        assert len(tasks) == 3
        for i, task in enumerate(tasks):
            assert task.title == f"Test Task {i}"
    
    def test_get_tasks_by_status(self, db_session, task_repository, sample_user_id):
        """Test getting tasks by status."""
        # Create tasks with different statuses
        task_data_todo = {
            "title": "TODO Task",
            "description": "Test description",
            "status": TaskStatus.TODO,
            "owner_id": sample_user_id
        }
        task_data_in_progress = {
            "title": "IN_PROGRESS Task",
            "description": "Test description",
            "status": TaskStatus.IN_PROGRESS,
            "owner_id": sample_user_id
        }
        
        task_repository.create_task(db_session, task_data_todo)
        task_repository.create_task(db_session, task_data_in_progress)
        
        # Get tasks by status
        todo_tasks = task_repository.get_tasks_by_status(db_session, sample_user_id, TaskStatus.TODO)
        in_progress_tasks = task_repository.get_tasks_by_status(db_session, sample_user_id, TaskStatus.IN_PROGRESS)
        
        assert len(todo_tasks) == 1
        assert len(in_progress_tasks) == 1
        assert todo_tasks[0].status == TaskStatus.TODO
        assert in_progress_tasks[0].status == TaskStatus.IN_PROGRESS
    
    def test_update_task(self, db_session, task_repository, sample_user_id):
        """Test task update."""
        # Create a task
        task_data = {
            "title": "Original Title",
            "description": "Original description",
            "status": TaskStatus.TODO,
            "owner_id": sample_user_id
        }
        created_task = task_repository.create_task(db_session, task_data)
        
        # Update task
        update_data = {
            "title": "Updated Title",
            "status": TaskStatus.IN_PROGRESS
        }
        updated_task = task_repository.update_task(db_session, created_task.id, sample_user_id, update_data)
        
        assert updated_task is not None
        assert updated_task.title == "Updated Title"
        assert updated_task.status == TaskStatus.IN_PROGRESS
        assert updated_task.description == "Original description"  # Unchanged
    
    def test_delete_task(self, db_session, task_repository, sample_user_id):
        """Test task deletion."""
        # Create a task
        task_data = {
            "title": "Task to Delete",
            "description": "Test description",
            "status": TaskStatus.TODO,
            "owner_id": sample_user_id
        }
        created_task = task_repository.create_task(db_session, task_data)
        
        # Delete task
        success = task_repository.delete_task(db_session, created_task.id, sample_user_id)
        
        assert success is True
        
        # Verify task is deleted
        task = task_repository.get_task_by_id(db_session, created_task.id, sample_user_id)
        assert task is None
    
    def test_search_tasks(self, db_session, task_repository, sample_user_id):
        """Test task search."""
        # Create tasks with searchable content
        task_data1 = {
            "title": "Important Meeting",
            "description": "Discuss project progress",
            "status": TaskStatus.TODO,
            "owner_id": sample_user_id
        }
        task_data2 = {
            "title": "Regular Task",
            "description": "Important documentation",
            "status": TaskStatus.TODO,
            "owner_id": sample_user_id
        }
        
        task_repository.create_task(db_session, task_data1)
        task_repository.create_task(db_session, task_data2)
        
        # Search for tasks
        results = task_repository.search_tasks(db_session, sample_user_id, "Important")
        
        assert len(results) == 2
        for task in results:
            assert "Important" in task.title or "Important" in task.description


class TestTaskService:
    """Test task service functionality."""
    
    def test_create_task_success(self, db_session, task_service, sample_user_id):
        """Test successful task creation."""
        task = task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="Test Task",
            description="Test description"
        )
        
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.status == TaskStatus.TODO
        assert task.owner_id == sample_user_id
    
    def test_create_task_empty_title(self, db_session, task_service, sample_user_id):
        """Test task creation with empty title."""
        with pytest.raises(HTTPException) as exc_info:
            task_service.create_task(
                db=db_session,
                owner_id=sample_user_id,
                title="",
                description="Test description"
            )
        
        assert exc_info.value.status_code == 400
        assert "Task title is required" in str(exc_info.value.detail)
    
    def test_create_task_title_too_long(self, db_session, task_service, sample_user_id):
        """Test task creation with title too long."""
        long_title = "x" * 256
        
        with pytest.raises(HTTPException) as exc_info:
            task_service.create_task(
                db=db_session,
                owner_id=sample_user_id,
                title=long_title,
                description="Test description"
            )
        
        assert exc_info.value.status_code == 400
        assert "Task title must be less than 255 characters" in str(exc_info.value.detail)
    
    def test_create_task_description_too_long(self, db_session, task_service, sample_user_id):
        """Test task creation with description too long."""
        long_description = "x" * 1001
        
        with pytest.raises(HTTPException) as exc_info:
            task_service.create_task(
                db=db_session,
                owner_id=sample_user_id,
                title="Test Task",
                description=long_description
            )
        
        assert exc_info.value.status_code == 400
        assert "Task description must be less than 1000 characters" in str(exc_info.value.detail)
    
    def test_create_task_past_due_date(self, db_session, task_service, sample_user_id):
        """Test task creation with past due date."""
        past_date = datetime.utcnow() - timedelta(days=1)
        
        with pytest.raises(HTTPException) as exc_info:
            task_service.create_task(
                db=db_session,
                owner_id=sample_user_id,
                title="Test Task",
                description="Test description",
                due_date=past_date
            )
        
        assert exc_info.value.status_code == 400
        assert "Due date cannot be in the past" in str(exc_info.value.detail)
    
    def test_get_task_success(self, db_session, task_service, sample_user_id):
        """Test successful task retrieval."""
        # Create a task
        created_task = task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="Test Task",
            description="Test description"
        )
        
        # Get task
        task = task_service.get_task(db_session, created_task.id, sample_user_id)
        
        assert task.id == created_task.id
        assert task.title == "Test Task"
    
    def test_get_task_not_found(self, db_session, task_service, sample_user_id):
        """Test task retrieval with non-existent ID."""
        with pytest.raises(HTTPException) as exc_info:
            task_service.get_task(db_session, 99999, sample_user_id)
        
        assert exc_info.value.status_code == 404
        assert "Task not found" in str(exc_info.value.detail)
    
    def test_update_task_success(self, db_session, task_service, sample_user_id):
        """Test successful task update."""
        # Create a task
        created_task = task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="Original Title",
            description="Original description"
        )
        
        # Update task
        updated_task = task_service.update_task(
            db=db_session,
            task_id=created_task.id,
            owner_id=sample_user_id,
            title="Updated Title",
            status=TaskStatus.IN_PROGRESS
        )
        
        assert updated_task.title == "Updated Title"
        assert updated_task.status == TaskStatus.IN_PROGRESS
        assert updated_task.description == "Original description"  # Unchanged
    
    def test_update_task_not_found(self, db_session, task_service, sample_user_id):
        """Test task update with non-existent ID."""
        with pytest.raises(HTTPException) as exc_info:
            task_service.update_task(
                db=db_session,
                task_id=99999,
                owner_id=sample_user_id,
                title="Updated Title"
            )
        
        assert exc_info.value.status_code == 404
        assert "Task not found" in str(exc_info.value.detail)
    
    def test_delete_task_success(self, db_session, task_service, sample_user_id):
        """Test successful task deletion."""
        # Create a task
        created_task = task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="Task to Delete",
            description="Test description"
        )
        
        # Delete task
        success = task_service.delete_task(db_session, created_task.id, sample_user_id)
        
        assert success is True
        
        # Verify task is deleted
        with pytest.raises(HTTPException) as exc_info:
            task_service.get_task(db_session, created_task.id, sample_user_id)
        
        assert exc_info.value.status_code == 404
    
    def test_delete_task_not_found(self, db_session, task_service, sample_user_id):
        """Test task deletion with non-existent ID."""
        with pytest.raises(HTTPException) as exc_info:
            task_service.delete_task(db_session, 99999, sample_user_id)
        
        assert exc_info.value.status_code == 404
        assert "Task not found" in str(exc_info.value.detail)
    
    def test_search_tasks_success(self, db_session, task_service, sample_user_id):
        """Test successful task search."""
        # Create tasks with searchable content
        task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="Important Meeting",
            description="Discuss project progress"
        )
        task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="Regular Task",
            description="Important documentation"
        )
        
        # Search for tasks
        results = task_service.search_tasks(db_session, sample_user_id, "Important")
        
        assert len(results) == 2
        for task in results:
            assert "Important" in task.title or "Important" in task.description
    
    def test_search_tasks_empty_term(self, db_session, task_service, sample_user_id):
        """Test task search with empty search term."""
        with pytest.raises(HTTPException) as exc_info:
            task_service.search_tasks(db_session, sample_user_id, "")
        
        assert exc_info.value.status_code == 400
        assert "Search term is required" in str(exc_info.value.detail)
