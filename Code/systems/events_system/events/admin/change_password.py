from systems.network import SocketServerSystem, UserAuth


async def o_admin_change_password_event(user_login: str, new_password: str) -> None: 
    socket_server = SocketServerSystem()
    
    if not new_password or not isinstance(new_password, str):
        await socket_server.send_data(user_login, f"new_password is req and must be str")
        return

    user_auth = UserAuth()
    await user_auth.change_password(user_login, new_password)
    return socket_server.send_data(user_login, "Password changed successfully")
