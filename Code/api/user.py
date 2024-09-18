from DMBotNetwork import ClUnit, ServerDB, Server


class UserServerModule:
    @staticmethod
    async def net_get_access(cl_unit: ClUnit):
        return await ServerDB.get_access(cl_unit.login)

    @staticmethod
    async def net_get_all_users(cl_unit: ClUnit):
        # Блять. Нужны или произвольные запросы бд, или сделать получение существующих людей
        return Server._cl_units.keys()
