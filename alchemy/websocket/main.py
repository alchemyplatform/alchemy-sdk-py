from __future__ import annotations

from typing import List, Callable

from alchemy.provider import AlchemyWebsocketProvider, Subscription
from alchemy.websocket.types import EventType


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

    def on(self, event: EventType, listener: Callable) -> Subscription:
        """
        Adds a listener to be triggered for each event.
        """
        # event = self._resolve_ens_alchemy_event(event_name)
        return self.provider.subscribe(event, listener)

    def once(self, event: EventType, listener: Callable):
        """
        Adds a listener to be triggered for only the next event,
        after which it will be removed
        """
        # event = self._resolve_ens_alchemy_event(event_name)
        return self.provider.once(event, listener)

    def off_all_events(self):
        """
        Unsubscribes from all events.
        """
        return self.provider.unsubscribe_all()

    # @staticmethod
    # def _resolve_ens_alchemy_event(event_name: str):
    #     """
    #     Converts ENS addresses in an Alchemy Event to the underlying resolved address.
    #     """
    #     return event_name
