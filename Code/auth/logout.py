from auth.bp_reg import auth_bp
from main_impt import auth_manager
from quart import jsonify, request


@auth_bp.route('/logout', methods=['POST'])
async def logout():
    data = await request.get_json()
    
    if 'token' not in data:
        return jsonify({'message': 'Field "token" is required'}), 400
    
    try:
        await auth_manager.logout_user(data['token'])
        return jsonify({'message': 'Logout attempt was made'}), 202
    
    except ValueError as e:
        return jsonify({'message': str(e)}), 403
    
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
