import pygame
import empty
import lang
import pickle
from gui.components.PageButton import PageButton

class ButtonList:
    def __init__(self,screen:pygame.surface.Surface,num:int,_lang:lang.Language,eventBus,arg,sign:str,pos:tuple=(0,0),_type:str='bool',asset_path="",conf_name="conf.data",x=None):
        self.chooses = []
        self.button_over_sound = empty.load_sound(asset_path+"sound/button.wav",eventBus,arg)
        self.button_over_sound.set_volume(0.3)
        self.button_click_sound = empty.load_sound(asset_path+"sound/button_click.wav",eventBus,arg)
        self.button_click_sound.set_volume(0.2)
        self.click = False
        self._type = _type
        self.sign = sign
        self._lang = _lang
        self.conf_name = conf_name
        self.x = x
        self.pos = pos
        for i in range(1,num+1):
            self.list2 = empty.load_image(asset_path+'images/choose_listing2.png',eventBus,arg).convert_alpha()
            self.list3 = empty.load_image(asset_path+'images/choose_listing3.png',eventBus,arg).convert_alpha()
            if i == num:
                self.chooses.append(PageButton(screen,self.sign+str(i),self._lang,None,self.list3,self.list3,self.list3,(self.pos[0],self.pos[1]+(self.list2.get_height())*num-1)))
            else:
                self.chooses.append(PageButton(screen,self.sign+str(i),self._lang,None,self.list2,self.list2,self.list2,(self.pos[0],self.pos[1]+(self.list2.get_height())*i-1)))
    def draw(self):
        for btn in self.chooses:
            btn.draw()
    def check(self):
        if pygame.mouse.get_pressed()[0]:
            self.click = True
        elif not pygame.mouse.get_pressed()[0] and self.click:
            pos = pygame.mouse.get_pos()
            self.click = False
            for btn in self.chooses:
                if btn.rect.left < pos[0] < btn.rect.right and \
                    btn.rect.top < pos[1] < btn.rect.bottom:
                    if self._type == 'bool':
                        with open(self.x,'rb') as conf:
                            sets = pickle.loads(conf.read())
                        if btn.sign[-1:] == '1':
                            sets['settings'][self.sign[16:-1]] = True
                        else:
                            sets['settings'][self.sign[16:-1]] = False
                        with open(self.x,'wb') as conf:
                            conf.write(pickle.dumps(sets))
                    else:
                        with open(self.x,'rb') as conf:
                            sets = pickle.loads(conf.read())
                        try:
                            sets['settings'][self.sign[16:-1]] = int(self._lang.get(btn.sign+'.id',self._lang._lang))
                        except:
                            sets['settings'][self.sign[16:-1]] = self._lang.get(btn.sign+'.id',self._lang._lang)
                        with open(self.x,'wb') as conf:
                            conf.write(pickle.dumps(sets))
                    return False
        return True