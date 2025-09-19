# API Documentation: Create Task

## Endpoint Details
- **Method**: `POST`
- **URL**: `/api/v1/tasks/`
- **Description**: Creates a new task for the authenticated user
- **Authentication**: Required (JWT Bearer Token)
- **Response Model**: `TaskResponse`

## Request

### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Request Body
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation for the project",
  "status": "TODO",
  "due_date": "2024-01-15T10:00:00Z"
}
```

### Request Schema
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| title | string | Yes | 1-255 characters | Task title |
| description | string | No | Maximum 1000 characters | Task description |
| status | string | No | TODO, IN_PROGRESS, COMPLETED | Task status (default: TODO) |
| due_date | string | No | ISO 8601 format, future date | Task due date |

### Status Values
- `TODO`: Task is not started (default)
- `IN_PROGRESS`: Task is currently being worked on
- `COMPLETED`: Task is finished

## Response

### Success Response (201 Created)
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

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "String should have at most 255 characters",
      "type": "string_too_long"
    },
    {
      "loc": ["body", "due_date"],
      "msg": "Due date cannot be in the past",
      "type": "value_error"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error during task creation"
}
```

## Example Usage

### cURL Example
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "status": "TODO",
    "due_date": "2024-01-15T10:00:00Z"
  }'
```

### Python Example
```python
import requests
from datetime import datetime, timezone

url = "http://localhost:8000/api/v1/tasks/"
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

# Create task with due date
due_date = datetime.now(timezone.utc).replace(hour=17, minute=0, second=0, microsecond=0)
due_date = due_date.replace(day=due_date.day + 1)  # Tomorrow at 5 PM

data = {
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation for the project",
    "status": "TODO",
    "due_date": due_date.isoformat()
}

response = requests.post(url, headers=headers, json=data)
if response.status_code == 201:
    task = response.json()
    print(f"Task created successfully!")
    print(f"Task ID: {task['id']}")
    print(f"Title: {task['title']}")
    print(f"Due Date: {task['due_date']}")
else:
    print(f"Error creating task: {response.json()}")
```

### JavaScript Example
```javascript
const token = localStorage.getItem('access_token');

const taskData = {
  title: 'Complete project documentation',
  description: 'Write comprehensive API documentation for the project',
  status: 'TODO',
  due_date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // Tomorrow
};

const response = await fetch('http://localhost:8000/api/v1/tasks/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(taskData)
});

const task = await response.json();
if (response.ok) {
  console.log('Task created successfully!');
  console.log('Task:', task);
} else {
  console.error('Error creating task:', task);
}
```

## Business Logic

1. **Authentication**: Verifies user is authenticated
2. **Validation**: Validates task data using Pydantic
3. **Due Date Check**: Ensures due date is in the future
4. **Task Creation**: Creates task with owner_id set to current user
5. **Response**: Returns created task information

## Security Features

- **User Isolation**: Tasks are automatically assigned to authenticated user
- **Input Validation**: Comprehensive validation using Pydantic
- **Date Validation**: Prevents creation of tasks with past due dates
- **SQL Injection Protection**: Uses SQLAlchemy ORM

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique task identifier |
| title | string | Task title |
| description | string | Task description (optional) |
| status | string | Task status |
| due_date | string | Task due date in ISO 8601 format (optional) |
| owner_id | integer | ID of the user who owns the task |
| created_at | string | Task creation timestamp |
| updated_at | string | Task last update timestamp |

## Related Endpoints

- `GET /api/v1/tasks/` - Get all tasks
- `GET /api/v1/tasks/{task_id}` - Get specific task
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task

## Notes

- Task is automatically assigned to the authenticated user
- Due date must be in the future
- Description is optional
- Status defaults to "TODO" if not provided
- All timestamps are in UTC timezone
- Task ID is auto-generated
