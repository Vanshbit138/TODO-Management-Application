"""
Improved Task management tests with comprehensive coverage.

This module contains comprehensive tests for the task management system
including CRUD operations, business logic, and edge cases.
"""

import pytest
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from src.models.task import Task, TaskStatus
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse


class TestTaskRepository:
    """Test task repository functionality."""

    def test_create_task(self, db_session, task_repository, sample_user_id, setup_database):
        """Test task creation."""
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "TODO",
            "owner_id": sample_user_id
        }
        
        task = task_repository.create_task(db_session, task_data)
        
        assert task.id is not None
        assert task.title == task_data["title"]
        assert task.description == task_data["description"]
        assert task.status == TaskStatus.TODO
        assert task.owner_id == sample_user_id

    def test_get_task_by_id(self, db_session, task_repository, sample_user_id, setup_database):
        """Test getting task by ID."""
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "TODO",
            "owner_id": sample_user_id
        }
        
        created_task = task_repository.create_task(db_session, task_data)
        retrieved_task = task_repository.get_task_by_id(db_session, created_task.id, sample_user_id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == task_data["title"]

    def test_get_task_by_id_wrong_owner(self, db_session, task_repository, sample_user_id, setup_database):
        """Test getting task by ID with wrong owner."""
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "TODO",
            "owner_id": sample_user_id
        }
        
        created_task = task_repository.create_task(db_session, task_data)
        retrieved_task = task_repository.get_task_by_id(db_session, created_task.id, 99999)
        
        assert retrieved_task is None

    def test_get_tasks_by_owner(self, db_session, task_repository, sample_user_id, setup_database):
        """Test getting tasks by owner."""
        # Create multiple tasks
        for i in range(3):
            task_data = {
                "title": f"Test Task {i}",
                "description": f"Test description {i}",
                "status": "TODO",
                "owner_id": sample_user_id
            }
            task_repository.create_task(db_session, task_data)
        
        tasks = task_repository.get_tasks_by_owner(db_session, sample_user_id)
        assert len(tasks) == 3

    def test_get_tasks_by_status(self, db_session, task_repository, sample_user_id, setup_database):
        """Test getting tasks by status."""
        # Create tasks with different statuses
        task_data_todo = {
            "title": "TODO Task",
            "description": "Test description",
            "status": "TODO",
            "owner_id": sample_user_id
        }
        task_data_in_progress = {
            "title": "In Progress Task",
            "description": "Test description",
            "status": "IN_PROGRESS",
            "owner_id": sample_user_id
        }
        
        task_repository.create_task(db_session, task_data_todo)
        task_repository.create_task(db_session, task_data_in_progress)
        
        todo_tasks = task_repository.get_tasks_by_status(db_session, sample_user_id, "TODO")
        assert len(todo_tasks) == 1
        assert todo_tasks[0].status == TaskStatus.TODO

    def test_update_task(self, db_session, task_repository, sample_user_id, setup_database):
        """Test task update."""
        task_data = {
            "title": "Original Title",
            "description": "Original description",
            "status": "TODO",
            "owner_id": sample_user_id
        }
        
        created_task = task_repository.create_task(db_session, task_data)
        
        update_data = {
            "title": "Updated Title",
            "status": "IN_PROGRESS"
        }
        
        updated_task = task_repository.update_task(db_session, created_task.id, sample_user_id, update_data)
        
        assert updated_task.title == "Updated Title"
        assert updated_task.status == TaskStatus.IN_PROGRESS
        assert updated_task.description == "Original description"  # Should remain unchanged

    def test_delete_task(self, db_session, task_repository, sample_user_id, setup_database):
        """Test task deletion."""
        task_data = {
            "title": "Task to Delete",
            "description": "Test description",
            "status": "TODO",
            "owner_id": sample_user_id
        }
        
        created_task = task_repository.create_task(db_session, task_data)
        task_id = created_task.id
        
        success = task_repository.delete_task(db_session, task_id, sample_user_id)
        assert success is True
        
        # Verify task is deleted
        deleted_task = task_repository.get_task_by_id(db_session, task_id, sample_user_id)
        assert deleted_task is None

    def test_search_tasks(self, db_session, task_repository, sample_user_id, setup_database):
        """Test task search functionality."""
        # Create tasks with searchable content
        task_data1 = {
            "title": "Important Meeting",
            "description": "Discuss project progress",
            "status": "TODO",
            "owner_id": sample_user_id
        }
        task_data2 = {
            "title": "Regular Task",
            "description": "Some other task",
            "status": "TODO",
            "owner_id": sample_user_id
        }
        
        task_repository.create_task(db_session, task_data1)
        task_repository.create_task(db_session, task_data2)
        
        # Search by title
        search_results = task_repository.search_tasks(db_session, sample_user_id, "Important")
        assert len(search_results) == 1
        assert search_results[0].title == "Important Meeting"
        
        # Search by description
        search_results = task_repository.search_tasks(db_session, sample_user_id, "project")
        assert len(search_results) == 1
        assert "project" in search_results[0].description.lower()


