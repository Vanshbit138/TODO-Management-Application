# User Story: Update TODO

As a logged-in user, I want to update my TODO items.

## Acceptance Criteria
- [ ] Editable fields: `title`, `description`, `status`, `due_date`
- [ ] Success: 200 OK with updated TODO details
- [ ] Failure: Task not found → 404 Not Found; User not owner → 403 Forbidden; Invalid data → 422 Unprocessable Entity

## Notes
- Area: TODO Management
- Dependencies: Authentication

