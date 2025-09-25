from app.config.extensions import db
from app.models.base import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(7))
    is_default = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    user = db.relationship('User', back_populates='categories')
    expenses = db.relationship('Expense', back_populates='category', lazy='dynamic')

    __table_args__ = (
        db.UniqueConstraint('name', 'user_id', name='uq_category_name_user'),
    )

    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'is_default': self.is_default,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_relations:
            data['expenses_count'] = self.expenses.count()
        return data

    def __repr__(self):
        return f'<Category {self.name}>'