class TestTaskService:
    """Test task service functionality."""

    def test_create_task_success(self, db_session, task_service, sample_user_id, setup_database):
        """Test successful task creation."""
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "TODO"
        }
        
        task = task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            **task_data
        )
        
        assert task.id is not None
        assert task.title == task_data["title"]
        assert task.description == task_data["description"]
        assert task.status == TaskStatus.TODO
        assert task.owner_id == sample_user_id

    def test_create_task_with_due_date(self, db_session, task_service, sample_user_id, setup_database):
        """Test task creation with due date."""
        due_date = datetime.now(timezone.utc) + timedelta(days=7)
        task_data = {
            "title": "Task with Due Date",
            "description": "Test description",
            "status": "TODO",
            "due_date": due_date
        }
        
        task = task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            **task_data
        )
        
        assert task.due_date is not None
        assert task.due_date.date() == due_date.date()

    def test_create_task_past_due_date(self, db_session, task_service, sample_user_id, setup_database):
        """Test task creation with past due date."""
        past_due_date = datetime.now(timezone.utc) - timedelta(days=1)
        task_data = {
            "title": "Task with Past Due Date",
            "description": "Test description",
            "status": "TODO",
            "due_date": past_due_date
        }
        
        with pytest.raises(HTTPException) as exc_info:
            task_service.create_task(
                db=db_session,
                owner_id=sample_user_id,
                **task_data
            )
        
        assert exc_info.value.status_code == 400
        assert "Due date cannot be in the past" in str(exc_info.value.detail)

    def test_get_task_success(self, db_session, task_service, sample_user_id, setup_database):
        """Test successful task retrieval."""
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "TODO"
        }
        
        created_task = task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            **task_data
        )
        
        retrieved_task = task_service.get_task(db_session, created_task.id, sample_user_id)
        
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == task_data["title"]

    def test_get_task_not_found(self, db_session, task_service, sample_user_id, setup_database):
        """Test task retrieval with non-existent ID."""
        with pytest.raises(HTTPException) as exc_info:
            task_service.get_task(db_session, 99999, sample_user_id)
        
        assert exc_info.value.status_code == 404
        assert "Task not found" in str(exc_info.value.detail)

    def test_get_task_wrong_owner(self, db_session, task_service, sample_user_id, setup_database):
        """Test task retrieval with wrong owner."""
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "TODO"
        }
        
        created_task = task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            **task_data
        )
        
        with pytest.raises(HTTPException) as exc_info:
            task_service.get_task(db_session, created_task.id, 99999)
        
        assert exc_info.value.status_code == 404

    def test_update_task_success(self, db_session, task_service, sample_user_id, setup_database):
        """Test successful task update."""
        task_data = {
            "title": "Original Title",
            "description": "Original description",
            "status": "TODO"
        }
        
        created_task = task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            **task_data
        )
        
        update_data = {
            "title": "Updated Title",
            "status": "IN_PROGRESS"
        }
        
        updated_task = task_service.update_task(
            db=db_session,
            task_id=created_task.id,
            owner_id=sample_user_id,
            **update_data
        )
        
        assert updated_task.title == "Updated Title"
        assert updated_task.status == TaskStatus.IN_PROGRESS

    def test_update_task_not_found(self, db_session, task_service, sample_user_id, setup_database):
        """Test task update with non-existent ID."""
        update_data = {
            "title": "Updated Title"
        }
        
        with pytest.raises(HTTPException) as exc_info:
            task_service.update_task(
                db=db_session,
                task_id=99999,
                owner_id=sample_user_id,
                **update_data
            )
        
        assert exc_info.value.status_code == 404

    def test_delete_task_success(self, db_session, task_service, sample_user_id, setup_database):
        """Test successful task deletion."""
        task_data = {
            "title": "Task to Delete",
            "description": "Test description",
            "status": "TODO"
        }
        
        created_task = task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            **task_data
        )
        
        success = task_service.delete_task(db_session, created_task.id, sample_user_id)
        assert success is True

    def test_delete_task_not_found(self, db_session, task_service, sample_user_id, setup_database):
        """Test task deletion with non-existent ID."""
        with pytest.raises(HTTPException) as exc_info:
            task_service.delete_task(db_session, 99999, sample_user_id)
        
        assert exc_info.value.status_code == 404

    def test_search_tasks_success(self, db_session, task_service, sample_user_id, setup_database):
        """Test successful task search."""
        # Create tasks with searchable content
        task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="Important Meeting",
            description="Discuss project progress",
            status="TODO"
        )
        
        task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="Regular Task",
            description="Some other task",
            status="TODO"
        )
        
        # Search by title
        search_results = task_service.search_tasks(db_session, sample_user_id, "Important")
        assert len(search_results) == 1
        assert "Important" in search_results[0].title

    def test_get_tasks_with_pagination(self, db_session, task_service, sample_user_id, setup_database):
        """Test getting tasks with pagination."""
        # Create multiple tasks
        for i in range(5):
            task_service.create_task(
                db=db_session,
                owner_id=sample_user_id,
                title=f"Task {i}",
                description=f"Description {i}",
                status="TODO"
            )
        
        # Test pagination
        tasks = task_service.get_tasks(db_session, sample_user_id, skip=0, limit=3)
        assert len(tasks) == 3
        
        tasks = task_service.get_tasks(db_session, sample_user_id, skip=3, limit=3)
        assert len(tasks) == 2

    def test_get_tasks_by_status(self, db_session, task_service, sample_user_id, setup_database):
        """Test getting tasks by status."""
        # Create tasks with different statuses
        task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="TODO Task",
            status="TODO"
        )
        
        task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="In Progress Task",
            status="IN_PROGRESS"
        )
        
        todo_tasks = task_service.get_tasks(db_session, sample_user_id, status="TODO")
        assert len(todo_tasks) == 1
        assert todo_tasks[0].status == TaskStatus.TODO

    def test_get_overdue_tasks(self, db_session, task_service, sample_user_id, setup_database):
        """Test getting overdue tasks."""
        # Create an overdue task
        past_due_date = datetime.now(timezone.utc) - timedelta(days=1)
        task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="Overdue Task",
            status="TODO",
            due_date=past_due_date
        )
        
        # Create a future task
        future_due_date = datetime.now(timezone.utc) + timedelta(days=1)
        task_service.create_task(
            db=db_session,
            owner_id=sample_user_id,
            title="Future Task",
            status="TODO",
            due_date=future_due_date
        )
        
        overdue_tasks = task_service.get_overdue_tasks(db_session, sample_user_id)
        assert len(overdue_tasks) == 1
        assert overdue_tasks[0].title == "Overdue Task"
