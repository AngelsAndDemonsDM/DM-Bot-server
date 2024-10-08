from DMBotNetwork import ClUnit, Server, ServerDB, require_access


class UserServerModule:
    @staticmethod
    async def net_get_access(cl_unit: ClUnit, login: str):
        access = await ServerDB.get_access(login)
        base_access = ServerDB.get_base_access()
        
        for key, value in base_access.items():
            if key not in access: # type: ignore
                access[key] = value # type: ignore
        
        return access

    @staticmethod
    async def net_get_all_users(cl_unit: ClUnit):
        return await ServerDB.get_all_users()

    @require_access("change_access")
    @staticmethod
    async def net_change_access(cl_unit: ClUnit, login: str, changes: dict):
        cur_target_access = await ServerDB.get_access(login)
        cl_unit_access = await ServerDB.get_access(cl_unit.login)

        if cur_target_access is None or cl_unit_access is None:
            return

        need_access = [k for k in changes.keys()]
        if ServerDB.check_access(cl_unit_access, need_access):
            cur_target_access.update(changes)
            await ServerDB.change_user_access(login, cur_target_access)
            return "Sucess"

        return "Insufficient access"

    @require_access("change_server_settings")
    @staticmethod
    async def net_get_server_settings(cl_unit: ClUnit):
        return {
            "timeout": Server.get_timeout(),
            "max_players": Server.get_max_players(),
            "allow_registration": Server.get_allow_registration(),
        }

    @require_access("change_server_settings")
    @staticmethod
    async def net_change_server_settings(
        cl_unit: ClUnit, type: str, value: bool | float | int
    ):
        if type == "timeout":
            if isinstance(value, float):
                Server.set_timeout(value)

            else:
                return "Timeout value must be of type float."

        elif type == "max_players":
            if isinstance(value, int) and value >= -1:
                Server.set_max_players(value)

            else:
                return (
                    "Max players value must be an integer greater than or equal to -1."
                )

        elif type == "allow_registration":
            if isinstance(value, bool):
                Server.set_allow_registration(value)

            else:
                return "Allow registration value must be of type bool."

        else:
            return f"Unknown setting type: {type}"

    @require_access("delete_users")
    @staticmethod
    async def net_delete_user(cl_unit: ClUnit, login: str):
        if login == "owner":
            return "Insufficient access"

        await Server.remove_user(login)
        return "Sucess"

    @require_access("create_users")
    @staticmethod
    async def net_create_user(cl_unit: ClUnit, login: str, password: str):
        try:
            await ServerDB.add_user(login, password)

        except Exception as err:
            return str(err)

        return "Sucess"
