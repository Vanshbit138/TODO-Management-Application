"""
Edge cases and error handling tests.

This module contains tests for edge cases, error conditions,
and boundary value testing to ensure robust error handling.
"""

import pytest
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from src.schemas.auth import UserRegistration, UserLogin
from src.schemas.task import TaskCreate, TaskUpdate


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_strings(self, client, sample_user_token, setup_database):
        """Test handling of empty strings."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Test empty title
        task_data = {
            "title": "",
            "description": "Valid description",
            "status": "TODO"
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 422

    def test_very_long_strings(self, client, sample_user_token, setup_database):
        """Test handling of very long strings."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Test very long title (should be handled by Pydantic validation)
        long_title = "A" * 300  # Exceeds max length
        task_data = {
            "title": long_title,
            "description": "Valid description",
            "status": "TODO"
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 422

    def test_special_characters(self, client, sample_user_token, setup_database):
        """Test handling of special characters."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Test special characters in title
        task_data = {
            "title": "Task with special chars: !@#$%^&*()",
            "description": "Description with émojis 🚀 and unicode",
            "status": "TODO"
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]

    def test_unicode_handling(self, client, sample_user_token, setup_database):
        """Test Unicode character handling."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        task_data = {
            "title": "Tâsk with àccénts",
            "description": "中文描述 and русский текст",
            "status": "TODO"
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 201

    def test_boundary_dates(self, client, sample_user_token, setup_database):
        """Test boundary date values."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Test date at exactly now (should be valid)
        now = datetime.now(timezone.utc)
        task_data = {
            "title": "Task due now",
            "description": "Test description",
            "status": "TODO",
            "due_date": now.isoformat()
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 201

    def test_far_future_dates(self, client, sample_user_token, setup_database):
        """Test very far future dates."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Test date far in the future
        far_future = datetime.now(timezone.utc) + timedelta(days=365 * 10)  # 10 years
        task_data = {
            "title": "Far future task",
            "description": "Test description",
            "status": "TODO",
            "due_date": far_future.isoformat()
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 201

    def test_invalid_status_values(self, client, sample_user_token, setup_database):
        """Test invalid status values."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        task_data = {
            "title": "Invalid status task",
            "description": "Test description",
            "status": "INVALID_STATUS"
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 422

    def test_malformed_json(self, client, sample_user_token, setup_database):
        """Test malformed JSON requests."""
        headers = {
            "Authorization": f"Bearer {sample_user_token}",
            "Content-Type": "application/json"
        }
        
        # Send malformed JSON
        malformed_json = '{"title": "Test", "description": "Test", "status": "TODO"'  # Missing closing brace
        response = client.post("/api/v1/tasks/", data=malformed_json, headers=headers)
        assert response.status_code == 422

    def test_missing_required_fields(self, client, sample_user_token, setup_database):
        """Test requests with missing required fields."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Missing title
        task_data = {
            "description": "Test description",
            "status": "TODO"
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 422

    def test_extra_fields(self, client, sample_user_token, setup_database):
        """Test requests with extra fields (should be ignored)."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        task_data = {
            "title": "Task with extra fields",
            "description": "Test description",
            "status": "TODO",
            "extra_field": "This should be ignored",
            "another_extra": 123
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 201
        
        data = response.json()
        assert "extra_field" not in data
        assert "another_extra" not in data

    def test_null_values(self, client, sample_user_token, setup_database):
        """Test handling of null values."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        task_data = {
            "title": "Task with null description",
            "description": None,  # Null description should be allowed
            "status": "TODO"
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 201

    def test_negative_pagination(self, client, sample_user_token, setup_database):
        """Test negative pagination values."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Test negative skip
        response = client.get("/api/v1/tasks/?skip=-1", headers=headers)
        assert response.status_code == 422
        
        # Test negative limit
        response = client.get("/api/v1/tasks/?limit=-1", headers=headers)
        assert response.status_code == 422

    def test_large_pagination(self, client, sample_user_token, setup_database):
        """Test very large pagination values."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Test very large skip
        response = client.get("/api/v1/tasks/?skip=1000000", headers=headers)
        assert response.status_code == 200  # Should return empty results, not error
        
        data = response.json()
        assert len(data["tasks"]) == 0

    def test_invalid_task_id_formats(self, client, sample_user_token, setup_database):
        """Test invalid task ID formats."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Test non-numeric task ID
        response = client.get("/api/v1/tasks/invalid_id", headers=headers)
        assert response.status_code == 422
        
        # Test negative task ID
        response = client.get("/api/v1/tasks/-1", headers=headers)
        assert response.status_code == 422

    def test_concurrent_operations(self, client, sample_user_token, setup_database):
        """Test concurrent operations on the same resource."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create a task
        task_data = {
            "title": "Concurrent test task",
            "description": "Test description",
            "status": "TODO"
        }
        create_response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        task_id = create_response.json()["id"]
        
        # Try to update the same task multiple times
        update_data1 = {"title": "Update 1"}
        update_data2 = {"title": "Update 2"}
        
        response1 = client.put(f"/api/v1/tasks/{task_id}", json=update_data1, headers=headers)
        response2 = client.put(f"/api/v1/tasks/{task_id}", json=update_data2, headers=headers)
        
        # Both should succeed (last one wins)
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_authentication_edge_cases(self, client, setup_database):
        """Test authentication edge cases."""
        # Test malformed authorization header
        headers = {"Authorization": "InvalidFormat token123"}
        response = client.get("/api/v1/tasks/", headers=headers)
        assert response.status_code == 401
        
        # Test empty authorization header
        headers = {"Authorization": ""}
        response = client.get("/api/v1/tasks/", headers=headers)
        assert response.status_code == 401
        
        # Test missing authorization header
        response = client.get("/api/v1/tasks/")
        assert response.status_code == 401

    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options("/api/v1/tasks/")
        assert response.status_code == 200
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers

    def test_content_type_handling(self, client, sample_user_token, setup_database):
        """Test different content types."""
        headers = {
            "Authorization": f"Bearer {sample_user_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        # This should fail because we expect JSON
        response = client.post("/api/v1/tasks/", data="title=Test", headers=headers)
        assert response.status_code == 422

    def test_large_request_body(self, client, sample_user_token, setup_database):
        """Test handling of large request bodies."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        
        # Create a task with very large description
        large_description = "A" * 10000  # 10KB description
        task_data = {
            "title": "Large task",
            "description": large_description,
            "status": "TODO"
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 201
