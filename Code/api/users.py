from DMBotNetwork import Server


class UserServerModule(Server):
    
    async def net_register_user(self, user_login: str):
        await self.db_add_user()