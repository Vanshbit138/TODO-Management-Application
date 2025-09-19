"""
Comprehensive API endpoint tests with full coverage.

This module contains integration tests for all API endpoints
including authentication, task management, and error handling.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone


class TestTaskEndpoints:
    """Test task management API endpoints."""

    def test_create_task_success(self, client, sample_user_token, setup_database):
        """Test successful task creation via API."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        task_data = {
            "title": "API Test Task",
            "description": "Test task created via API",
            "status": "TODO"
        }
        
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert "id" in data
        assert "created_at" in data

    def test_create_task_unauthorized(self, client, setup_database):
        """Test task creation without authentication."""
        task_data = {
            "title": "Unauthorized Task",
            "description": "This should fail",
            "status": "TODO"
        }
        
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 401

    def test_create_task_invalid_data(self, client, sample_user_token, setup_database):
        """Test task creation with invalid data."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        task_data = {
            "title": "",  # Empty title should fail
            "description": "Test description",
            "status": "TODO"
        }
        
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 422

    def test_create_task_past_due_date(self, client, sample_user_token, setup_database):
        """Test task creation with past due date."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        past_due_date = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        task_data = {
            "title": "Past Due Task",
            "description": "This should fail",
            "status": "TODO",
            "due_date": past_due_date
        }
        
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 400

    def test_get_tasks_success(self, client, sample_user_token, setup_database):
        """Test getting tasks via API."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create a task first
        task_data = {
            "title": "Get Tasks Test",
            "description": "Test description",
            "status": "TODO"
        }
        client.post("/api/v1/tasks/", json=task_data, headers=headers)
        
        # Get tasks
        response = client.get("/api/v1/tasks/", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert len(data["tasks"]) >= 1

    def test_get_tasks_with_pagination(self, client, sample_user_token, setup_database):
        """Test getting tasks with pagination."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create multiple tasks
        for i in range(5):
            task_data = {
                "title": f"Pagination Test {i}",
                "description": f"Test description {i}",
                "status": "TODO"
            }
            client.post("/api/v1/tasks/", json=task_data, headers=headers)
        
        # Test pagination
        response = client.get("/api/v1/tasks/?skip=0&limit=3", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["tasks"]) == 3

    def test_get_tasks_by_status(self, client, sample_user_token, setup_database):
        """Test getting tasks by status."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create tasks with different statuses
        task_data_todo = {
            "title": "TODO Task",
            "description": "Test description",
            "status": "TODO"
        }
        task_data_in_progress = {
            "title": "In Progress Task",
            "description": "Test description",
            "status": "IN_PROGRESS"
        }
        
        client.post("/api/v1/tasks/", json=task_data_todo, headers=headers)
        client.post("/api/v1/tasks/", json=task_data_in_progress, headers=headers)
        
        # Get TODO tasks only
        response = client.get("/api/v1/tasks/?status=TODO", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert all(task["status"] == "TODO" for task in data["tasks"])

    def test_get_task_by_id_success(self, client, sample_user_token, setup_database):
        """Test getting specific task by ID."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create a task
        task_data = {
            "title": "Get by ID Test",
            "description": "Test description",
            "status": "TODO"
        }
        create_response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        task_id = create_response.json()["id"]
        
        # Get the task by ID
        response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == task_data["title"]

    def test_get_task_by_id_not_found(self, client, sample_user_token, setup_database):
        """Test getting non-existent task by ID."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        response = client.get("/api/v1/tasks/99999", headers=headers)
        assert response.status_code == 404

    def test_update_task_success(self, client, sample_user_token, setup_database):
        """Test successful task update."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create a task
        task_data = {
            "title": "Original Title",
            "description": "Original description",
            "status": "TODO"
        }
        create_response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        task_id = create_response.json()["id"]
        
        # Update the task
        update_data = {
            "title": "Updated Title",
            "status": "IN_PROGRESS"
        }
        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "IN_PROGRESS"

    def test_update_task_partial(self, client, sample_user_token, setup_database):
        """Test partial task update."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create a task
        task_data = {
            "title": "Original Title",
            "description": "Original description",
            "status": "TODO"
        }
        create_response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        task_id = create_response.json()["id"]
        
        # Update only the title
        update_data = {"title": "Updated Title Only"}
        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Updated Title Only"
        assert data["description"] == "Original description"  # Should remain unchanged

    def test_update_task_not_found(self, client, sample_user_token, setup_database):
        """Test updating non-existent task."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        update_data = {"title": "Updated Title"}
        response = client.put("/api/v1/tasks/99999", json=update_data, headers=headers)
        assert response.status_code == 404

    def test_delete_task_success(self, client, sample_user_token, setup_database):
        """Test successful task deletion."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create a task
        task_data = {
            "title": "Task to Delete",
            "description": "Test description",
            "status": "TODO"
        }
        create_response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        task_id = create_response.json()["id"]
        
        # Delete the task
        response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
        assert response.status_code == 200
        
        # Verify task is deleted
        get_response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client, sample_user_token, setup_database):
        """Test deleting non-existent task."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        response = client.delete("/api/v1/tasks/99999", headers=headers)
        assert response.status_code == 404

    def test_search_tasks_success(self, client, sample_user_token, setup_database):
        """Test task search functionality."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create tasks with searchable content
        task_data1 = {
            "title": "Important Meeting",
            "description": "Discuss project progress",
            "status": "TODO"
        }
        task_data2 = {
            "title": "Regular Task",
            "description": "Some other task",
            "status": "TODO"
        }
        
        client.post("/api/v1/tasks/", json=task_data1, headers=headers)
        client.post("/api/v1/tasks/", json=task_data2, headers=headers)
        
        # Search by title
        response = client.get("/api/v1/tasks/search?q=Important", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["tasks"]) == 1
        assert "Important" in data["tasks"][0]["title"]

    def test_search_tasks_empty_term(self, client, sample_user_token, setup_database):
        """Test task search with empty search term."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        response = client.get("/api/v1/tasks/search?q=", headers=headers)
        assert response.status_code == 400

    def test_get_overdue_tasks(self, client, sample_user_token, setup_database):
        """Test getting overdue tasks."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create an overdue task
        past_due_date = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        task_data = {
            "title": "Overdue Task",
            "description": "This task is overdue",
            "status": "TODO",
            "due_date": past_due_date
        }
        client.post("/api/v1/tasks/", json=task_data, headers=headers)
        
        # Get overdue tasks
        response = client.get("/api/v1/tasks/overdue", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "Overdue Task"

    def test_get_tasks_by_due_date(self, client, sample_user_token, setup_database):
        """Test getting tasks by due date."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create tasks with different due dates
        today = datetime.now(timezone.utc).isoformat()
        tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        
        task_data1 = {
            "title": "Today Task",
            "description": "Due today",
            "status": "TODO",
            "due_date": today
        }
        task_data2 = {
            "title": "Tomorrow Task",
            "description": "Due tomorrow",
            "status": "TODO",
            "due_date": tomorrow
        }
        
        client.post("/api/v1/tasks/", json=task_data1, headers=headers)
        client.post("/api/v1/tasks/", json=task_data2, headers=headers)
        
        # Get tasks by due date
        response = client.get("/api/v1/tasks/by-due-date", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["tasks"]) == 2


class TestHealthEndpoints:
    """Test health and utility endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
