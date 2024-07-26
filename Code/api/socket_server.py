import asyncio
import logging
from asyncio import StreamReader, StreamWriter

from systems.events_system import EventManager
from systems.network import (AccessError, AuthError, SocketConnectManager,
                             UserAuth)

logger = logging.getLogger("Socket Server")

async def handle_client(reader: StreamReader, writer: StreamWriter):
    socket_manager: SocketConnectManager = SocketConnectManager.get_instance()
    event_manager: EventManager = EventManager.get_instance()
    user_auth: UserAuth = UserAuth.get_instance()
    default_soket_buffer: int = 8192
    
    user = None
    try:
        # Получаем токен
        token_data = await reader.read(default_soket_buffer)
        try:
            token = token_data.decode('utf-8')
        except UnicodeDecodeError as e:
            logger.error(f"Decoding error: {e}. Data received: {token_data}")
            writer.write(b"Invalid token format")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return
        
        if not token:
            writer.write(b"Missing token")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return
        
        user, access = await user_auth.get_login_access_by_token(token)
        
        socket_manager.add_user_connect(user, writer)
        
        writer.write(b"Token accepted")
        await writer.drain()
        
        while True:
            message_data = await reader.read(default_soket_buffer)
            if not message_data:
                break
            
            try:
                message_data = SocketConnectManager.unpack_data(message_data)
                event_type = message_data.get("ev_type", None)
                await event_manager.call_event(event_type, socket_user=user, socket_access=access, **message_data)
            
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    except AuthError:
        writer.write(b"Unauthorized")
        await writer.drain()
    
    except AccessError:
        writer.write(b"Forbidden")
        await writer.drain()
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    finally:
        if user:
            socket_manager.rm_user_connect(user)
        writer.close()
        await writer.wait_closed()

def start_socket_server(host='0.0.0.0', port=5001):
    async def main():
        server = await asyncio.start_server(handle_client, host, port)
        logger.info(f"Socket server started on {host}:{port}")
        async with server:
            await server.serve_forever()
    
    asyncio.run(main())
