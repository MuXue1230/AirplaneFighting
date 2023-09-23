from plugin.event.Event import Event
from plugin.event import EventType

class UnloadEvent(Event):
    event_id = EventType.UNLOAD_EVENT
    asset_id = ''
    argv = {}
    
    def __init__(self, asset_id, asset_type, asset_path, argv):
        self.asset_id = asset_id
        self.argv = argv
