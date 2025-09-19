# API Documentation: Update Task

## Endpoint Details
- **Method**: `PUT`
- **URL**: `/api/v1/tasks/{task_id}`
- **Description**: Updates an existing task
- **Authentication**: Required (JWT Bearer Token)
- **Response Model**: `TaskResponse`

## Request

### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | integer | Yes | Task ID |

### Request Body
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "status": "IN_PROGRESS",
  "due_date": "2024-01-20T10:00:00Z"
}
```

### Request Schema
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| title | string | No | 1-255 characters | Task title |
| description | string | No | Maximum 1000 characters | Task description |
| status | string | No | TODO, IN_PROGRESS, COMPLETED | Task status |
| due_date | string | No | ISO 8601 format, future date | Task due date |

### Status Values
- `TODO`: Task is not started
- `IN_PROGRESS`: Task is currently being worked on
- `COMPLETED`: Task is finished

## Response

### Success Response (200 OK)
```json
{
  "id": 1,
  "title": "Updated task title",
  "description": "Updated task description",
  "status": "IN_PROGRESS",
  "due_date": "2024-01-20T10:00:00Z",
  "owner_id": 1,
  "created_at": "2024-01-10T08:00:00Z",
  "updated_at": "2024-01-10T09:00:00Z"
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "detail": "Due date cannot be in the past"
}
```

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

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "String should have at most 255 characters",
      "type": "string_too_long"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error during task update"
}
```

## Example Usage

### cURL Example
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "status": "IN_PROGRESS",
    "due_date": "2024-01-20T10:00:00Z"
  }'
```

### Python Example
```python
import requests
from datetime import datetime, timezone

def update_task(task_id, updates, token):
    url = f"http://localhost:8000/api/v1/tasks/{task_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.put(url, headers=headers, json=updates)
    if response.status_code == 200:
        task = response.json()
        print(f"Task updated successfully!")
        print(f"Title: {task['title']}")
        print(f"Status: {task['status']}")
        return task
    elif response.status_code == 404:
        print("Task not found")
        return None
    else:
        print(f"Error: {response.json()}")
        return None

# Usage - Update task status
updates = {"status": "IN_PROGRESS"}
task = update_task(1, updates, "<your_token>")

# Usage - Update multiple fields
updates = {
    "title": "New task title",
    "description": "Updated description",
    "status": "COMPLETED",
    "due_date": datetime.now(timezone.utc).replace(hour=17, minute=0, second=0, microsecond=0).isoformat()
}
task = update_task(1, updates, "<your_token>")
```

### JavaScript Example
```javascript
const updateTask = async (taskId, updates) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`http://localhost:8000/api/v1/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });
  
  const task = await response.json();
  if (response.ok) {
    console.log('Task updated successfully!');
    console.log('Updated task:', task);
    return task;
  } else if (response.status === 404) {
    console.error('Task not found');
    return null;
  } else {
    console.error('Error updating task:', task);
    return null;
  }
};

// Usage - Update task status
const task = await updateTask(1, { status: 'IN_PROGRESS' });

// Usage - Update multiple fields
const updates = {
  title: 'New task title',
  description: 'Updated description',
  status: 'COMPLETED',
  due_date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
};
const updatedTask = await updateTask(1, updates);
```

## Business Logic

1. **Authentication**: Verifies user is authenticated
2. **Task Lookup**: Finds task by ID
3. **Ownership Check**: Ensures task belongs to authenticated user
4. **Validation**: Validates update data using Pydantic
5. **Update**: Updates task with provided fields
6. **Response**: Returns updated task information

## Security Features

- **User Isolation**: Users can only update their own tasks
- **Ownership Validation**: Verifies task ownership before updating
- **Input Validation**: Comprehensive validation using Pydantic
- **Date Validation**: Prevents setting past due dates
- **SQL Injection Protection**: Uses SQLAlchemy ORM

## Partial Updates

All fields are optional, allowing for partial updates:
- Update only title: `{"title": "New title"}`
- Update only status: `{"status": "COMPLETED"}`
- Update only due date: `{"due_date": "2024-01-20T10:00:00Z"}`
- Update multiple fields: `{"title": "New title", "status": "IN_PROGRESS"}`

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

- `GET /api/v1/tasks/{task_id}` - Get specific task
- `POST /api/v1/tasks/` - Create new task
- `DELETE /api/v1/tasks/{task_id}` - Delete task
- `GET /api/v1/tasks/` - Get all tasks

## Notes

- Only updates fields provided in the request body
- Due date must be in the future
- Task must belong to the authenticated user
- Returns 404 if task doesn't exist or doesn't belong to user
- All timestamps are in UTC timezone
- Supports partial updates (only provided fields are updated)
