from werkzeug.security import generate_password_hash, check_password_hash
from app.config.extensions import db
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    expenses = db.relationship('Expense', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    budgets = db.relationship('Budget', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    categories = db.relationship('Category', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_relations:
            data['expenses_count'] = self.expenses.count()
            data['budgets_count'] = self.budgets.count()
        return data

    def __repr__(self):
        return f'<User {self.username}>'