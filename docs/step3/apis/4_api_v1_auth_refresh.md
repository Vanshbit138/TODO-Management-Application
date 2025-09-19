# API Documentation: Refresh Token

## Endpoint Details
- **Method**: `POST`
- **URL**: `/api/v1/auth/refresh`
- **Description**: Refreshes the current access token and returns a new one
- **Authentication**: Required (JWT Bearer Token)
- **Response Model**: `TokenResponse`

## Request

### Headers
```
Authorization: Bearer <jwt_token>
```

### Path Parameters
None

### Query Parameters
None

### Request Body
None

## Response

### Success Response (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzA1NjQ4MDAwfQ.new_signature",
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
  "detail": "Internal server error during token refresh"
}
```

## Example Usage

### cURL Example
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Python Example
```python
import requests

url = "http://localhost:8000/api/v1/auth/refresh"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

response = requests.post(url, headers=headers)
if response.status_code == 200:
    token_data = response.json()
    new_token = token_data['access_token']
    user = token_data['user']
    print(f"Token refreshed successfully!")
    print(f"New token: {new_token}")
    print(f"User: {user['username']}")
else:
    print(f"Token refresh failed: {response.json()}")
```

### JavaScript Example
```javascript
const token = localStorage.getItem('access_token');

const response = await fetch('http://localhost:8000/api/v1/auth/refresh', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const tokenData = await response.json();
if (response.ok) {
  const { access_token, user } = tokenData;
  console.log('Token refreshed successfully!');
  
  // Update stored token
  localStorage.setItem('access_token', access_token);
  console.log('New token stored');
} else {
  console.error('Token refresh failed:', tokenData);
  // Handle refresh failure - redirect to login
  localStorage.removeItem('access_token');
  window.location.href = '/login';
}
```

## Business Logic

1. **Token Validation**: Validates current JWT token
2. **User Verification**: Ensures user exists and is active
3. **New Token Generation**: Creates a new JWT token with fresh expiration
4. **User Data**: Returns current user information
5. **Response**: Returns new token and user data

## Security Features

- **Token Validation**: Verifies current token before issuing new one
- **User Status Check**: Ensures user is still active
- **Fresh Expiration**: New token has full expiration time
- **Same User Data**: Token contains same user information

## Token Information

### New JWT Payload
```json
{
  "sub": "1",
  "email": "user@example.com",
  "exp": 1705650000,
  "iat": 1705648200
}
```

### Token Usage
Replace the old token with the new one:
```
Authorization: Bearer <new_access_token>
```

## Related Endpoints

- `POST /api/v1/auth/login` - Initial login to get token
- `GET /api/v1/auth/me` - Get current user information
- `POST /api/v1/auth/register` - Register a new user

## Notes

- Requires valid JWT token (can be expired)
- Returns new token with fresh 30-minute expiration
- Useful for extending user sessions
- Should be called before token expires
- Old token becomes invalid after refresh
- No request body required
