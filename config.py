import lang
import pickle
import pygame

COLOR = {
    'BLACK':(0,0,0),
    'WHITE':(255,255,255),
    'GREEN':(0,255,0),
    'RED':(255,0,0),
}

class Config:
    def __init__(self):
        self.config_name = "conf.dat"
        self.assets_path = "assets/"
        self.log_to_file = False
        self.record = True
        self.demo = False
        self.uicheck = True

    def handleArgs(self,argv):
        for arg in argv:
            if arg[:2] == '--':
                if arg[2:] == 'config':
                    self.config_name = argv[argv.index(arg)+1]
                elif arg[2:] == 'assets':
                    self.assets_path = argv[argv.index(arg)+1]
                elif arg[2:] == 'log':
                    self.log_to_file = True
                elif arg[2:] == 'norecord':
                    self.record = False
                elif arg[2:] == 'demo':
                    self.demo = True
            elif arg[:1] == '-':
                if arg[1:] == 'C':
                    self.config_name = argv[argv.index(arg)+1]
                elif arg[1:] == 'A':
                    self.assets_path = argv[argv.index(arg)+1]
                elif arg[1:] == 'L':
                    self.log_to_file = True

    def init(self):
        with open(self.config_name,'rb') as f:
            self.app_info = pickle.load(f)
        self.settings = self.app_info['settings']
        self._lang = self.settings['language']
        self.language = lang.Language(self.assets_path,self._lang)
        self.font = self.language.get_font(self._lang)

    def get_screen_size(self):
        if self.settings['screen_width'] == 0 or self.demo:
            max = pygame.display.list_modes()[0][0]
            if 2160 < max:
                return 1750, 1200
            elif 1920 < max <= 2160:
                return 1400, 960
            elif max <= 1920:
                return 1050, 720
        else:
            try:
                return int(self.settings['screen_width']), int(self.settings['screen_height'])
            except:
                self.settings['screen_width'] = 0
                self.settings['screen_height'] = 0
                self.write(self)
                return self.get_screen_size()
    
    def reload(self):
        with open(self.config_name,'rb') as f:
            self.app_info = pickle.load(f)
    
    def write(self,conf):
        with open(conf.config_name,'wb') as f:
            pickle.dump(conf.app_info,f)
        self.reload()