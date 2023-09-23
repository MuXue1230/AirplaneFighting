from plugin.event.Event import Event
from plugin.event import EventType

class PlaneSpawnEvent(Event):
    event_id = EventType.PLANE_SPAWN_EVENT
    plane_obj = None
    argv = {}
    
    def __init__(self, plane_obj, argv):
        self.plane_obj = plane_obj
        self.argv = argv
