from flask import Blueprint, request, jsonify


bp = Blueprint('health', __name__)
# Note: Blueprint name changed from 'api' to '.' to avoid conflicts

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message":"I'm up and running"}), 200
