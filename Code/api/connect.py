import logging

from quart import Blueprint, websocket
from systems.events import EventManager
from systems.network import (AccessError, AuthError, UserAuth,
                             WebSocketConnectManager)

connect_bp = Blueprint('connect', __name__)

@connect_bp.websocket('/connect')
async def api_connect():
    websocket_manager = WebSocketConnectManager()
    event_manager = EventManager()
    
    try:
        token = websocket.headers.get('Authorization')
        if not token:
            await websocket.send("Missing token")
            await websocket.close()
            return
        
        user_auth = UserAuth()
        user, access = await user_auth.get_login_access_by_token(token)

        websocket_manager.add_user_connect(user, websocket)
        
        while True:
            message_data = await websocket.receive_json()
            message_data = WebSocketConnectManager.unpack_data(message_data)
            event_type = message_data.get("ev_type")

            await event_manager.call_event(event_type, websocket_user=user, websocket_access=access, **message_data)
    
    except AuthError:
        await websocket.send("Unauthorized")
    
    except AccessError:
        await websocket.send("Forbidden")
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    
    finally:
        websocket_manager.rm_user_connect(user)
        await websocket.close()
