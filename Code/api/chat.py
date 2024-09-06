from DMBotNetwork import ClientUnit, Server


class ChatModule(Server):
    async def net_ooc_chat(self, cl_unit: ClientUnit, msg: str):
        await Server.broadcast("req_net", "ooc_chat", sender=cl_unit.login, msg=msg)
