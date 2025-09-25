#!/bin/bash

echo "Setting up Expense Tracker Flask API..."

echo "1. Creating virtual environment..."
python3 -m venv flask-env

echo "2. Activating virtual environment..."
source flask-env/bin/activate

echo "3. Installing dependencies..."
pip install -r requirements.txt

echo "4. Creating database..."
createdb expense_tracker_db 2>/dev/null || echo "Database may already exist"

echo "5. Initializing Flask-Migrate..."
export FLASK_APP=run.py
flask db init

echo "6. Creating initial migration..."
flask db migrate -m "Initial migration: User, Category, Expense, Budget models"

echo "7. Applying migration..."
flask db upgrade

echo ""
echo "Setup complete! Run 'python run.py' to start the application."