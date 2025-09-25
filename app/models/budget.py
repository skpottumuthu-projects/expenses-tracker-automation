from datetime import datetime, timezone
from app.config.extensions import db
from app.models.base import BaseModel

class Budget(BaseModel):
    __tablename__ = 'budgets'

    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    period = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    end_date = db.Column(db.DateTime)
    alert_threshold = db.Column(db.Integer, default=80)
    is_active = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    user = db.relationship('User', back_populates='budgets')
    category = db.relationship('Category')

    def get_spent_amount(self):
        from app.models.expense import Expense
        query = Expense.query.filter(
            Expense.user_id == self.user_id,
            Expense.expense_date >= self.start_date
        )
        if self.end_date:
            query = query.filter(Expense.expense_date <= self.end_date)
        if self.category_id:
            query = query.filter(Expense.category_id == self.category_id)

        total = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.user_id == self.user_id,
            Expense.expense_date >= self.start_date
        )
        if self.end_date:
            total = total.filter(Expense.expense_date <= self.end_date)
        if self.category_id:
            total = total.filter(Expense.category_id == self.category_id)

        result = total.scalar()
        return float(result) if result else 0.0

    def get_remaining_amount(self):
        return float(self.amount) - self.get_spent_amount()

    def get_usage_percentage(self):
        if self.amount == 0:
            return 0
        return (self.get_spent_amount() / float(self.amount)) * 100

    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'name': self.name,
            'amount': float(self.amount) if self.amount else 0,
            'period': self.period,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'alert_threshold': self.alert_threshold,
            'is_active': self.is_active,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'spent_amount': self.get_spent_amount(),
            'remaining_amount': self.get_remaining_amount(),
            'usage_percentage': round(self.get_usage_percentage(), 2),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_relations:
            data['user'] = self.user.to_dict() if self.user else None
            data['category'] = self.category.to_dict() if self.category else None
        return data

    def __repr__(self):
        return f'<Budget {self.name} - ${self.amount}>'