from systems.entity_system import EntityFactory
from systems.events import EventManager
from systems.network import WebSocketConnectManager

entity_factory = EntityFactory()
event_manager = EventManager()
websocket_connect_manager = WebSocketConnectManager()
