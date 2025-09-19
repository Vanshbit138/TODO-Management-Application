# API Documentation: Get Current User

## Endpoint Details
- **Method**: `GET`
- **URL**: `/api/v1/auth/me`
- **Description**: Retrieves information about the currently authenticated user
- **Authentication**: Required (JWT Bearer Token)
- **Response Model**: `UserResponse`

## Request

### Headers
```
Authorization: Bearer <jwt_token>
```

### Path Parameters
None

### Query Parameters
None

## Response

### Success Response (200 OK)
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false
}
```

### Error Responses

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

#### 403 Forbidden
```json
{
  "detail": "Inactive user"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Example Usage

### cURL Example
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Python Example
```python
import requests

url = "http://localhost:8000/api/v1/auth/me"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    user = response.json()
    print(f"Current user: {user['username']} ({user['email']})")
else:
    print(f"Error: {response.json()}")
```

### JavaScript Example
```javascript
const token = localStorage.getItem('access_token');

const response = await fetch('http://localhost:8000/api/v1/auth/me', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const user = await response.json();
if (response.ok) {
  console.log('Current user:', user);
  console.log(`Welcome, ${user.full_name || user.username}!`);
} else {
  console.error('Error:', user);
  // Handle token expiration
  if (response.status === 401) {
    localStorage.removeItem('access_token');
    // Redirect to login
  }
}
```

## Business Logic

1. **Token Validation**: Validates JWT token signature and expiration
2. **User Lookup**: Retrieves user information from database
3. **Status Check**: Verifies user is active
4. **Response**: Returns user information without sensitive data

## Security Features

- **JWT Validation**: Verifies token signature and expiration
- **User Status Check**: Ensures user is active
- **Data Filtering**: Returns only safe user information
- **Token Expiration**: Handles expired tokens gracefully

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique user identifier |
| email | string | User's email address |
| username | string | User's username |
| full_name | string | User's full name (optional) |
| is_active | boolean | Whether user account is active |
| is_verified | boolean | Whether user email is verified |

## Related Endpoints

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get token
- `POST /api/v1/auth/refresh` - Refresh access token

## Notes

- Requires valid JWT token in Authorization header
- Returns user information without password or sensitive data
- Useful for checking authentication status
- Can be used to get user context in frontend applications
- Token must not be expired
