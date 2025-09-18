  # User Stories & Acceptance Criteria

  ## Authentication

  ### User Registration
  **Story:** As a new user, I want to register an account so that I can access the TODO application.  

  **Acceptance Criteria:**  
  - **Input validation**
    - Valid email format required
    - Password must be ≥ 8 chars, include uppercase, lowercase, and a number
  - **On success**
    - Returns **201 Created** with `{ user_id, message }`
  - **Failure cases**
    - Email already exists → **400 Bad Request** ("Email already registered")
    - Invalid email or weak password → **400 Bad Request**
    - Missing required fields → **422 Unprocessable Entity** with field-level errors

  ---

  ### User Login
  **Story:** As a registered user, I want to log in to access my personal TODOs.  

  **Acceptance Criteria:**  
  - **On success**
    - Returns **200 OK** with JWT token (valid 24h) containing user ID + email
  - **Failure cases**
    - Invalid credentials / user not found → **401 Unauthorized**
    - Missing fields → **422 Unprocessable Entity**

  ---

  ## TODO Management

  ### Create TODO
  **Story:** As a logged-in user, I want to create TODO items.  

  **Acceptance Criteria:**  
  - **Required:** `title`  
  - **Optional:** `description`, `due_date`  
  - **Status values:** pending, in-progress, completed  
  - **On success:** Returns **201 Created** with TODO details  
  - **Failure cases:** Missing/invalid title → **422 Unprocessable Entity**

  ---

  ### Read/List TODOs
  **Story:** As a logged-in user, I want to retrieve my TODOs with filters and pagination.  

  **Acceptance Criteria:**  
  - Supports pagination (`page`, `size`)  
  - Supports filters: `status`, `due_date` (range/overdue)  
  - **On success:** Returns **200 OK** with list of user’s TODOs  
  - **Failure cases:** Unauthorized → **401 Unauthorized**  
  - Invalid filters → appropriate error code  

  ---

  ### Update TODO
  **Story:** As a logged-in user, I want to update my TODO items.  

  **Acceptance Criteria:**  
  - Editable fields: `title`, `description`, `status`, `due_date`  
  - **On success:** Returns **200 OK** with updated TODO details  
  - **Failure cases:**  
    - Task not found → **404 Not Found**  
    - User not owner → **403 Forbidden**  
    - Invalid data → **422 Unprocessable Entity**  

  ---

  ### Delete TODO
  **Story:** As a logged-in user, I want to delete my TODO items.  

  **Acceptance Criteria:**  
  - **On success:** Returns **204 No Content**  
  - **Failure cases:**  
    - Task not found → **404 Not Found**  
    - User not owner → **403 Forbidden**  
