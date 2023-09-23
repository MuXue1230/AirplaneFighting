import pygame
import empty
import lang
import pickle
from gui import GUI
from gui.components import Thing, Button, Label

class PageUI(GUI):
    def __init__(self,screen:pygame.surface.Surface,swidth:int,sheight:int,sign:str,_lang:lang.Language,next_ui:GUI,asset_path,conf_name,eventBus,arg,x=None,**argv):
        super().__init__(screen,swidth,sheight)
        temp = empty.load_image(asset_path+'images/title.png',eventBus,arg).convert_alpha()
        temp = pygame.transform.scale(temp,(screen.get_width(),temp.get_height()))
        self.til_img = Thing(screen,temp,('free',0,0))
        if x:
            self.back_btn = Button(screen,x,empty.load_image(asset_path+'images/back.png',eventBus,arg).convert_alpha(),empty.load_image(asset_path+'images/back_over.png',eventBus,arg).convert_alpha(), \
                                      empty.load_image(asset_path+'images/back_pressed.png',eventBus,arg).convert_alpha(), self._over,('free',40,40),next_ui=next_ui,**argv)
        else:
            self.back_btn = Button(screen,self._press,empty.load_image(asset_path+'images/back.png',eventBus,arg).convert_alpha(),empty.load_image(asset_path+'images/back_over.png',eventBus,arg).convert_alpha(), \
                                      empty.load_image(asset_path+'images/back_pressed.png',eventBus,arg).convert_alpha(), self._over,('free',40,40),next_ui=next_ui)
        self.title_txt = Label(screen,sign,_lang,60,('center_obj',0,0),father_obj=self.til_img)
        with open(conf_name, 'rb') as conf:
            self.app_info = pickle.load(conf)
        if self.app_info['settings']['mix']:
            self.button_over_sound = empty.load_sound(asset_path+"sound/button.wav",eventBus,arg)
            self.button_over_sound.set_volume(0.3)
            self.button_click_sound = empty.load_sound(asset_path+"sound/button_click.wav",eventBus,arg)
            self.button_click_sound.set_volume(0.2)
        self.background = empty.load_image(asset_path+'images/settings.png',eventBus,arg).convert()
        self.background.set_alpha(126)
        self.background = pygame.transform.scale(self.background,screen.get_size())
        super().add_thing(self.til_img)
        super().add_button(self.back_btn)
        super().add_label(self.title_txt)
    
    def _over(self,_in):
        if self.app_info['settings']['mix']:
            self.button_over_sound.play()
    
    def _press(self,_in):
        if self.app_info['settings']['mix']:
            self.button_click_sound.play()
        self.close()
        _in['next_ui'].open()
    
    def draw(self):
        self.screen.blit(self.background,(0,0))
        last = None
        wait = None
        wait_pre = None
        for _id in self.things.keys():
            _object = self.things[_id]
            if 'label' in _id:
                _object.draw(last)
            elif 'button' in _id:
                _object[0].draw(last)
            elif 'pthing' in _id:
                if _object.is_listing:
                    wait = _object
                    wait_pre = last
                else:
                    _object.draw(last)
            elif 'thing' in _id:
                _object.draw(last)
            last = _object
        if wait:
            wait.draw(wait_pre)
    
    def add_thing(self,pThing):
        for _id in range(1,11):
            if 'pthing'+str(_id) in self.things.keys():
                if _id == 10:
                    raise SyntaxError("Don't put mor than 10 options in 1 UI.")
                continue
            else:
                self.things['pthing'+str(_id)] = pThing
                break
    
    def check(self):
        super().check()
        for _id in self.things.keys():
            _object = self.things[_id]
            if 'pthing' in _id:
                if _object.is_listing:
                    return _object.check()
        for _id in self.things.keys():
            _object = self.things[_id]
            if 'pthing' in _id:
                _object.check()