import pygame
from random import *
import plugin

def load_sound(file_path,eventBus: plugin.EventBus,argv):
    eventBus.addEvent(plugin.event.LoadEvent(None,plugin.event.AssetType.SOUND,file_path,argv))
    try:
        argv['logger'].debug('Loading file:',file_path)
        sound = pygame.mixer.Sound(file_path)
        return sound
    except:
        argv['logger'].error('Load failure:',file_path)
        return EmptySound()

def load_music(file_path,eventBus: plugin.EventBus,argv):
    eventBus.addEvent(plugin.event.LoadEvent(None,plugin.event.AssetType.MUSIC,file_path,argv))
    try:
        argv['logger'].debug('Loading file:',file_path)
        pygame.mixer.music.load(file_path)
    except:
        argv['logger'].error('Load failure:',file_path)
        pygame.mixer.music = EmptyMusic()

def load_image(file_path,eventBus: plugin.EventBus,argv):
    eventBus.addEvent(plugin.event.LoadEvent(None,plugin.event.AssetType.IMAGE,file_path,argv))
    try:
        argv['logger'].debug('Loading file:',file_path)
        import pygame
        image = pygame.image.load(file_path)
    except:
        argv['logger'].error('Load failure:',file_path)
        image = create_gray_rectangle()

    return image

def create_gray_rectangle():
    size = (50, 50)
    image = pygame.Surface(size)
    color = randint(0,255)
    green_color = (color, color, color)
    image.fill(green_color)
    return image

class EmptyMusic:
    def load(self, file_path):
        pass

    def play(self, loops=0, start=0.0):
        pass

    def pause(self):
        pass
    
    def unpause(self):
        pass

    def unload(self):
        pass

    def stop(self):
        pass

    def set_volume(self, volume):
        pass

class EmptySound:
    def __init__(self):
        pass

    def play(self, loops=0, maxtime=0, fade_ms=0):
        pass

    def stop(self):
        pass

    def fadeout(self, time):
        pass

    def set_volume(self, volume):
        pass

    def get_volume(self):
        return 0.0

    def get_num_channels(self):
        return 0

    def get_length(self):
        return 0

    def get_raw(self):
        return b''

    def get_num_channels(self):
        return 0

    def get_busy(self):
        return False

    def get_endevent(self):
        return 0

    def set_endevent(self, eventid):
        pass

    def fadeout(self, milliseconds):
        pass

    def set_volume(self, value):
        pass

    def get_volume(self):
        return 0.0

    def get_volume(self):
        return 0.0

    def get_length(self):
        return 0

    def get_num_channels(self):
        return 0

    def get_num_channels(self):
        return 0

    def get_num_channels(self):
        return 0

    def get_num_channels(self):
        return 0