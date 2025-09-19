# API Documentation: Search Tasks

## Endpoint Details
- **Method**: `POST`
- **URL**: `/api/v1/tasks/search`
- **Description**: Searches tasks by title or description
- **Authentication**: Required (JWT Bearer Token)
- **Response Model**: `TaskListResponse`

## Request

### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Request Body
```json
{
  "search_term": "documentation",
  "skip": 0,
  "limit": 10
}
```

### Request Schema
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| search_term | string | Yes | Minimum 1 character | Search term to match against title or description |
| skip | integer | No | >= 0 | Number of records to skip (default: 0) |
| limit | integer | No | 1-1000 | Maximum number of records to return (default: 100) |

## Response

### Success Response (200 OK)
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write comprehensive API documentation for the project",
      "status": "TODO",
      "due_date": "2024-01-15T10:00:00Z",
      "owner_id": 1,
      "created_at": "2024-01-10T08:00:00Z",
      "updated_at": "2024-01-10T08:00:00Z"
    },
    {
      "id": 3,
      "title": "Update user documentation",
      "description": "Update the user guide with new features",
      "status": "IN_PROGRESS",
      "due_date": "2024-01-18T14:00:00Z",
      "owner_id": 1,
      "created_at": "2024-01-09T10:00:00Z",
      "updated_at": "2024-01-10T09:30:00Z"
    }
  ],
  "total": 2,
  "skip": 0,
  "limit": 10
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
      "loc": ["body", "search_term"],
      "msg": "String should have at least 1 character",
      "type": "string_too_short"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error during task search"
}
```

## Example Usage

### cURL Example
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/search" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "documentation",
    "skip": 0,
    "limit": 10
  }'
```

### Python Example
```python
import requests

def search_tasks(search_term, token, skip=0, limit=10):
    url = "http://localhost:8000/api/v1/tasks/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "search_term": search_term,
        "skip": skip,
        "limit": limit
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        tasks = result['tasks']
        total = result['total']
        print(f"Found {total} tasks matching '{search_term}'")
        for task in tasks:
            print(f"- {task['title']} ({task['status']})")
        return result
    else:
        print(f"Error: {response.json()}")
        return None

# Usage
results = search_tasks("documentation", "<your_token>")
results = search_tasks("meeting", "<your_token>", skip=0, limit=5)
```

### JavaScript Example
```javascript
const searchTasks = async (searchTerm, skip = 0, limit = 10) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/api/v1/tasks/search', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      search_term: searchTerm,
      skip: skip,
      limit: limit
    })
  });
  
  const result = await response.json();
  if (response.ok) {
    console.log(`Found ${result.total} tasks matching '${searchTerm}'`);
    result.tasks.forEach(task => {
      console.log(`- ${task.title} (${task.status})`);
    });
    return result;
  } else {
    console.error('Error searching tasks:', result);
    return null;
  }
};

// Usage
const results = await searchTasks('documentation');
const paginatedResults = await searchTasks('meeting', 0, 5);
```

## Business Logic

1. **Authentication**: Verifies user is authenticated
2. **Search Term Validation**: Ensures search term is not empty
3. **User Filtering**: Only searches tasks owned by authenticated user
4. **Text Matching**: Searches both title and description fields
5. **Pagination**: Supports skip/limit pagination
6. **Response**: Returns matching tasks with metadata

## Search Features

- **Case Insensitive**: Search is case-insensitive
- **Partial Matching**: Matches partial text in title or description
- **Multiple Fields**: Searches both title and description
- **User Isolation**: Only searches user's own tasks
- **Pagination**: Supports pagination for large result sets

## Security Features

- **User Isolation**: Users can only search their own tasks
- **Input Validation**: Search term validation using Pydantic
- **SQL Injection Protection**: Uses SQLAlchemy ORM with parameterized queries

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| tasks | array | List of matching task objects |
| total | integer | Total number of matching tasks |
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
- `GET /api/v1/tasks/{task_id}` - Get specific task
- `POST /api/v1/tasks/` - Create new task
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task

## Notes

- Search is case-insensitive
- Searches both title and description fields
- Only returns tasks owned by the authenticated user
- Empty search term is not allowed
- Supports pagination for large result sets
- Returns empty array if no matches found
