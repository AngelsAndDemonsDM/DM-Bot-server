import asyncio
from typing import Any, Callable, Dict, List

from systems.singleton import singleton


@singleton
class EventManager:
    __slots__ = ['_register_defs']
    
    def __init__(self) -> None:
        self._register_defs: Dict[str, List[Callable[..., Any]]] = {}
        
    def register_event(self, event_name: str):
        def decorator(func: Callable[..., Any]):
            if event_name not in self._register_defs:
                self._register_defs[event_name] = []
            self._register_defs[event_name].append(func)
            return func
        
        return decorator
    
    async def call_event(self, event_name: str, *args, **kwargs):
        handlers = self._register_defs.get(event_name, [])
        results = []
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                result = await handler(*args, **kwargs)
            
            else:
                result = handler(*args, **kwargs)
            
            results.append(result)
        
        return results
