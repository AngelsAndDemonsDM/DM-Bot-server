from auth.bp_reg import auth_bp
from main_impt import auth_manager
from quart import jsonify, request
from systems.access_manager import AccessFlags


@auth_bp.route('/delete_user', methods=['POST'])
async def api_delete_user():
    try:
        data = await request.get_json()
        
        if 'requester_token' not in data:
            return jsonify({'message': 'Field "requester_login" is required'}), 400
        
        if 'login' not in data:
            return jsonify({'message': 'Field "login" is required'}), 400
        
        try:
            access: AccessFlags = await auth_manager.get_user_access(data['requester_token'])
            if not access["delete_users"]:
                return jsonify({'message': 'Access denied'}), 403
        
        except ValueError as e:
            return jsonify({'message': str(e)}), 403
        
        await auth_manager.delete_user(data['requester_login'])
        return jsonify({'message': 'User deleted successfully'}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 403
    
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
