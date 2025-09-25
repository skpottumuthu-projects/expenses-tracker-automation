from flask import Blueprint, request
from pydantic import ValidationError
from app.models.role import Category
from app.schemas.category_schema import CategoryCreateSchema, CategoryUpdateSchema
from app.utils.responses import success_response, error_response, created_response, not_found_response, validation_error_response

bp = Blueprint('categories', __name__)

@bp.route('/', methods=['GET'])
def get_categories():
    user_id = request.args.get('user_id', type=int)

    if user_id:
        categories = Category.query.filter(
            (Category.user_id == user_id) | (Category.is_default == True)
        ).all()
    else:
        categories = Category.query.filter_by(is_default=True).all()

    return success_response([cat.to_dict() for cat in categories])

@bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return not_found_response("Category not found")
    return success_response(category.to_dict(include_relations=True))

@bp.route('/', methods=['POST'])
def create_category():
    try:
        data = CategoryCreateSchema(**request.get_json())
        user_id = request.args.get('user_id', type=int)

        existing = Category.query.filter_by(
            name=data.name,
            user_id=user_id
        ).first()

        if existing:
            return error_response("Category with this name already exists for this user", status_code=409)

        category = Category(
            name=data.name,
            description=data.description,
            icon=data.icon,
            color=data.color,
            user_id=user_id
        )
        category.save()

        return created_response(category.to_dict(), "Category created successfully")

    except ValidationError as e:
        return validation_error_response(e.errors())
    except Exception as e:
        return error_response(str(e), status_code=500)

@bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return not_found_response("Category not found")

        if category.is_default:
            return error_response("Cannot update default categories", status_code=403)

        data = CategoryUpdateSchema(**request.get_json())

        if data.name:
            category.name = data.name
        if data.description is not None:
            category.description = data.description
        if data.icon is not None:
            category.icon = data.icon
        if data.color is not None:
            category.color = data.color

        category.save()
        return success_response(category.to_dict(), "Category updated successfully")

    except ValidationError as e:
        return validation_error_response(e.errors())
    except Exception as e:
        return error_response(str(e), status_code=500)

@bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return not_found_response("Category not found")

        if category.is_default:
            return error_response("Cannot delete default categories", status_code=403)

        category.delete()
        return success_response(message="Category deleted successfully")

    except Exception as e:
        return error_response(str(e), status_code=500)