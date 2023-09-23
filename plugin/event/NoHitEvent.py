from plugin.event.Event import Event
from plugin.event import EventType

class NoHitEvent(Event):
    event_id = EventType.NO_HIT_EVENT
    screen = None
    argv = {}
    
    def __init__(self, screen, argv):
        self.screen = screen
        self.argv = argv
