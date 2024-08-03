import asyncio
import logging
import signal

import websockets
from systems.events_system import EventManager
from systems.network import AccessError, AuthError, ConnectManager, UserAuth
from websockets import WebSocketServerProtocol

logger = logging.getLogger("Socket Server")

connect_manager: ConnectManager = ConnectManager()
event_manager: EventManager = EventManager()
user_auth: UserAuth = UserAuth()

async def handle_client(websocket: WebSocketServerProtocol, path: str):
    user = None
    try:
        token_data = await websocket.recv()
        try:
            token = token_data.strip()
        except Exception as e:
            logger.error(f"Error decoding token: {e}. Data received: {token_data}")
            await websocket.send("Invalid token format")
            return
        
        if not token:
            await websocket.send("Missing token")
            return
        
        user, access = await user_auth.get_login_access_by_token(token)
        
        connect_manager.add_user_connect(user, websocket)
        
        await websocket.send("Token accepted")
        
        async for message_data in websocket:
            try:
                message_data = ConnectManager.unpack_data(message_data)
                event_type = message_data.get("ev_type")
                await event_manager.call_open_event(event_type, socket_user=user, socket_access=access, **message_data)
            
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    except AuthError:
        await websocket.send("Unauthorized")
    
    except AccessError:
        await websocket.send("Forbidden")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    finally:
        if user:
            connect_manager.rm_user_connect(user)
        await websocket.close()

async def start_websocket_server(host='0.0.0.0', port=5001):
    server = await websockets.serve(handle_client, host, port)
    logger.info(f"WebSocket server started on ws://{host}:{port}")

    loop = asyncio.get_running_loop()

    # Функция для остановки сервера
    async def shutdown():
        logger.info("Shutting down server...")
        server.close()
        await server.wait_closed()
        loop.stop()
        logger.info("Server shutdown complete")

    # Регистрация обработчика сигнала для корректного завершения работы
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), lambda: asyncio.create_task(shutdown()))
