# Expense Tracker API Documentation

Base URL: `http://localhost:5004`

## Response Format

All responses follow this structure:

**Success Response:**
```json
{
  "success": true,
  "message": "Success message",
  "data": {...}
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error message",
  "errors": {...}
}
```

---

## Health Check

### GET `/health`
Check if API is running

**Response:**
```json
{
  "status": "ok",
  "message": "I'm up and running"
}
```

---

## Users API

### GET `/api/users/`
Get all users

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Success",
  "data": [
    {
      "id": 1,
      "email": "user@example.com",
      "username": "john_doe",
      "first_name": "John",
      "last_name": "Doe",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### GET `/api/users/<user_id>`
Get user by ID

**Response:** `200 OK` (includes relations)

### POST `/api/users/`
Create new user

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "secure123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Validation:**
- Email must be valid
- Username min 3 characters
- Password min 6 characters

**Response:** `201 Created`

### PUT `/api/users/<user_id>`
Update user

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "first_name": "Jane",
  "is_active": false
}
```

**Response:** `200 OK`

### DELETE `/api/users/<user_id>`
Delete user

**Response:** `200 OK`

---

## Categories API

### GET `/api/categories/`
Get categories

**Query Parameters:**
- `user_id` (int, optional) - Filter by user (returns user categories + defaults)

**Response:** `200 OK`

### GET `/api/categories/<category_id>`
Get category by ID

**Response:** `200 OK`

### POST `/api/categories/`
Create category

**Query Parameters:**
- `user_id` (int, optional) - Owner user ID

**Request Body:**
```json
{
  "name": "Food & Dining",
  "description": "Restaurant, groceries, etc.",
  "icon": "food",
  "color": "#FF5733"
}
```

**Response:** `201 Created`

### PUT `/api/categories/<category_id>`
Update category (cannot update defaults)

**Request Body:**
```json
{
  "name": "Updated Category",
  "color": "#00FF00"
}
```

**Response:** `200 OK`

### DELETE `/api/categories/<category_id>`
Delete category (cannot delete defaults)

**Response:** `200 OK`

---

## Expenses API

### GET `/api/expenses/`
Get expenses

**Query Parameters:**
- `user_id` (int) - Filter by user
- `category_id` (int) - Filter by category
- `start_date` (ISO date) - Filter from date
- `end_date` (ISO date) - Filter to date

**Example:** `/api/expenses/?user_id=1&start_date=2024-01-01`

**Response:** `200 OK`

### GET `/api/expenses/<expense_id>`
Get expense by ID

**Response:** `200 OK`

### POST `/api/expenses/`
Create expense

**Query Parameters:**
- `user_id` (int, required) - Owner user ID

**Request Body:**
```json
{
  "amount": 50.00,
  "description": "Lunch at restaurant",
  "notes": "Team lunch",
  "expense_date": "2024-01-15T12:30:00",
  "payment_method": "credit_card",
  "category_id": 1
}
```

**Validation:**
- Amount must be > 0
- Description required
- Category must exist

**Response:** `201 Created`

### PUT `/api/expenses/<expense_id>`
Update expense

**Request Body:**
```json
{
  "amount": 55.00,
  "description": "Updated lunch expense"
}
```

**Response:** `200 OK`

### DELETE `/api/expenses/<expense_id>`
Delete expense

**Response:** `200 OK`

---

## Budgets API

### GET `/api/budgets/`
Get budgets

**Query Parameters:**
- `user_id` (int) - Filter by user
- `category_id` (int) - Filter by category
- `is_active` (bool) - Filter by active status

**Response:** `200 OK` (includes spent/remaining calculations)

### GET `/api/budgets/<budget_id>`
Get budget by ID

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Monthly Food Budget",
    "amount": 500.00,
    "period": "monthly",
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": null,
    "alert_threshold": 80,
    "is_active": true,
    "user_id": 1,
    "category_id": 1,
    "spent_amount": 250.00,
    "remaining_amount": 250.00,
    "usage_percentage": 50.0
  }
}
```

### POST `/api/budgets/`
Create budget

**Query Parameters:**
- `user_id` (int, required) - Owner user ID

**Request Body:**
```json
{
  "name": "Monthly Food Budget",
  "amount": 500.00,
  "period": "monthly",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-01-31T23:59:59",
  "alert_threshold": 80,
  "category_id": 1
}
```

**Validation:**
- Amount must be > 0
- Period must be: daily, weekly, monthly, yearly

**Response:** `201 Created`

### PUT `/api/budgets/<budget_id>`
Update budget

**Request Body:**
```json
{
  "amount": 600.00,
  "alert_threshold": 75,
  "is_active": true
}
```

**Response:** `200 OK`

### DELETE `/api/budgets/<budget_id>`
Delete budget

**Response:** `200 OK`

---

## Error Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `403` - Forbidden (e.g., cannot delete default category)
- `404` - Not Found
- `409` - Conflict (e.g., duplicate email/username)
- `422` - Validation Error
- `500` - Internal Server Error

---

## Example Usage

### 1. Create a User
```bash
curl -X POST http://localhost:5004/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "john_doe",
    "password": "secure123",
    "first_name": "John"
  }'
```

### 2. Create a Category
```bash
curl -X POST "http://localhost:5004/api/categories/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Food",
    "icon": "🍔",
    "color": "#FF5733"
  }'
```

### 3. Add an Expense
```bash
curl -X POST "http://localhost:5004/api/expenses/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "description": "Lunch",
    "category_id": 1,
    "payment_method": "card"
  }'
```

### 4. Set a Budget
```bash
curl -X POST "http://localhost:5004/api/budgets/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monthly Food Budget",
    "amount": 500.00,
    "period": "monthly",
    "category_id": 1
  }'
```

### 5. Check Budget Status
```bash
curl http://localhost:5004/api/budgets/1
```