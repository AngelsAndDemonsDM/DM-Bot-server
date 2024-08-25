from typing import Dict

from DMBotNetwork import Server


class UserModule(Server):
    async def net_delete_user(self, user_login: str, login: str):
        if not isinstance(login, str):
            return {"action": "log", "log_type": "error", "msg": "Invalid login type, expected string."}

        if not await self.check_access_login(user_login, ["delete_users"]):
            return {"action": "log", "log_type": "error", "msg": "Access denied: insufficient permissions to delete users."}
        
        if await self.db_delete_user(login):
            return {"action": "log", "log_type": "info", "msg": f"User '{login}' successfully deleted."}
        
        return {"action": "log", "log_type": "error", "msg": f"Failed to delete user '{login}'."}

    async def net_register_user(self, user_login: str, login: str, password: str):
        if not isinstance(login, str) or not isinstance(password, str):
            return {"action": "log", "log_type": "error", "msg": "Invalid login or password type, expected strings."}

        if not await self.check_access_login(user_login, ['create_users']):
            return {"action": "log", "log_type": "error", "msg": "Access denied: insufficient permissions to register users."}

        if await self.db_add_user(login, password):
            return {"action": "log", "log_type": "info", "msg": f"User '{login}' successfully registered."}
        
        return {"action": "log", "log_type": "error", "msg": f"Failed to register user '{login}'."}

    async def net_change_password(self, user_login: str, login: str, new_password: str):
        if not isinstance(login, str) or not isinstance(new_password, str):
            return {"action": "log", "log_type": "error", "msg": "Invalid login or new_password type, expected strings."}

        if not await self.check_access_login(user_login, ['change_password']):
            return {"action": "log", "log_type": "error", "msg": "Access denied: insufficient permissions to change password."}

        if await self.db_change_password(login, new_password):
            return {"action": "log", "log_type": "info", "msg": f"Password for user '{login}' successfully changed."}
        
        return {"action": "log", "log_type": "error", "msg": f"Failed to change password for user '{login}'."}

    async def net_change_access(self, user_login: str, login: str, new_access: Dict[str, bool]):
        if not isinstance(login, str) or not isinstance(new_access, dict):
            return {"action": "log", "log_type": "error", "msg": "Invalid login or new_access type, expected string and dict."}

        if not await self.check_access_login(user_login, ['change_access']):
            return {"action": "log", "log_type": "error", "msg": "Access denied: insufficient permissions to change access rights."}

        if await self.db_change_access(login, new_access):
            return {"action": "log", "log_type": "info", "msg": f"Access rights for user '{login}' successfully changed."}
        
        return {"action": "log", "log_type": "error", "msg": f"Failed to change access rights for user '{login}'."}
