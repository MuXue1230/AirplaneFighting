from plugin.event import EventType

class EventBus:
    handleFunction = []
    eventListener = {}

    def __init__(self):
        self.eventListener['event'] = []

        self.eventListener['pre_init'] = []
        self.eventListener['init'] = []
        self.eventListener['exit'] = []
        self.eventListener['reload'] = []

        self.eventListener['load'] = []
        self.eventListener['unload'] = []
        
        self.eventListener['gui_open'] = []
        self.eventListener['gui_close'] = []
        self.eventListener['plane_crash'] = []
        self.eventListener['plane_spawn'] = []
        self.eventListener['bomb'] = []
        self.eventListener['supply'] = []
        self.eventListener['no_hit'] = []
        self.eventListener['double_bullet'] = []
        self.eventListener['upgrade'] = []

        self.eventListener['plugin_load'] = []
        self.eventListener['plugin_init'] = []
        self.eventListener['plugin_error'] = []

    def addListener(self, event_type: int, listener):
        if event_type == EventType.EVENT:
            self.eventListener['event'].append(listener)
        elif event_type == EventType.PRE_INIT_EVENT:
            self.eventListener['pre_init'].append(listener)
        elif event_type == EventType.INIT_EVENT:
            self.eventListener['init'].append(listener)
        elif event_type == EventType.EXIT_EVENT:
            self.eventListener['exit'].append(listener)
        elif event_type == EventType.RELOAD_EVENT:
            self.eventListener['reload'].append(listener)
        elif event_type == EventType.LOAD_EVENT:
            self.eventListener['load'].append(listener)
        elif event_type == EventType.UNLOAD_EVENT:
            self.eventListener['unload'].append(listener)
        elif event_type == EventType.GUI_OPEN_EVENT:
            self.eventListener['gui_open'].append(listener)
        elif event_type == EventType.GUI_CLOSE_EVENT:
            self.eventListener['gui_close'].append(listener)
        elif event_type == EventType.PLANE_CRASH_EVENT:
            self.eventListener['plane_crash'].append(listener)
        elif event_type == EventType.PLANE_SPAWN_EVENT:
            self.eventListener['plane_spawn'].append(listener)
        elif event_type == EventType.BOMB_EVENT:
            self.eventListener['bomb'].append(listener)
        elif event_type == EventType.SUPPLY_EVENT:
            self.eventListener['supply'].append(listener)
        elif event_type == EventType.NO_HIT_EVENT:
            self.eventListener['no_hit'].append(listener)
        elif event_type == EventType.DOUBLE_BULLET_EVENT:
            self.eventListener['double_bullet'].append(listener)
        elif event_type == EventType.UPGRADE_EVENT:
            self.eventListener['upgrade'].append(listener)

    def addHandler(self, handler):
        self.handleFunction.append(handler)

    def addEvent(self, event):
        if event.event_id == EventType.EVENT:
            for listener in self.eventListener['event']:
                listener.handle(event)
        elif event.event_id == EventType.PRE_INIT_EVENT:
            for listener in self.eventListener['pre_init']:
                listener.handle(event)
        elif event.event_id == EventType.INIT_EVENT:
            for listener in self.eventListener['init']:
                listener.handle(event)
        elif event.event_id == EventType.EXIT_EVENT:
            for listener in self.eventListener['exit']:
                listener.handle(event)
        elif event.event_id == EventType.RELOAD_EVENT:
            for listener in self.eventListener['reload']:
                listener.handle(event)
        elif event.event_id == EventType.LOAD_EVENT:
            for listener in self.eventListener['load']:
                listener.handle(event)
        elif event.event_id == EventType.UNLOAD_EVENT:
            for listener in self.eventListener['unload']:
                listener.handle(event)
        elif event.event_id == EventType.GUI_OPEN_EVENT:
            for listener in self.eventListener['gui_open']:
                listener.handle(event)
        elif event.event_id == EventType.GUI_CLOSE_EVENT:
            for listener in self.eventListener['gui_close']:
                listener.handle(event)
        elif event.event_id == EventType.PLANE_CRASH_EVENT:
            for listener in self.eventListener['plane_crash']:
                listener.handle(event)
        elif event.event_id == EventType.PLANE_SPAWN_EVENT:
            for listener in self.eventListener['plane_spawn']:
                listener.handle(event)
        elif event.event_id == EventType.BOMB_EVENT:
            for listener in self.eventListener['bomb']:
                listener.handle(event)
        elif event.event_id == EventType.SUPPLY_EVENT:
            for listener in self.eventListener['supply']:
                listener.handle(event)
        elif event.event_id == EventType.NO_HIT_EVENT:
            for listener in self.eventListener['no_hit']:
                listener.handle(event)
        elif event.event_id == EventType.DOUBLE_BULLET_EVENT:
            for listener in self.eventListener['double_bullet']:
                listener.handle(event)
        elif event.event_id == EventType.UPGRADE_EVENT:
            for listener in self.eventListener['upgrade']:
                listener.handle(event)