# User Story: Create TODO

As a logged-in user, I want to create TODO items.

## Acceptance Criteria
- [ ] Required: `title`
- [ ] Optional: `description`, `due_date`
- [ ] Status values: pending, in-progress, completed
- [ ] Success: 201 Created with TODO details
- [ ] Failure: missing/invalid title → 422 Unprocessable Entity

## Notes
- Area: TODO Management
- Dependencies: Authentication (must be logged in)

