# API Documentation: Get Overdue Tasks

## Endpoint Details
- **Method**: `GET`
- **URL**: `/api/v1/tasks/overdue/list`
- **Description**: Retrieves overdue tasks for the authenticated user
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

## Response

### Success Response (200 OK)
```json
{
  "tasks": [
    {
      "id": 2,
      "title": "Overdue task",
      "description": "This task is overdue",
      "status": "TODO",
      "due_date": "2024-01-05T10:00:00Z",
      "owner_id": 1,
      "created_at": "2024-01-01T08:00:00Z",
      "updated_at": "2024-01-01T08:00:00Z"
    },
    {
      "id": 5,
      "title": "Another overdue task",
      "description": "This task is also overdue",
      "status": "IN_PROGRESS",
      "due_date": "2024-01-08T14:00:00Z",
      "owner_id": 1,
      "created_at": "2024-01-02T10:00:00Z",
      "updated_at": "2024-01-03T09:30:00Z"
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
  "detail": "Internal server error during overdue tasks retrieval"
}
```

## Example Usage

### cURL Example
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/overdue/list" \
  -H "Authorization: Bearer <token>"
```

### Python Example
```python
import requests

def get_overdue_tasks(token, skip=0, limit=100):
    url = "http://localhost:8000/api/v1/tasks/overdue/list"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"skip": skip, "limit": limit}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        tasks = result['tasks']
        total = result['total']
        print(f"Found {total} overdue tasks")
        for task in tasks:
            print(f"- {task['title']} (Due: {task['due_date']})")
        return result
    else:
        print(f"Error: {response.json()}")
        return None

# Usage
overdue_tasks = get_overdue_tasks("<your_token>")
overdue_tasks = get_overdue_tasks("<your_token>", skip=0, limit=10)
```

### JavaScript Example
```javascript
const getOverdueTasks = async (skip = 0, limit = 100) => {
  const token = localStorage.getItem('access_token');
  
  const params = new URLSearchParams({
    skip: skip.toString(),
    limit: limit.toString()
  });
  
  const response = await fetch(`http://localhost:8000/api/v1/tasks/overdue/list?${params}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const result = await response.json();
  if (response.ok) {
    console.log(`Found ${result.total} overdue tasks`);
    result.tasks.forEach(task => {
      console.log(`- ${task.title} (Due: ${task.due_date})`);
    });
    return result;
  } else {
    console.error('Error getting overdue tasks:', result);
    return null;
  }
};

// Usage
const overdueTasks = await getOverdueTasks();
const paginatedOverdue = await getOverdueTasks(0, 10);
```

## Business Logic

1. **Authentication**: Verifies user is authenticated
2. **User Filtering**: Only returns tasks owned by authenticated user
3. **Overdue Filtering**: Filters tasks where due_date < current_time
4. **Status Filtering**: Only includes tasks that are not COMPLETED
5. **Pagination**: Supports skip/limit pagination
6. **Response**: Returns overdue tasks with metadata

## Overdue Criteria

A task is considered overdue if:
- It has a due_date set
- The due_date is in the past (before current time)
- The task status is not COMPLETED

## Security Features

- **User Isolation**: Users can only see their own overdue tasks
- **Input Validation**: Query parameters are validated
- **SQL Injection Protection**: Uses SQLAlchemy ORM

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| tasks | array | List of overdue task objects |
| total | integer | Total number of overdue tasks |
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

## Related Endpoints

- `GET /api/v1/tasks/` - Get all tasks
- `GET /api/v1/tasks/due/list` - Get tasks ordered by due date
- `GET /api/v1/tasks/{task_id}` - Get specific task
- `PUT /api/v1/tasks/{task_id}` - Update task

## Notes

- Only returns tasks with due_date in the past
- Excludes completed tasks from overdue list
- Only returns tasks owned by the authenticated user
- Supports pagination for large result sets
- Returns empty array if no overdue tasks found
- Useful for dashboard widgets and notifications
