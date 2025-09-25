#!/usr/bin/env python3
"""
Database initialization script
Run this to create all database tables
"""
import os
from app import create_app
from app.config.extensions import db

def init_database():
    print("🚀 Initializing database...")

    # Create Flask app
    app = create_app('development')

    with app.app_context():
        # Drop all tables (if exist) and recreate
        print("📦 Creating all tables...")
        db.create_all()
        print("✅ Database tables created successfully!")

        # List all tables
        print("\n📋 Created tables:")
        for table in db.metadata.tables.keys():
            print(f"   - {table}")

if __name__ == '__main__':
    init_database()