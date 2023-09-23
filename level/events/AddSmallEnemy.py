from plugin.event import Event, EventType

class AddSmallEnemy(Event):
    event_id = EventType.BOMB_EVENT
    screen = None
    argv = {}
    
    def __init__(self, screen, argv):
        self.screen = screen
        self.argv = argv