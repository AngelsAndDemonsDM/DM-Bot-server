from DMBotNetwork import ClUnit, ServerDB, require_access


class UserServerModule:
    @staticmethod
    async def net_get_access(cl_unit: ClUnit, login: str):
        return await ServerDB.get_access(login)

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
