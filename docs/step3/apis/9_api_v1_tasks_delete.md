# API Documentation: Delete Task

## Endpoint Details
- **Method**: `DELETE`
- **URL**: `/api/v1/tasks/{task_id}`
- **Description**: Deletes a specific task
- **Authentication**: Required (JWT Bearer Token)
- **Response Model**: No Content (204)

## Request

### Headers
```
Authorization: Bearer <jwt_token>
```

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | integer | Yes | Task ID |

### Request Body
None

## Response

### Success Response (204 No Content)
No response body.

### Error Responses

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

#### 404 Not Found
```json
{
  "detail": "Task not found"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error during task deletion"
}
```

## Example Usage

### cURL Example
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer <token>"
```

### Python Example
```python
import requests

def delete_task(task_id, token):
    url = f"http://localhost:8000/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("Task deleted successfully!")
        return True
    elif response.status_code == 404:
        print("Task not found")
        return False
    else:
        print(f"Error: {response.json()}")
        return False

# Usage
success = delete_task(1, "<your_token>")
if success:
    print("Task has been removed")
```

### JavaScript Example
```javascript
const deleteTask = async (taskId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`http://localhost:8000/api/v1/tasks/${taskId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.ok) {
    console.log('Task deleted successfully!');
    return true;
  } else if (response.status === 404) {
    console.error('Task not found');
    return false;
  } else {
    const error = await response.json();
    console.error('Error deleting task:', error);
    return false;
  }
};

// Usage
const success = await deleteTask(1);
if (success) {
  console.log('Task has been removed from the list');
}
```

## Business Logic

1. **Authentication**: Verifies user is authenticated
2. **Task Lookup**: Finds task by ID
3. **Ownership Check**: Ensures task belongs to authenticated user
4. **Deletion**: Permanently deletes the task from database
5. **Response**: Returns 204 No Content on success

## Security Features

- **User Isolation**: Users can only delete their own tasks
- **Ownership Validation**: Verifies task ownership before deletion
- **SQL Injection Protection**: Uses SQLAlchemy ORM
- **Cascade Deletion**: Task is permanently removed from database

## Related Endpoints

- `GET /api/v1/tasks/{task_id}` - Get specific task
- `POST /api/v1/tasks/` - Create new task
- `PUT /api/v1/tasks/{task_id}` - Update task
- `GET /api/v1/tasks/` - Get all tasks

## Notes

- Task is permanently deleted from the database
- Only tasks owned by the authenticated user can be deleted
- Returns 404 if task doesn't exist or doesn't belong to user
- No response body on successful deletion (204 status)
- Task ID must be a valid integer
- Deletion cannot be undone
