from systems.entity_system import EntityFactory
from systems.events import EventManager
from systems.network import UserAuth, WebSocketConnectManager

entity_factory = EntityFactory()
event_manager = EventManager()
user_auth = UserAuth()
websocket_connect_manager = WebSocketConnectManager()
