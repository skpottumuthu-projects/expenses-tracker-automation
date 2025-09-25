# Expense Tracker Database Design

## Entity Relationship Diagram

```
┌─────────────────┐
│     Users       │
├─────────────────┤
│ id (PK)         │
│ email           │
│ username        │
│ password_hash   │
│ first_name      │
│ last_name       │
│ is_active       │
│ created_at      │
│ updated_at      │
└─────────────────┘
        │
        │ 1:N
        │
        ├──────────────────────────────┬──────────────────┐
        │                              │                  │
        ▼                              ▼                  ▼
┌─────────────────┐          ┌─────────────────┐  ┌─────────────────┐
│   Categories    │          │    Expenses     │  │     Budgets     │
├─────────────────┤          ├─────────────────┤  ├─────────────────┤
│ id (PK)         │          │ id (PK)         │  │ id (PK)         │
│ name            │◄─────────│ category_id(FK) │  │ name            │
│ description     │   N:1    │ user_id (FK)    │  │ amount          │
│ icon            │          │ amount          │  │ period          │
│ color           │          │ description     │  │ start_date      │
│ is_default      │          │ notes           │  │ end_date        │
│ user_id (FK)    │          │ expense_date    │  │ alert_threshold │
│ created_at      │          │ payment_method  │  │ is_active       │
│ updated_at      │          │ receipt_url     │  │ user_id (FK)    │
└─────────────────┘          │ is_recurring    │  │ category_id(FK) │
                             │ recurring_freq  │  │ created_at      │
                             │ created_at      │  │ updated_at      │
                             │ updated_at      │  └─────────────────┘
                             └─────────────────┘
```

## Table Definitions

### Users Table
Primary table for user authentication and profile information.

| Column         | Type          | Constraints                    | Description                    |
|---------------|---------------|--------------------------------|--------------------------------|
| id            | Integer       | PRIMARY KEY                    | Auto-incrementing user ID      |
| email         | String(120)   | UNIQUE, NOT NULL, INDEXED      | User's email address           |
| username      | String(80)    | UNIQUE, NOT NULL, INDEXED      | Unique username                |
| password_hash | String(255)   | NOT NULL                       | Hashed password                |
| first_name    | String(50)    | NULLABLE                       | User's first name              |
| last_name     | String(50)    | NULLABLE                       | User's last name               |
| is_active     | Boolean       | NOT NULL, DEFAULT TRUE         | Account active status          |
| created_at    | DateTime      | NOT NULL                       | Account creation timestamp     |
| updated_at    | DateTime      | NOT NULL                       | Last update timestamp          |

**Indexes:**
- `email` - For fast user lookup by email
- `username` - For fast user lookup by username

---

### Categories Table
Stores expense categories (both user-defined and system defaults).

