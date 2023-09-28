from plugin.event import EventStatus
from plugin.event import EventType

class Event:
    event_id = EventType.EVENT
    event_status = EventStatus.NOTHING
    argv = {}
    
    def __init__(self, argv):
        self.argv = argv
    
    def getStatus(self):
        return self.event_status
    
    def setStatus(self, status:int):
        self.event_status = status