from flask import Blueprint, request
from pydantic import ValidationError
from app.models.expense import Expense
from app.models.user import User
from app.models.role import Category
from app.schemas.expense_schema import ExpenseCreateSchema, ExpenseUpdateSchema
from app.utils.responses import success_response, error_response, created_response, not_found_response, validation_error_response
from app.config.extensions import db
from datetime import datetime

bp = Blueprint('expenses', __name__)

@bp.route('/', methods=['GET'])
def get_expenses():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Expense.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if start_date:
        query = query.filter(Expense.expense_date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Expense.expense_date <= datetime.fromisoformat(end_date))

    expenses = query.order_by(Expense.expense_date.desc()).all()
    return success_response([exp.to_dict() for exp in expenses])

@bp.route('/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return not_found_response("Expense not found")
    return success_response(expense.to_dict(include_relations=True))

@bp.route('/', methods=['POST'])
def create_expense():
    try:
        data = ExpenseCreateSchema(**request.get_json())
        user_id = request.args.get('user_id', type=int)

        if not user_id:
            return error_response("user_id is required", status_code=400)

        user = User.query.get(user_id)
        if not user:
            return not_found_response("User not found")

        category = Category.query.get(data.category_id)
        if not category:
            return not_found_response("Category not found")

        expense = Expense(
            amount=data.amount,
            description=data.description,
            notes=data.notes,
            expense_date=data.expense_date,
            payment_method=data.payment_method,
            receipt_url=data.receipt_url,
            user_id=user_id,
            category_id=data.category_id
        )
        expense.save()

        return created_response(expense.to_dict(include_relations=True), "Expense created successfully")

    except ValidationError as e:
        return validation_error_response(e.errors())
    except Exception as e:
        return error_response(str(e), status_code=500)

@bp.route('/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    try:
        expense = Expense.query.get(expense_id)
        if not expense:
            return not_found_response("Expense not found")

        data = ExpenseUpdateSchema(**request.get_json())

        if data.amount is not None:
            expense.amount = data.amount
        if data.description:
            expense.description = data.description
        if data.notes is not None:
            expense.notes = data.notes
        if data.expense_date:
            expense.expense_date = data.expense_date
        if data.payment_method is not None:
            expense.payment_method = data.payment_method
        if data.receipt_url is not None:
            expense.receipt_url = data.receipt_url
        if data.category_id:
            category = Category.query.get(data.category_id)
            if not category:
                return not_found_response("Category not found")
            expense.category_id = data.category_id

        expense.save()
        return success_response(expense.to_dict(include_relations=True), "Expense updated successfully")

    except ValidationError as e:
        return validation_error_response(e.errors())
    except Exception as e:
        return error_response(str(e), status_code=500)

@bp.route('/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        expense = Expense.query.get(expense_id)
        if not expense:
            return not_found_response("Expense not found")

        expense.delete()
        return success_response(message="Expense deleted successfully")

    except Exception as e:
        return error_response(str(e), status_code=500)