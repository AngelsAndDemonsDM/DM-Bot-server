from systems.network import (AccessError, SocketServerSystem, UserAccess,
                             UserAuth)


async def o_admin_change_access_event(user_login: str, user_access: UserAccess, targer_login: str, new_access: dict) -> None: 
    socket_server = SocketServerSystem()
    
    if not user_access.get_flag("change_access"):
        raise AccessError()
    
    if not targer_login or not isinstance(targer_login, str):
        await socket_server.send_data(user_login, f"targer_login is req and must be str")
        return
        
    if not new_access or not isinstance(new_access, dict):
        await socket_server.send_data(user_login, f"new_access is req and must be Dict[str, bool]")
        return
    
    user_auth = UserAuth()
    target_access = await user_auth.get_access_by_login(targer_login)
    
    for access, value in new_access.items():
        if not user_access.get_flag(access):
            await socket_server.send_data(user_login, f"Cannot grant access '{access}' which you don't have")
            return

        else:
            target_access.set_flag(access, value)

    await user_auth.change_access(targer_login, target_access)
    await socket_server.send_data(user_login, "Access changed successfully")