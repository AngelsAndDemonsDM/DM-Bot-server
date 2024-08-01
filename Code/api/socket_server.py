import asyncio
import logging
import signal
from asyncio import StreamReader, StreamWriter

from systems.events_system import EventManager
from systems.network import (AccessError, AuthError, SocketConnectManager,
                             UserAuth)

logger = logging.getLogger("Socket Server")

async def handle_client(reader: StreamReader, writer: StreamWriter):
    socket_manager: SocketConnectManager = SocketConnectManager.get_instance()
    event_manager: EventManager = EventManager.get_instance()
    user_auth: UserAuth = UserAuth.get_instance()
    default_socket_buffer: int = 8192
    
    user = None
    try:
        # Получаем токен
        token_data = await reader.read(default_socket_buffer)
        try:
            token = token_data.decode('utf-8').strip()
        except UnicodeDecodeError as e:
            logger.error(f"Decoding error: {e}. Data received: {token_data}")
            await send_response(writer, b"Invalid token format")
            return
        
        if not token:
            await send_response(writer, b"Missing token")
            return
        
        user, access = await user_auth.get_login_access_by_token(token)
        
        socket_manager.add_user_connect(user, writer)
        
        await send_response(writer, b"Token accepted")
        
        while True:
            message_data = await reader.read(default_socket_buffer)
            if not message_data:
                break
            
            try:
                message_data = SocketConnectManager.unpack_data(message_data)
                event_type = message_data.get("ev_type")
                await event_manager.call_event(event_type, socket_user=user, socket_access=access, **message_data)
            
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    except AuthError:
        await send_response(writer, b"Unauthorized")
    
    except AccessError:
        await send_response(writer, b"Forbidden")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    finally:
        if user:
            socket_manager.rm_user_connect(user)
        writer.close()
        await writer.wait_closed()

async def send_response(writer: StreamWriter, message: bytes):
    writer.write(message)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def start_socket_server(host='0.0.0.0', port=5001):
    server = await asyncio.start_server(handle_client, host, port)
    logger.info(f"Server started on {host}:{port}")

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

    await server.serve_forever()
