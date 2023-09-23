from plugin.event.Event import Event
from plugin.event import EventType
from plugin.event import AssetType

class LoadEvent(Event):
    event_id = EventType.LOAD_EVENT
    asset_id = ''
    asset_type = AssetType.UNKNOW
    asset_path = ''
    argv = {}
    
    def __init__(self, asset_id, asset_type, asset_path, argv):
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.asset_path = asset_path
        self.argv = argv
