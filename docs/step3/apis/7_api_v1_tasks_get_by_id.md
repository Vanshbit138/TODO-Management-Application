# API Documentation: Get Task by ID

## Endpoint Details
- **Method**: `GET`
- **URL**: `/api/v1/tasks/{task_id}`
- **Description**: Retrieves a specific task by its ID
- **Authentication**: Required (JWT Bearer Token)
- **Response Model**: `TaskResponse`

## Request

### Headers
```
Authorization: Bearer <jwt_token>
```

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | integer | Yes | Task ID |

## Response

### Success Response (200 OK)
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation for the project",
  "status": "TODO",
  "due_date": "2024-01-15T10:00:00Z",
  "owner_id": 1,
  "created_at": "2024-01-10T08:00:00Z",
  "updated_at": "2024-01-10T08:00:00Z"
}
```

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
  "detail": "Internal server error during task retrieval"
}
```

## Example Usage

### cURL Example
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer <token>"
```

### Python Example
```python
import requests

def get_task(task_id, token):
    url = f"http://localhost:8000/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        task = response.json()
        print(f"Task: {task['title']}")
        print(f"Status: {task['status']}")
        print(f"Due Date: {task['due_date']}")
        return task
    elif response.status_code == 404:
        print("Task not found")
        return None
    else:
        print(f"Error: {response.json()}")
        return None

# Usage
task = get_task(1, "<your_token>")
```

### JavaScript Example
```javascript
const getTask = async (taskId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`http://localhost:8000/api/v1/tasks/${taskId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const task = await response.json();
  if (response.ok) {
    console.log('Task:', task);
    return task;
  } else if (response.status === 404) {
    console.error('Task not found');
    return null;
  } else {
    console.error('Error:', task);
    return null;
  }
};

// Usage
const task = await getTask(1);
if (task) {
  console.log(`Task: ${task.title} (${task.status})`);
}
```

## Business Logic

1. **Authentication**: Verifies user is authenticated
2. **Task Lookup**: Finds task by ID
3. **Ownership Check**: Ensures task belongs to authenticated user
4. **Response**: Returns task information

## Security Features

- **User Isolation**: Users can only access their own tasks
- **Ownership Validation**: Verifies task ownership before returning
- **SQL Injection Protection**: Uses SQLAlchemy ORM

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique task identifier |
| title | string | Task title |
| description | string | Task description |
| status | string | Task status |
| due_date | string | Task due date in ISO 8601 format |
| owner_id | integer | ID of the user who owns the task |
| created_at | string | Task creation timestamp |
| updated_at | string | Task last update timestamp |

## Related Endpoints

- `GET /api/v1/tasks/` - Get all tasks
- `POST /api/v1/tasks/` - Create new task
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task

## Notes

- Only returns tasks owned by the authenticated user
- Returns 404 if task doesn't exist or doesn't belong to user
- Task ID must be a valid integer
- All timestamps are in UTC timezone
