import logging
from systems.events.event_manager import EventManager
from systems.network.user_auth import UserAccess
ev_manager = EventManager()
logger = logging.getLogger("Test ev")

@ev_manager.register_event("echo")
def test_echo(socket_user, socket_access: UserAccess, data):
    logger.info(socket_user, socket_access._flags, data)
    return
