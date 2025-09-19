# API Documentation: Get Tasks by Due Date

## Endpoint Details
- **Method**: `GET`
- **URL**: `/api/v1/tasks/due/list`
- **Description**: Retrieves tasks ordered by due date for the authenticated user
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
      "id": 1,
      "title": "Task due soon",
      "description": "This task is due soon",
      "status": "TODO",
      "due_date": "2024-01-15T10:00:00Z",
      "owner_id": 1,
      "created_at": "2024-01-10T08:00:00Z",
      "updated_at": "2024-01-10T08:00:00Z"
    },
    {
      "id": 2,
      "title": "Task due later",
      "description": "This task is due later",
      "status": "IN_PROGRESS",
      "due_date": "2024-01-20T14:00:00Z",
      "owner_id": 1,
      "created_at": "2024-01-09T10:00:00Z",
      "updated_at": "2024-01-10T09:30:00Z"
    },
    {
      "id": 3,
      "title": "Task without due date",
      "description": "This task has no due date",
      "status": "TODO",
      "due_date": null,
      "owner_id": 1,
      "created_at": "2024-01-08T10:00:00Z",
      "updated_at": "2024-01-08T10:00:00Z"
    }
  ],
  "total": 3,
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
  "detail": "Internal server error during tasks retrieval"
}
```

## Example Usage

### cURL Example
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/due/list" \
  -H "Authorization: Bearer <token>"
```

### Python Example
```python
import requests

def get_tasks_by_due_date(token, skip=0, limit=100):
    url = "http://localhost:8000/api/v1/tasks/due/list"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"skip": skip, "limit": limit}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        tasks = result['tasks']
        total = result['total']
        print(f"Found {total} tasks ordered by due date")
        for task in tasks:
            due_date = task['due_date'] or 'No due date'
            print(f"- {task['title']} (Due: {due_date})")
        return result
    else:
        print(f"Error: {response.json()}")
        return None

# Usage
tasks_by_due = get_tasks_by_due_date("<your_token>")
tasks_by_due = get_tasks_by_due_date("<your_token>", skip=0, limit=10)
```

### JavaScript Example
```javascript
const getTasksByDueDate = async (skip = 0, limit = 100) => {
  const token = localStorage.getItem('access_token');
  
  const params = new URLSearchParams({
    skip: skip.toString(),
    limit: limit.toString()
  });
  
  const response = await fetch(`http://localhost:8000/api/v1/tasks/due/list?${params}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const result = await response.json();
  if (response.ok) {
    console.log(`Found ${result.total} tasks ordered by due date`);
    result.tasks.forEach(task => {
      const dueDate = task.due_date || 'No due date';
      console.log(`- ${task.title} (Due: ${dueDate})`);
    });
    return result;
  } else {
    console.error('Error getting tasks by due date:', result);
    return null;
  }
};

// Usage
const tasksByDue = await getTasksByDueDate();
const paginatedTasks = await getTasksByDueDate(0, 10);
```

## Business Logic

1. **Authentication**: Verifies user is authenticated
2. **User Filtering**: Only returns tasks owned by authenticated user
3. **Due Date Ordering**: Orders tasks by due_date (ascending)
4. **Null Handling**: Tasks without due_date are placed at the end
5. **Pagination**: Supports skip/limit pagination
6. **Response**: Returns tasks ordered by due date with metadata

## Ordering Logic

Tasks are ordered as follows:
1. Tasks with due_date (ascending order - earliest first)
2. Tasks without due_date (null values last)

## Security Features

- **User Isolation**: Users can only see their own tasks
- **Input Validation**: Query parameters are validated
- **SQL Injection Protection**: Uses SQLAlchemy ORM

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| tasks | array | List of task objects ordered by due date |
| total | integer | Total number of tasks |
| skip | integer | Number of records skipped |
| limit | integer | Maximum number of records returned |

### Task Object Fields
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique task identifier |
| title | string | Task title |
| description | string | Task description |
| status | string | Task status |
| due_date | string | Task due date in ISO 8601 format (null if not set) |
| owner_id | integer | ID of the user who owns the task |
| created_at | string | Task creation timestamp |
| updated_at | string | Task last update timestamp |

## Related Endpoints

- `GET /api/v1/tasks/` - Get all tasks
- `GET /api/v1/tasks/overdue/list` - Get overdue tasks
- `GET /api/v1/tasks/{task_id}` - Get specific task
- `PUT /api/v1/tasks/{task_id}` - Update task

## Notes

- Tasks are ordered by due_date (earliest first)
- Tasks without due_date appear at the end
- Only returns tasks owned by the authenticated user
- Supports pagination for large result sets
- Useful for calendar views and deadline management
- Returns empty array if no tasks found
