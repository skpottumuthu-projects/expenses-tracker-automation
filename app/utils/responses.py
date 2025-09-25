from flask import jsonify
from typing import Any, Optional

def success_response(data: Any = None, message: str = "Success", status_code: int = 200):
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(message: str = "Error occurred", errors: Optional[dict] = None, status_code: int = 400):
    response = {
        "success": False,
        "message": message,
        "errors": errors
    }
    return jsonify(response), status_code

def created_response(data: Any = None, message: str = "Resource created successfully"):
    return success_response(data, message, 201)

def not_found_response(message: str = "Resource not found"):
    return error_response(message, status_code=404)

def validation_error_response(errors: dict, message: str = "Validation failed"):
    return error_response(message, errors, 422)