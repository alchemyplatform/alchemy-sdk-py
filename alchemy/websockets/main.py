from __future__ import annotations

from typing import List

from alchemy.provider import AlchemyWebsocketProvider
from alchemy.websockets.types import Listener


class AlchemyWebSocket:
    """
    The Websocket namespace contains all subscription related functions that
    allow you to subscribe to events and receive updates as they occur.

    Do not call this constructor directly. Instead, instantiate an Alchemy object
    with `alchemy = Alchemy('your_api_key')` and then access the websocket namespace
    via `alchemy.ws`.
    """

    def __init__(self, provider: AlchemyWebsocketProvider):
        self.provider = provider

    def on(self, event_name: str, listener: Listener):
        """
        Adds a listener to be triggered for each event.
        """
        event = self._resolve_ens_alchemy_event(event_name)
        return self.provider.on(event, listener)

    def once(self, event_name: str, listener: Listener):
        """
        Adds a listener to be triggered for only the next event,
        after which it will be removed
        """
        event = self._resolve_ens_alchemy_event(event_name)
        return self.provider.once(event, listener)

    def off(self, event_name: str, listener: Listener | None = None):
        """
        Removes the provided listener for the event. If no
        listener is provided, all listeners for the event will be removed.
        """
        event = self._resolve_ens_alchemy_event(event_name)
        return self.provider.off(event, listener)

    def remove_all_listeners(self, event_name: str | None = None):
        """
        Removes all listeners for the provided event. If no event
        is provided, all events and their listeners are removed.
        """
        event = self._resolve_ens_alchemy_event(event_name)
        return self.provider.remove_all_listeners(event)

    def listener_count(self, event_name: str | None = None) -> int:
        """
        Returns the number of listeners for the provided event. If
        no event is provided, the total number of listeners for all events is returned.
        """
        event = self._resolve_ens_alchemy_event(event_name)
        return self.provider.listener_count(event)

    def listeners(self, event_name: str | None = None) -> List[Listener]:
        """
        Returns the listeners for the provided event. If no event
        is provided, all listeners will be included.
        """
        event = self._resolve_ens_alchemy_event(event_name)
        return self.provider.listeners(event)

    @staticmethod
    def _resolve_ens_alchemy_event(event_name: str):
        """
        Converts ENS addresses in an Alchemy Event to the underlying resolved address.
        """
        return event_name
