from api.account.bp_reg import account_bp
from api.api_tools import get_requester_info, handle_request_errors
from quart import jsonify, request


@handle_request_errors
@account_bp.route('/access_flags', methods=['POST'])
async def api_access_flags():
    _, _, requester_accses = await get_requester_info(request.headers)
    return jsonify(requester_accses.all_access), 200
