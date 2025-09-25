from datetime import datetime, timezone
from app.config.extensions import db
from app.models.base import BaseModel

class Expense(BaseModel):
    __tablename__ = 'expenses'

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text)
    expense_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    payment_method = db.Column(db.String(50))
    receipt_url = db.Column(db.String(255))
    is_recurring = db.Column(db.Boolean, default=False)
    recurring_frequency = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    user = db.relationship('User', back_populates='expenses')
    category = db.relationship('Category', back_populates='expenses')

    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'amount': float(self.amount) if self.amount else 0,
            'description': self.description,
            'notes': self.notes,
            'expense_date': self.expense_date.isoformat() if self.expense_date else None,
            'payment_method': self.payment_method,
            'receipt_url': self.receipt_url,
            'is_recurring': self.is_recurring,
            'recurring_frequency': self.recurring_frequency,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_relations:
            data['user'] = self.user.to_dict() if self.user else None
            data['category'] = self.category.to_dict() if self.category else None
        return data

    def __repr__(self):
        return f'<Expense {self.description} - ${self.amount}>'