from plugin.event.Event import Event
from plugin.event import EventType

class PreInitEvent(Event):
    event_id = EventType.PRE_INIT_EVENT
    screen = None
    argv = {}
    
    def __init__(self, screen, argv):
        self.screen = screen
        self.argv = argv
