from typing import Tuple

from api.decorators import server_exception_handler
from quart import Blueprint, jsonify, request
from systems.network import AccessError, AuthError, UserAccess, UserAuth

admin_bp = Blueprint('admin', __name__)

async def _get_reqester_data(headers: dict) -> Tuple[str, UserAccess]:
    auth_token: str = headers.get('Authorization', None)
    if not auth_token:
        raise AuthError()
    
    user_auth = UserAuth.get_instance()
    return await user_auth.get_login_access_by_token(auth_token)

@server_exception_handler
@admin_bp.route('/delete_user', methods=['POST'])
async def api_delete_user():
    data = await request.json
    if "login" not in data:
        raise ValueError("'login' is required")
    
    _, requester_access = await _get_reqester_data(request.headers)
    if not requester_access.get_flag("delete_user"):
        raise AccessError()
    
    # Логика для удаления пользователя
    user_auth = UserAuth.get_instance()
    await user_auth.delete_user(data["login"])
    return jsonify({"message": "User deleted successfully"}), 200

@server_exception_handler
@admin_bp.route('/change_access', methods=['POST'])
async def api_change_access():
    data = await request.json
    if "login" not in data:
        raise ValueError("'login' is required")
    
    if "new_access" not in data:
        raise ValueError("'new_access' is required")
    
    if not isinstance(data["new_access"], dict):
        raise ValueError("'new_access' must be a Dict[str, bool]")
    
    _, requester_access = await _get_reqester_data(request.headers)
    if not requester_access.get_flag("change_access"):
        raise AccessError()
    
    user_auth = UserAuth.get_instance()
    target_access = await user_auth.get_access_by_login(data["login"])
    
    
    # Проверка, чтобы нельзя было выдавать доступ, которого у пользователя нет
    for access, value in data["new_access"].items():
        if not requester_access.get_flag(access):
            raise AccessError(f"Cannot grant access '{access}' which you don't have")
        
        else:
            target_access.set_flag(access, value)

    await user_auth.change_access(data["login"], data["new_access"])
    return jsonify({"message": "Access changed successfully"}), 200

@server_exception_handler
@admin_bp.route('/change_password', methods=['POST'])
async def api_change_password():
    data = await request.json
    if "new_password" not in data:
        raise ValueError("'new_password' is required")
    
    requester_login, _ = await _get_reqester_data(request.headers)
    
    user_auth = UserAuth.get_instance()
    await user_auth.change_password(requester_login, data["new_password"])
    return jsonify({"message": "Password changed successfully"}), 200
