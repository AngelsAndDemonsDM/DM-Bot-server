from DMBotNetwork import ClUnit, ServerDB


class UserServerModule:
    @staticmethod
    async def net_get_access(cl_unit: ClUnit, login: str):
        return await ServerDB.get_access(login)

    @staticmethod
    async def net_get_all_users(cl_unit: ClUnit):
        return await ServerDB.get_all_users()
