import logging
import re

from systems.events_system import events
from systems.events_system.event_manager import EventManager

logger = logging.getLogger("Event manager")

def register_events() -> None:
    logger.info("Start register events")
    
    ev_manager = EventManager()
    event_names = events.__all__
    
    event_name_pattern = re.compile(r"(.+)_event$")
    
    for name in event_names:
        handler = getattr(events, name)
        
        if callable(handler):
            match = event_name_pattern.match(name)
            if match:
                event_name = match.group(1)
                ev_manager.register_event(event_name, handler)
                logger.info(f"Registered event '{event_name}' with handler {handler.__name__}")
    
    logger.info("End register events")
