import logging

from systems.network import SocketConnectManager, UserAccess

logger = logging.getLogger("Test ev")

#TODO: Удалить после добавления первого нормального ивента

async def echo_event(socket_user, socket_access: UserAccess, data): # Ивенты работают только по именованным аргументам! Если пользователь отправил data, то и в функцию прийдёт только data. socket_user, socket_access: UserAccess всегда можно поставить в функцию
    logger.info(f"Echo event called with user: {socket_user}, access: {socket_access._flags}, data: {data}")
    
    sock_con_man:SocketConnectManager = SocketConnectManager()
    if data == "fuck u":
        await sock_con_man.send_data(socket_user, {"ev_type": "echo", "data": "fuck u 2"})
