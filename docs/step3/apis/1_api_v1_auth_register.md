# API Documentation: User Registration

## Endpoint Details
- **Method**: `POST`
- **URL**: `/api/v1/auth/register`
- **Description**: Creates a new user account with email validation and password hashing
- **Authentication**: Not required
- **Response Model**: `UserResponse`

## Request

### Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

### Request Schema
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| email | string | Yes | Valid email format | User's email address |
| username | string | Yes | 3-50 characters, alphanumeric only | Unique username |
| password | string | Yes | 8-128 characters, mixed case, numbers, special characters | User password |
| full_name | string | No | Maximum 255 characters | User's full name |

### Password Requirements
- Minimum 8 characters
- Maximum 128 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character from: `!@#$%^&*()_+-=[]{}|;:,.<>?`

## Response

### Success Response (201 Created)
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

#### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "Password must contain at least one uppercase letter",
      "type": "value_error"
    },
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
  "detail": "Internal server error during user registration"
}
```

## Example Usage

### cURL Example
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

### Python Example
```python
import requests

url = "http://localhost:8000/api/v1/auth/register"
data = {
    "email": "john@example.com",
    "username": "johndoe",
    "password": "SecurePass123!",
    "full_name": "John Doe"
}

response = requests.post(url, json=data)
if response.status_code == 201:
    user = response.json()
    print(f"User created with ID: {user['id']}")
else:
    print(f"Error: {response.json()}")
```

### JavaScript Example
```javascript
const response = await fetch('http://localhost:8000/api/v1/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'john@example.com',
    username: 'johndoe',
    password: 'SecurePass123!',
    full_name: 'John Doe'
  })
});

const user = await response.json();
if (response.ok) {
  console.log('User created:', user);
} else {
  console.error('Error:', user);
}
```

## Business Logic

1. **Email Validation**: Validates email format using Pydantic's EmailStr
2. **Username Validation**: Ensures username is alphanumeric and unique
3. **Password Hashing**: Passwords are hashed using bcrypt before storage
4. **Duplicate Check**: Prevents duplicate email and username registration
5. **User Creation**: Creates user with default values (is_active=true, is_verified=false)

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **Input Validation**: Comprehensive validation using Pydantic
- **Email Format Validation**: Ensures proper email format
- **SQL Injection Protection**: Uses SQLAlchemy ORM
- **Data Sanitization**: Proper handling of user input

## Related Endpoints

- `POST /api/v1/auth/login` - Login with registered credentials
- `GET /api/v1/auth/me` - Get current user information
- `POST /api/v1/auth/refresh` - Refresh access token

## Notes

- Username must be unique across the system
- Email must be unique across the system
- Full name is optional
- User is created with `is_active=true` and `is_verified=false` by default
- Password strength validation is enforced at the API level
