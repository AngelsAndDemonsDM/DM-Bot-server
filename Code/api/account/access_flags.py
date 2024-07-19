from api.account.bp_reg import account_bp
from api.api_tools import catch_MissingFilds_Auth_Exception, get_requester_info
from quart import jsonify, request


@catch_MissingFilds_Auth_Exception
@account_bp.route('/access_flags', methods=['POST'])
async def api_access_flags():
    _, _, requester_accses = await get_requester_info(request.headers)
    return jsonify(requester_accses._flags), 200 # Ай, ай, так низя, но мне похеру =)
