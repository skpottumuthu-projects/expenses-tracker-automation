from flask import Blueprint, request
from pydantic import ValidationError
from app.models.budget import Budget
from app.models.user import User
from app.models.role import Category
from app.schemas.budget_schema import BudgetCreateSchema, BudgetUpdateSchema
from app.utils.responses import success_response, error_response, created_response, not_found_response, validation_error_response

bp = Blueprint('budgets', __name__)

@bp.route('/', methods=['GET'])
def get_budgets():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    is_active = request.args.get('is_active', type=bool)

    query = Budget.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if is_active is not None:
        query = query.filter_by(is_active=is_active)

    budgets = query.all()
    return success_response([budget.to_dict() for budget in budgets])

@bp.route('/<int:budget_id>', methods=['GET'])
def get_budget(budget_id):
    budget = Budget.query.get(budget_id)
    if not budget:
        return not_found_response("Budget not found")
    return success_response(budget.to_dict(include_relations=True))

@bp.route('/', methods=['POST'])
def create_budget():
    try:
        data = BudgetCreateSchema(**request.get_json())
        user_id = request.args.get('user_id', type=int)

        if not user_id:
            return error_response("user_id is required", status_code=400)

        user = User.query.get(user_id)
        if not user:
            return not_found_response("User not found")

        if data.category_id:
            category = Category.query.get(data.category_id)
            if not category:
                return not_found_response("Category not found")

        budget = Budget(
            name=data.name,
            amount=data.amount,
            period=data.period,
            start_date=data.start_date,
            end_date=data.end_date,
            alert_threshold=data.alert_threshold,
            user_id=user_id,
            category_id=data.category_id
        )
        budget.save()

        return created_response(budget.to_dict(include_relations=True), "Budget created successfully")

    except ValidationError as e:
        return validation_error_response(e.errors())
    except Exception as e:
        return error_response(str(e), status_code=500)

@bp.route('/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    try:
        budget = Budget.query.get(budget_id)
        if not budget:
            return not_found_response("Budget not found")

        data = BudgetUpdateSchema(**request.get_json())

        if data.name:
            budget.name = data.name
        if data.amount is not None:
            budget.amount = data.amount
        if data.period:
            budget.period = data.period
        if data.end_date is not None:
            budget.end_date = data.end_date
        if data.alert_threshold is not None:
            budget.alert_threshold = data.alert_threshold
        if data.is_active is not None:
            budget.is_active = data.is_active
        if data.category_id is not None:
            if data.category_id:
                category = Category.query.get(data.category_id)
                if not category:
                    return not_found_response("Category not found")
            budget.category_id = data.category_id

        budget.save()
        return success_response(budget.to_dict(include_relations=True), "Budget updated successfully")

    except ValidationError as e:
        return validation_error_response(e.errors())
    except Exception as e:
        return error_response(str(e), status_code=500)

@bp.route('/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    try:
        budget = Budget.query.get(budget_id)
        if not budget:
            return not_found_response("Budget not found")

        budget.delete()
        return success_response(message="Budget deleted successfully")

    except Exception as e:
        return error_response(str(e), status_code=500)