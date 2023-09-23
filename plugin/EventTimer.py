from plugin.event import Event
from plugin.event import EventType
from plugin import TimerUnit
from plugin import Errors
from plugin import EventBus
from plugin import Listener

import threading
import time

class EventTimer(Listener):
    def __init__(self, event: Event, eventBus: EventBus, time: tuple, loop: int):
        self.event = event
        self.eventBus = eventBus
        self.time = time[0] * self.__unit(time[1])
        self.loop = loop
        self.sign = False
        self.stop_sign = False
        self.thread = threading.Thread(target=self.__wait)
        self.eventBus.addListener(EventType.EVENT,self)
    
    def __unit(self, unit:int):
        if unit == TimerUnit.MS:
            return 1
        elif unit == TimerUnit.SEC:
            return 1000
        elif unit == TimerUnit.MIN:
            return 60000
        elif unit == TimerUnit.H:
            return 3600000
        raise Errors.TimerUnitError('You cannot use the unit which id is '+str(unit)+'.')
    
    def __wait(self):
        i = 0
        while not i == self.loop:
            time.sleep(self.time/1000)
            if self.stop_sign:
                break
            self.sign = True
            i += 1
        self.thread = threading.Thread(target=self.__wait)
    
    def start(self):
        self.stop_sign = False
        if not self.thread.is_alive():
            self.thread.start()
    
    def stop(self):
        self.stop_sign = True

    def handle(self,event):
        if self.sign:
            self.eventBus.addEvent(self.event)
            self.sign = False
