import importlib.util
import logging
import re
from pathlib import Path

from root_path import ROOT_PATH
from systems.events_system.event_manager import EventManager

logger = logging.getLogger("Event manager")

def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def register_events() -> None:
    logger.info("Start register events")
    
    ev_manager = EventManager()
    event_name_pattern = re.compile(r"^(?:o_|p_)?(.+?)_event$") 

    events_directory = Path(ROOT_PATH)
    events_directory = events_directory / "Code" / "systems" / "events_system" / "events"
    for file_path in events_directory.rglob("*.py"):
        module_name = file_path.stem  # Имя модуля без расширения .py
        if module_name == "__init__":
            continue # Иначе будет регестрация по 15 раз одного и того же
        
        module = import_module_from_file(module_name, file_path)

        for name in dir(module):
            handler = getattr(module, name)
            if callable(handler):
                match = event_name_pattern.match(name)
                if match:
                    event_name = match.group(1)  # Извлекаем имя события без модификаторов и суффиксов
                    if name.startswith("o_"):
                        ev_manager.register_open_event(event_name, handler)
                        logger.info(f"Registered open event '{event_name}' with handler '{handler.__name__}'")
                    
                    elif name.startswith("p_"):
                        ev_manager.register_protected_event(event_name, handler)
                        logger.info(f"Registered protected event '{event_name}' with handler '{handler.__name__}'")
    
    logger.info("End register events")