from plugin.event.Event import Event
from plugin.event import EventType

class UpgradeEvent(Event):
    event_id = EventType.UPGRADE_EVENT
    level = 0
    argv = {}
    
    def __init__(self, level, argv):
        self.level = level
        self.argv = argv
