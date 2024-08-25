from DMBotNetwork import Server


class ChatModule(Server):
    async def net_ooc_chat(self, user_login: str, msg: str):
        if not isinstance(msg, str):
            return {"action": "log", "log_type": "error", "msg": "Invalid msg or type, expected string."}

        for login, writer in self._connects.items():
            await self.send_data(writer, {"action": "net", "type": "ooc_chat", "sender": user_login, "msg": msg})
        
        return
