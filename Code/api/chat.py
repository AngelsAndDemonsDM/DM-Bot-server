from typing import Dict, Optional

from DMBotNetwork import ClUnit, Server, ServerDB


class ChatServerModule:
    @staticmethod
    async def net_send_message(
        cl_unit: ClUnit, message: str, message_type: str
    ) -> None:
        cl_to_send: Optional[Dict[str, ClUnit]] = None

        if message_type == "admin":
            if not await ServerDB.check_access_login(
                cl_unit.login, ["access_admin_chat"]
            ):
                return

            cl_to_send = await Server.get_connects_with_access("access_admin_chat")

        await Server.broadcast(
            "req_net_func",
            cl_to_send,
            "get_chat_message",
            message=message,
            message_type=message_type,
            sender=cl_unit.login,
        )
