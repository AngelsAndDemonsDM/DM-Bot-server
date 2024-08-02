from systems.network import (AccessError, SocketServerSystem, UserAccess,
                             UserAuth)


async def o_admin_delete_user_event(user_login: str, user_access: UserAccess, targer_login: str) -> None: 
    socket_server = SocketServerSystem()
    
    if not user_access.get_flag("delete_user"):
        raise AccessError()
    
    if not targer_login or not isinstance(targer_login, str):
        await socket_server.send_data(user_login, f"targer_login is req and must be str")
        return
    
    user_auth = UserAuth()
    await user_auth.delete_user(targer_login)
    await socket_server.send_data(user_login, "User deleted successfully")
