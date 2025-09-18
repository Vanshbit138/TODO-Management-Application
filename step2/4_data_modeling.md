# Step 2 — Data Modeling (Preview)

This step only **prepares entities** (not implemented yet).  
Full ORM models and Alembic migrations will be added in Step 3.

---

## Entities

### User
- Core entity for authentication/authorization
- Fields: `id`, `email`, `hashed_password`, `is_active`, `created_at`
- One-to-Many relationship with `Task`

### Task
- Represents a TODO item owned by a `User`
- Fields: `id`, `title`, `description`, `status`, `due_date`, `owner_id`, `created_at`, `updated_at`
- Belongs to exactly one `User`

---

## Relationships
- **User 1 ───< Many Tasks**  
- `users.id → tasks.owner_id` (FK with ON DELETE CASCADE)

---

