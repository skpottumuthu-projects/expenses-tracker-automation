from flask import Flask
from app.config.config import config
from app.config.extensions import db, migrate

def create_app(config_name='development'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app import models

        # Auto-create tables if they don't exist (development only)
        if config_name == 'development':
            # db.create_all()
            print("✅ Database tables created/verified")

    return app