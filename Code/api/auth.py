from typing import Tuple

from api.decorators import server_exception_handler
from quart import Blueprint, jsonify, request
from systems.db_systems import UniqueConstraintError
from systems.network import AuthError, UserAuth

auth_bp = Blueprint('auth', __name__)

def _get_login_password(data: dict) -> Tuple[str, str]:
    if "login" not in data:
        raise ValueError("Login is required")
    
    if "password" not in data:
        raise ValueError("Password is required")
    
    return data["login"], data["password"]

@server_exception_handler
@auth_bp.route('/register', methods=['POST'])
async def api_register():
    user_auth = UserAuth()
    data = await request.json
    login, password = _get_login_password(data)
    try:
        await user_auth.register_user(login, password)
        return jsonify({"message": "User registered successfully"}), 201
    
    except UniqueConstraintError:
        return jsonify({"message": "Login already exists"}), 409

@server_exception_handler
@auth_bp.route('/login', methods=['POST'])
async def api_login():
    data = await request.json
    login, password = _get_login_password(data)
    user_auth = UserAuth()
    try:
        token = await user_auth.login_user(login, password)
        return jsonify({"message": "Login successful", "token": token}), 200
    
    except AuthError:
        return jsonify({"message": "Invalid credentials"}), 401
