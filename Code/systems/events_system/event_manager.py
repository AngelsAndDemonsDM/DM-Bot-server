import asyncio
from inspect import signature
from typing import Any, Callable, Dict, List

from systems.misc import GlobalClass


class EventManager(GlobalClass):
    __slots__ = ['_open_events', '_protected_events', '_initialized']
    
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._open_events: Dict[str, List[Callable[..., Any]]] = {}
            self._protected_events: Dict[str, List[Callable[..., Any]]] = {}

    def _register_event(self, event_dict: Dict[str, List[Callable[..., Any]]], event_name: str, func: Callable[..., Any]) -> None:
        if event_name not in event_dict:
            event_dict[event_name] = []
        event_dict[event_name].append(func)

    def register_open_event(self, event_name: str, func: Callable[..., Any]) -> None:
        self._register_event(self._open_events, event_name, func)

    def register_protected_event(self, event_name: str, func: Callable[..., Any]) -> None:
        self._register_event(self._protected_events, event_name, func)

    async def _call_event(self, event_dict: Dict[str, List[Callable[..., Any]]], event_name: str, *args, **kwargs) -> None:
        handlers = event_dict.get(event_name, [])
        for handler in handlers:
            handler_signature = signature(handler)
            handler_kwargs = {k: v for k, v in kwargs.items() if k in handler_signature.parameters}
            if asyncio.iscoroutinefunction(handler):
                await handler(*args, **handler_kwargs)
            else:
                handler(*args, **handler_kwargs)

    async def call_open_event(self, event_name: str, *args, **kwargs) -> None:
        await self._call_event(self._open_events, event_name, *args, **kwargs)

    async def call_protected_event(self, event_name: str, *args, **kwargs) -> None:
        await self._call_event(self._protected_events, event_name, *args, **kwargs)

    async def call_all_event(self, event_name: str, *args, **kwargs) -> None:
        await self._call_event(self._open_events, event_name, *args, **kwargs)
        await self._call_event(self._protected_events, event_name, *args, **kwargs)
