import logging
import socket
import threading

from systems.events import EventManager
from systems.network import (AccessError, AuthError, SocketConnectManager,
                             UserAuth)

logger = logging.getLogger("Socket Server")

def handle_client(client_socket: socket.socket, address):
    socket_manager = SocketConnectManager()
    event_manager = EventManager()
    
    try:
        token = client_socket.recv(1024).decode('utf-8')
        if not token:
            client_socket.send(b"Missing token")
            client_socket.close()
            return
        
        user_auth = UserAuth()
        user, access = user_auth.get_login_access_by_token(token)

        socket_manager.add_user_connect(user, client_socket)
        
        while True:
            message_data = client_socket.recv(1024)
            if not message_data:
                break
            
            message_data: dict = SocketConnectManager.unpack_data(message_data)
            event_type = message_data.get("ev_type")

            event_manager.call_event(event_type, socket_user=user, socket_access=access, **message_data)
    
    except AuthError:
        client_socket.send(b"Unauthorized")
    
    except AccessError:
        client_socket.send(b"Forbidden")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    finally:
        socket_manager.rm_user_connect(user)
        client_socket.close()

def start_socket_server(host='0.0.0.0', port=5001):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    logger.info(f"Soket server start on {host}:{port}")
    
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()
