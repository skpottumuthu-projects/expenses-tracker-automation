from flask import Blueprint
from app.api.user_controller import bp as user_bp
from app.api.category_controller import bp as category_bp
from app.api.expense_controller import bp as expense_bp
from app.api.budget_controller import bp as budget_bp

bp = Blueprint('api', __name__)

bp.register_blueprint(user_bp, url_prefix='/users')
bp.register_blueprint(category_bp, url_prefix='/categories')
bp.register_blueprint(expense_bp, url_prefix='/expenses')
bp.register_blueprint(budget_bp, url_prefix='/budgets') 


 