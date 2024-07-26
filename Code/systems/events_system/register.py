import logging

from systems.events_system import events
from systems.events_system.event_manager import EventManager

logger = logging.getLogger("Event register")

def register_ev():
    ev_manager = EventManager.get_instance()
    
    event_names = events.__all__
    
    for name in event_names:
        handler = getattr(events, name)
        
        if callable(handler) and hasattr(handler, 'event_name'):
            event_name = handler.event_name
            ev_manager.register_event(event_name, handler)
            logger.info(f"Registered event '{event_name}' with handler {handler.__name__}")

