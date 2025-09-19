# API Documentation: User Login

## Endpoint Details
- **Method**: `POST`
- **URL**: `/api/v1/auth/login`
- **Description**: Authenticates a user and returns JWT access token
- **Authentication**: Not required
- **Response Model**: `TokenResponse`

## Request

### Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

### Request Schema
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| email | string | Yes | Valid email format | User's email address |
| password | string | Yes | Non-empty string | User's password |

## Response

### Success Response (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzA1NjQ4MDAwfQ.example_signature",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "full_name": "John Doe",
    "is_active": true,
    "is_verified": false
  }
}
```

### Error Responses

#### 401 Unauthorized
```json
{
  "detail": "Incorrect email or password"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error during login"
}
```

## Example Usage

### cURL Example
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Python Example
```python
import requests

url = "http://localhost:8000/api/v1/auth/login"
data = {
    "email": "john@example.com",
    "password": "SecurePass123!"
}

response = requests.post(url, json=data)
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    user = token_data['user']
    print(f"Login successful! Token: {access_token}")
    print(f"User: {user['username']}")
else:
    print(f"Login failed: {response.json()}")
```

### JavaScript Example
```javascript
const response = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'SecurePass123!'
  })
});

const tokenData = await response.json();
if (response.ok) {
  const { access_token, user } = tokenData;
  console.log('Login successful!');
  console.log('Token:', access_token);
  console.log('User:', user);
  
  // Store token for future requests
  localStorage.setItem('access_token', access_token);
} else {
  console.error('Login failed:', tokenData);
}
```

## Business Logic

1. **Email Lookup**: Finds user by email address
2. **Password Verification**: Verifies password using bcrypt
3. **User Status Check**: Ensures user is active
4. **Token Generation**: Creates JWT access token with user data
5. **Response**: Returns token and user information

## Security Features

- **Password Hashing**: Uses bcrypt for secure password verification
- **JWT Tokens**: Secure token-based authentication
- **Input Validation**: Email format validation using Pydantic
- **Error Handling**: Generic error messages to prevent user enumeration
- **Token Expiration**: Tokens expire after 30 minutes (configurable)

## Token Information

### JWT Payload
```json
{
  "sub": "1",
  "email": "user@example.com",
  "exp": 1705648000,
  "iat": 1705646200
}
```

### Token Usage
Include the token in the Authorization header for protected endpoints:
```
Authorization: Bearer <access_token>
```

## Related Endpoints

- `POST /api/v1/auth/register` - Register a new user
- `GET /api/v1/auth/me` - Get current user information
- `POST /api/v1/auth/refresh` - Refresh access token

## Notes

- Tokens expire after 30 minutes by default
- Use the refresh endpoint to get new tokens
- Store tokens securely on the client side
- Tokens are stateless and don't require server-side storage
- Invalid credentials return the same error message to prevent user enumeration
