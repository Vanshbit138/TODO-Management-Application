# User Story: User Login

As a registered user, I want to log in to access my personal TODOs.

## Acceptance Criteria
- [ ] Success: 200 OK with JWT token (valid 24h) containing user ID + email
- [ ] Invalid credentials / user not found → 401 Unauthorized
- [ ] Missing fields → 422 Unprocessable Entity

## Notes
- Area: Authentication
- Dependencies: User registration, JWT issuing and validation

