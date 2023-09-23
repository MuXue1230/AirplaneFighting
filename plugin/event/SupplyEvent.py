from plugin.event.Event import Event
from plugin.event import EventType

class SupplyEvent(Event):
    event_id = EventType.SUPPLY_EVENT
    screen = None
    argv = {}
    
    def __init__(self, screen, argv):
        self.screen = screen
        self.argv = argv
