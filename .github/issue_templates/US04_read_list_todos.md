# User Story: Read/List TODOs

As a logged-in user, I want to retrieve my TODOs with filters and pagination.

## Acceptance Criteria
- [ ] Supports pagination (`page`, `size`)
- [ ] Supports filters: `status`, `due_date` (range/overdue)
- [ ] Success: 200 OK with list of user’s TODOs
- [ ] Failure: Unauthorized → 401 Unauthorized; Invalid filters → appropriate error

## Notes
- Area: TODO Management
- Dependencies: Authentication

