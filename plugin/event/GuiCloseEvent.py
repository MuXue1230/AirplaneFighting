from plugin.event.Event import Event
from plugin.event import EventType

class GuiCloseEvent(Event):
    event_id = EventType.GUI_CLOSE_EVENT
    gui_obj = None
    argv = {}
    
    def __init__(self, gui_obj, argv):
        self.gui_obj = gui_obj
        self.argv = argv
