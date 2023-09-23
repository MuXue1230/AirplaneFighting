from plugin.event.Event import Event
from plugin.event import EventType

class ReloadEvent(Event):
    event_id = EventType.RELOAD_EVENT
    
    def __init__(self):
        pass
