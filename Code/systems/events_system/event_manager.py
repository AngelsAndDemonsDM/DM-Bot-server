import asyncio
from inspect import signature
from typing import Any, Callable, Dict, List

from systems.decorators import global_class


@global_class
class EventManager:
    __slots__ = ['_register_defs']
    
    def __init__(self) -> None:
        self._register_defs: Dict[str, List[Callable[..., Any]]] = {}
        
    def register_event(self, event_name: str, func: Callable[..., Any]):
        if event_name not in self._register_defs:
            self._register_defs[event_name] = []
        self._register_defs[event_name].append(func)
    
    async def call_event(self, event_name: str, *args, **kwargs):
        handlers = self._register_defs.get(event_name, [])
        for handler in handlers:
            handler_signature = signature(handler)
            handler_kwargs = {k: v for k, v in kwargs.items() if k in handler_signature.parameters}
            
            if asyncio.iscoroutinefunction(handler):
                await handler(*args, **handler_kwargs)
            
            else:
                handler(*args, **handler_kwargs)
