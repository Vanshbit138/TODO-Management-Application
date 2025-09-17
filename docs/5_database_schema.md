# Database Schema

## Users Table
| Column          | Type                 | Constraints                            | Notes                     |
|-----------------|----------------------|----------------------------------------|---------------------------|
| id              | Serial (PK)          | Primary Key                            | Unique user ID            |
| email           | Varchar(255)         | UNIQUE, NOT NULL                       | User’s email (indexed)    |
| hashed_password | Varchar(255)         | NOT NULL                               | Bcrypt-hashed password    |
| is_active       | Boolean              | DEFAULT TRUE                           | Active flag               |
| created_at      | Timestamp with tz    | DEFAULT NOW()                          | Account creation timestamp|

🔹 **Indexes:**  
- Unique index on `email`  
- B-tree index on `created_at` (optional, for analytics)  

---

## Tasks Table
| Column       | Type                 | Constraints                                  | Notes                          |
|--------------|----------------------|----------------------------------------------|--------------------------------|
| id           | Serial (PK)          | Primary Key                                  | Unique task ID                 |
| title        | Varchar(255)         | NOT NULL                                     | Task title                     |
| description  | Text                 |                                              | Task details                   |
| status       | Enum                 | DEFAULT 'pending'                            | Values: pending, in-progress, completed |
| due_date     | Date                 |                                              | Optional deadline              |
| owner_id     | Integer              | NOT NULL, FK → users(id) ON DELETE CASCADE   | Task owner (foreign key)       |
| created_at   | Timestamp with tz    | DEFAULT NOW()                                | Task creation time             |
| updated_at   | Timestamp with tz    | DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP    | Last updated time              |

🔹 **Indexes:**  
- Index on `owner_id` (for quick lookups of user tasks)  
- Index on `status` (to optimize filtering by status)  
- Optional composite index on `(owner_id, due_date)` for overdue queries  

---

## Enums

```sql
CREATE TYPE task_status AS ENUM ('pending', 'in-progress', 'completed');

```
## Relationships

One-to-Many:

- users.id → tasks.owner_id
- A user can own many tasks
- Tasks are deleted automatically when the owning user is deleted (ON DELETE CASCADE)

```
Example ERD
 Users ───< Tasks
```

- One User can have many Tasks
- Each Task belongs to exactly one User