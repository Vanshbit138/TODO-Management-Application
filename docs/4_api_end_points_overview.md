# API Endpoints Overview

## Authentication & User

| Method | Endpoint         | Auth | Body/Params            | Description               |
|--------|------------------|------|------------------------|---------------------------|
| POST   | /api/v1/register | No   | `{ email, password }`  | Register new user         |
| POST   | /api/v1/token    | No   | `{ email, password }`  | Login, get JWT token      |
| GET    | /api/v1/profile  | Yes  | None                   | Get current user profile  |

---

## TODO Management

| Method | Endpoint             | Auth | Body/Params                          | Description        |
|--------|----------------------|------|--------------------------------------|--------------------|
| POST   | /api/v1/tasks/create | Yes  | `{ title, description?, due_date? }` | Create TODO item   |
| GET    | /api/v1/tasks        | Yes  | `page, size, status?, due_date?`     | List user TODOs    |
| GET    | /api/v1/tasks/{id}   | Yes  | None                                 | View single TODO   |
| PUT    | /api/v1/tasks/{id}   | Yes  | `{ title?, description?, status?, due_date? }` | Update TODO item   |
| DELETE | /api/v1/tasks/{id}   | Yes  | None                                 | Delete TODO item   |

---

## Security
- **Authentication:** JWT in `Authorization: Bearer <token>` header  
- **Password Hashing:** bcrypt  
- **Standard Errors:**  
  - `401 Unauthorized` → Missing/invalid token  
  - `403 Forbidden` → No access to resource  
  - `404 Not Found` → Resource not found  
  - `422 Unprocessable Entity` → Validation errors  

---

## Example Requests & Responses

### 1. User Registration
```http 

Request

POST /api/v1/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "Password123"
}

Response (201 Created)

{
  "user_id": 1,
  "message": "User registered successfully"
}

Failure (400 Bad Request)

{
  "error": "Email already registered"
}

2. Login / Token

Request

POST /api/v1/token
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "Password123"
}


Response (200 OK)

{
  "access_token": "jwt-token-here",
  "token_type": "bearer",
  "expires_in": 86400
}


Failure (401 Unauthorized)

{
  "error": "Invalid credentials"
}

3. Create TODO

Request

POST /api/v1/tasks/create
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "due_date": "2025-09-20"
}


Response (201 Created)

{
  "id": 101,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "due_date": "2025-09-20",
  "user_id": 1
}


Failure (422 Unprocessable Entity)

{
  "error": "Title is required"
}

4. Get TODOs

Request

GET /api/v1/tasks?page=1&size=10&status=pending
Authorization: Bearer <jwt-token>


Response (200 OK)

{
  "page": 1,
  "size": 10,
  "total": 2,
  "tasks": [
    {
      "id": 101,
      "title": "Buy groceries",
      "status": "pending"
    },
    {
      "id": 102,
      "title": "Finish project report",
      "status": "in-progress"
    }
  ]
}

5. Update TODO

Request

PUT /api/v1/tasks/101
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "status": "completed"
}


Response (200 OK)

{
  "id": 101,
  "title": "Buy groceries",
  "status": "completed",
  "user_id": 1
}


Failure (404 Not Found)

{
  "error": "Task not found"
}

6. Delete TODO

Request

DELETE /api/v1/tasks/101
Authorization: Bearer <jwt-token>


Response (204 No Content)

(no body)


Failure (403 Forbidden)

{
  "error": "Not authorized to delete this task"
}
