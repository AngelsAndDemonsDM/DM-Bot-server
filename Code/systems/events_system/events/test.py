import logging

from systems.network.user_auth import UserAccess

logger = logging.getLogger("Test ev")

#TODO: Удалить после добавления первого нормального ивента

def test_echo(socket_user, socket_access: UserAccess, data): # Ивенты работают только по именованным аргументам! Если пользователь отправил data, то и в функцию прийдёт только data. socket_user, socket_access: UserAccess всегда можно поставить в функцию
    logger.info(f"Echo event called with user: {socket_user}, access: {socket_access._flags}, data: {data}")
    
test_echo.event_name = "echo" # Указание типа ивента
