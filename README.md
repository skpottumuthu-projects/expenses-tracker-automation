# Expense Tracker Flask API

A Flask-based REST API for tracking expenses with PostgreSQL database.

## Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip or uv package manager

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd expense_tracker_flask_api
```

### 2. Create virtual environment

```bash
python3 -m venv flask-env
source flask-env/bin/activate  # On Windows: flask-env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or using pyproject.toml:

```bash
pip install -e .
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and update with your database credentials:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=expense_tracker_db
```

### 5. Set up PostgreSQL database

```bash
createdb expense_tracker_db
```

### 6. Initialize database migrations

```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

Or use the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

### 7. Run the application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## Project Structure

```
expense_tracker_flask_api/
├── app/
│   ├── __init__.py           # Application factory
│   ├── api/                  # API routes/blueprints
│   ├── models/               # Database models
│   │   ├── base.py          # Base model with common fields
│   │   ├── user.py          # User model
│   │   ├── role.py          # Category model
│   │   ├── expense.py       # Expense model
│   │   └── budget.py        # Budget model
│   ├── schemas/              # Pydantic schemas for validation
│   ├── services/             # Business logic
│   └── config/               # Configuration files
│       ├── config.py        # Config classes
│       └── extensions.py    # Flask extensions
├── migrations/               # Database migrations (Flask-Migrate)
├── tests/                    # Test files
├── .env                      # Environment variables (not in git)
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project metadata
├── run.py                    # Application entry point
└── setup.sh                  # Setup script
```

## Database Schema

### Models

1. **User** - User accounts with authentication
   - email, username, password_hash
   - first_name, last_name, is_active
   - Relationships: expenses, budgets, categories

2. **Category** - Expense categories
   - name, description, icon, color
   - is_default, user_id
   - Supports both user-specific and default categories

3. **Expense** - Expense records
   - amount, description, notes
   - expense_date, payment_method, receipt_url
   - is_recurring, recurring_frequency
   - Relationships: user, category

4. **Budget** - Budget tracking
   - name, amount, period
   - start_date, end_date, alert_threshold
   - is_active
   - Relationships: user, category (optional)

## Development

### Running tests

```bash
pytest
```

### Code formatting

```bash
black .
```

### Linting

```bash
flake8
```

## API Endpoints

_(To be documented as endpoints are implemented)_

## License

MIT