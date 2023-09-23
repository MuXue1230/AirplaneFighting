from plugin.event.Event import Event
from plugin.event import EventType

class DoubleBulletEvent(Event):
    event_id = EventType.DOUBLE_BULLET_EVENT
    screen = None
    argv = {}
    
    def __init__(self, screen, argv):
        self.screen = screen
        self.argv = argv