| Column      | Type        | Constraints                          | Description                    |
|------------|-------------|--------------------------------------|--------------------------------|
| id         | Integer     | PRIMARY KEY                          | Auto-incrementing category ID  |
| name       | String(50)  | NOT NULL                             | Category name                  |
| description| Text        | NULLABLE                             | Category description           |
| icon       | String(50)  | NULLABLE                             | Icon identifier                |
| color      | String(7)   | NULLABLE                             | Hex color code (e.g., #FF5733) |
| is_default | Boolean     | DEFAULT FALSE                        | System default category        |
| user_id    | Integer     | FOREIGN KEY (users.id), NULLABLE     | Owner user (NULL for defaults) |
| created_at | DateTime    | NOT NULL                             | Creation timestamp             |
| updated_at | DateTime    | NOT NULL                             | Last update timestamp          |

**Unique Constraints:**
- `(name, user_id)` - Prevent duplicate category names per user

**Business Rules:**
- Default categories (`is_default=True`) are system-wide with `user_id=NULL`
- User-specific categories have a `user_id`
- Users can create categories with same names as defaults

---

### Expenses Table
Records all expense transactions.

| Column             | Type          | Constraints                      | Description                        |
|-------------------|---------------|----------------------------------|------------------------------------|
| id                | Integer       | PRIMARY KEY                      | Auto-incrementing expense ID       |
| amount            | Numeric(10,2) | NOT NULL                         | Expense amount (2 decimal places)  |
| description       | String(200)   | NOT NULL                         | Expense description                |
| notes             | Text          | NULLABLE                         | Additional notes                   |
| expense_date      | DateTime      | NOT NULL, DEFAULT NOW            | Date of expense                    |
| payment_method    | String(50)    | NULLABLE                         | Payment method (cash, card, etc.)  |
| receipt_url       | String(255)   | NULLABLE                         | Receipt image/file URL             |
| is_recurring      | Boolean       | DEFAULT FALSE                    | Recurring expense flag             |
| recurring_frequency| String(20)   | NULLABLE                         | Frequency (daily, weekly, monthly) |
| user_id           | Integer       | FOREIGN KEY (users.id), NOT NULL | Expense owner                      |
| category_id       | Integer       | FOREIGN KEY (categories.id), NOT NULL | Expense category              |
| created_at        | DateTime      | NOT NULL                         | Record creation timestamp          |
| updated_at        | DateTime      | NOT NULL                         | Last update timestamp              |

**Indexes:**
- `user_id` - For fast user expense queries
- `category_id` - For category-based filtering
- `expense_date` - For date range queries

---

### Budgets Table
Budget limits and tracking.

| Column          | Type          | Constraints                           | Description                        |
|----------------|---------------|---------------------------------------|------------------------------------|
| id             | Integer       | PRIMARY KEY                           | Auto-incrementing budget ID        |
| name           | String(100)   | NOT NULL                              | Budget name                        |
| amount         | Numeric(10,2) | NOT NULL                              | Budget amount limit                |
| period         | String(20)    | NOT NULL                              | Period (daily, weekly, monthly)    |
| start_date     | DateTime      | NOT NULL, DEFAULT NOW                 | Budget start date                  |
| end_date       | DateTime      | NULLABLE                              | Budget end date (NULL=ongoing)     |
| alert_threshold| Integer       | DEFAULT 80                            | Alert at % usage (e.g., 80%)       |
| is_active      | Boolean       | DEFAULT TRUE                          | Budget active status               |
| user_id        | Integer       | FOREIGN KEY (users.id), NOT NULL      | Budget owner                       |
| category_id    | Integer       | FOREIGN KEY (categories.id), NULLABLE | Category (NULL=overall budget)     |
| created_at     | DateTime      | NOT NULL                              | Record creation timestamp          |
| updated_at     | DateTime      | NOT NULL                              | Last update timestamp              |

**Indexes:**
- `user_id` - For user budget queries
- `category_id` - For category-specific budgets

**Business Rules:**
- If `category_id` is NULL, budget applies to all expenses
- If `category_id` is set, budget applies only to that category
- `alert_threshold` triggers notifications when spent amount reaches percentage

---

## Relationships

1. **User → Categories** (1:N)
   - One user can have many categories
   - Cascade delete: When user is deleted, their categories are deleted

2. **User → Expenses** (1:N)
   - One user can have many expenses
   - Cascade delete: When user is deleted, their expenses are deleted

3. **User → Budgets** (1:N)
   - One user can have many budgets
   - Cascade delete: When user is deleted, their budgets are deleted

4. **Category → Expenses** (1:N)
   - One category can have many expenses
   - A category must exist before creating expenses

5. **Category → Budgets** (1:N, Optional)
   - Budgets can optionally be linked to a category
   - NULL category_id means budget applies to all expenses

---

## Key Features

### 1. Soft Relationships
- Categories can be shared (system defaults) or user-specific
- Budgets can be category-specific or overall

### 2. Audit Trail
- All tables have `created_at` and `updated_at` timestamps
- Track when records are created and modified

### 3. Data Integrity
- Foreign key constraints ensure referential integrity
- Unique constraints prevent duplicate data
- NOT NULL constraints ensure required data

### 4. Performance Optimizations
- Indexed frequently queried columns (email, username)
- Lazy loading on relationships to avoid N+1 queries
- Numeric type for precise monetary calculations

### 5. Extensibility
- Base model pattern for common fields
- Easy to add new models with shared functionality
- Support for recurring expenses (future feature)
- Receipt URL storage for document management