# API Documentation: Get Tasks

## Endpoint Details
- **Method**: `GET`
- **URL**: `/api/v1/tasks/`
- **Description**: Retrieves tasks for the authenticated user with optional filtering and pagination
- **Authentication**: Required (JWT Bearer Token)
- **Response Model**: `TaskListResponse`

## Request

### Headers
```
Authorization: Bearer <jwt_token>
```

### Query Parameters
| Parameter | Type | Required | Default | Validation | Description |
|-----------|------|----------|---------|------------|-------------|
| skip | integer | No | 0 | >= 0 | Number of records to skip |
| limit | integer | No | 100 | 1-1000 | Maximum number of records to return |
| status | string | No | null | TODO, IN_PROGRESS, COMPLETED | Filter by task status |

### Status Values
- `TODO`: Task is not started
- `IN_PROGRESS`: Task is currently being worked on
- `COMPLETED`: Task is finished

## Response

### Success Response (200 OK)
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write comprehensive API documentation",
      "status": "TODO",
      "due_date": "2024-01-15T10:00:00Z",
      "owner_id": 1,
      "created_at": "2024-01-10T08:00:00Z",
      "updated_at": "2024-01-10T08:00:00Z"
    },
    {
      "id": 2,
      "title": "Review code changes",
      "description": "Review pull request #123",
      "status": "IN_PROGRESS",
      "due_date": "2024-01-12T14:00:00Z",
      "owner_id": 1,
      "created_at": "2024-01-09T10:00:00Z",
      "updated_at": "2024-01-10T09:30:00Z"
    }
  ],
  "total": 2,
  "skip": 0,
  "limit": 100
}
```

### Error Responses

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
      "loc": ["query", "limit"],
      "msg": "Input should be less than or equal to 1000",
      "type": "less_than_equal"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error during task retrieval"
}
```

## Example Usage

### cURL Examples

#### Get all tasks
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer <token>"
```

#### Get tasks with pagination
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?skip=0&limit=10" \
  -H "Authorization: Bearer <token>"
```

#### Get tasks by status
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?status=TODO" \
  -H "Authorization: Bearer <token>"
```

#### Get completed tasks with pagination
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?status=COMPLETED&skip=0&limit=5" \
  -H "Authorization: Bearer <token>"
```

### Python Example
```python
import requests

url = "http://localhost:8000/api/v1/tasks/"
headers = {"Authorization": "Bearer <token>"}

# Get all tasks
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    tasks = data['tasks']
    total = data['total']
    print(f"Found {total} tasks")
    for task in tasks:
        print(f"- {task['title']} ({task['status']})")
else:
    print(f"Error: {response.json()}")

# Get TODO tasks with pagination
params = {"status": "TODO", "skip": 0, "limit": 5}
response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    print(f"TODO tasks: {len(data['tasks'])}")
```

### JavaScript Example
```javascript
const token = localStorage.getItem('access_token');

// Get all tasks
const response = await fetch('http://localhost:8000/api/v1/tasks/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const data = await response.json();
if (response.ok) {
  console.log(`Found ${data.total} tasks`);
  data.tasks.forEach(task => {
    console.log(`- ${task.title} (${task.status})`);
  });
} else {
  console.error('Error:', data);
}

// Get tasks by status with pagination
const getTasksByStatus = async (status, page = 0, limit = 10) => {
  const params = new URLSearchParams({
    status: status,
    skip: page * limit,
    limit: limit
  });
  
  const response = await fetch(`http://localhost:8000/api/v1/tasks/?${params}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
};

// Usage
const todoTasks = await getTasksByStatus('TODO', 0, 5);
console.log('TODO tasks:', todoTasks);
```

## Business Logic

1. **Authentication**: Verifies user is authenticated
2. **User Filtering**: Only returns tasks owned by the authenticated user
3. **Status Filtering**: Optional filtering by task status
4. **Pagination**: Supports skip/limit pagination
5. **Total Count**: Includes total count for pagination metadata

## Security Features

- **User Isolation**: Users can only see their own tasks
- **Input Validation**: Query parameters are validated
- **SQL Injection Protection**: Uses SQLAlchemy ORM

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| tasks | array | List of task objects |
| total | integer | Total number of tasks (for pagination) |
| skip | integer | Number of records skipped |
| limit | integer | Maximum number of records returned |

### Task Object Fields
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

## Pagination

- **Default Limit**: 100 records
- **Maximum Limit**: 1000 records
- **Skip Parameter**: Number of records to skip
- **Total Count**: Included in response for pagination UI

## Related Endpoints

- `POST /api/v1/tasks/` - Create new task
- `GET /api/v1/tasks/{task_id}` - Get specific task
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task
- `POST /api/v1/tasks/search` - Search tasks

## Notes

- Only returns tasks owned by the authenticated user
- Supports filtering by status
- Includes pagination metadata
- Tasks are returned in creation order (newest first)
- Empty result returns empty tasks array with total=0
