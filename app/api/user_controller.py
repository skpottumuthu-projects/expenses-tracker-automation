from flask import Blueprint, request
from pydantic import ValidationError
from app.models.user import User
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from app.utils.responses import success_response, error_response, created_response, not_found_response, validation_error_response

bp = Blueprint('users', __name__)

@bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return success_response([user.to_dict() for user in users])

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return not_found_response("User not found")
    return success_response(user.to_dict(include_relations=True))

@bp.route('/', methods=['POST'])
def create_user():
    try:
        data = UserCreateSchema(**request.get_json())

        if User.query.filter_by(email=data.email).first():
            return error_response("Email already exists", status_code=409)

        if User.query.filter_by(username=data.username).first():
            return error_response("Username already exists", status_code=409)

        user = User(
            email=data.email,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name
        )
        user.set_password(data.password)
        user.save()

        return created_response(user.to_dict(), "User created successfully")

    except ValidationError as e:
        return validation_error_response(e.errors())
    except Exception as e:
        return error_response(str(e), status_code=500)

@bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response("User not found")

        data = UserUpdateSchema(**request.get_json())

        if data.email and data.email != user.email:
            if User.query.filter_by(email=data.email).first():
                return error_response("Email already exists", status_code=409)
            user.email = data.email

        if data.username and data.username != user.username:
            if User.query.filter_by(username=data.username).first():
                return error_response("Username already exists", status_code=409)
            user.username = data.username

        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        if data.is_active is not None:
            user.is_active = data.is_active

        user.save()
        return success_response(user.to_dict(), "User updated successfully")

    except ValidationError as e:
        return validation_error_response(e.errors())
    except Exception as e:
        return error_response(str(e), status_code=500)

@bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response("User not found")

        user.delete()
        return success_response(message="User deleted successfully")

    except Exception as e:
        return error_response(str(e), status_code=500)