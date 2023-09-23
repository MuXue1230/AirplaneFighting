import pygame
import lang
import empty
import pickle
from gui.components.PageButton import PageButton
from gui.components.ButtonList import ButtonList
from gui.components.Thing import Thing

class PageThing(Thing):
    def __init__(self, screen: pygame.surface.Surface, sign:str, _lang:lang.Language,eventBus,arg,pos=1,_type='bool',choose=1,max=2,asset_path="",conf_name="conf.data",x=None,jump_to=None,**argv):
        self.font = pygame.font.Font(_lang.get_font(_lang._lang),36)
        if pos == 1:
            super().__init__(screen, self.font.render(_lang.get(sign,_lang._lang), True, (0,0,0)), ('free', 50, 150), None, None)
        else:
            super().__init__(screen, self.font.render(_lang.get(sign,_lang._lang), True, (0,0,0)), ('under', 0, 20), None, None)
        self.sign = sign
        self._lang = _lang
        self._type = _type
        self.is_list = False
        self.click = False
        self._over = False
        self.choose = int(choose)
        self.jump_to = jump_to
        self.argv = argv
        if not x:
            x = conf_name
        with open(conf_name, 'rb') as conf:
            self.app_info = pickle.load(conf)
        if self.app_info['settings']['mix']:
            self.button_over_sound = empty.load_sound(asset_path+"sound/button.wav",eventBus,arg)
            self.button_over_sound.set_volume(0.3)
            self.button_click_sound = empty.load_sound(asset_path+"sound/button_click.wav",eventBus,arg)
            self.button_click_sound.set_volume(0.2)
        self.is_listing = False
        self.moved = False
        if self._type == 'bool' or self._type == 'choose':
            self.nor = empty.load_image(asset_path+'images/choose.png',eventBus,arg).convert_alpha()
            self.over = empty.load_image(asset_path+'images/choose_over.png',eventBus,arg).convert_alpha()
            self.pressed = empty.load_image(asset_path+'images/choose_pressed.png',eventBus,arg).convert_alpha()
            self.button = PageButton(screen,self.sign[:-1]+str(self.choose),self._lang,None,self.nor,self.over,self.pressed,(screen.get_width()-325,0))
            self.list = ButtonList(screen, max, _lang,eventBus,arg, sign[:-1],(screen.get_width()-325,0),self._type,asset_path=asset_path,conf_name=conf_name,x=x)
            self.list1 = empty.load_image(asset_path+'images/choose_listing1.png',eventBus,arg).convert_alpha()
        elif self._type == 'enter':
            self.nor = empty.load_image(asset_path+'images/enter.png',eventBus,arg).convert_alpha()
            self.over = empty.load_image(asset_path+'images/enter_over.png',eventBus,arg).convert_alpha()
            self.pressed = empty.load_image(asset_path+'images/enter_pressed.png',eventBus,arg).convert_alpha()
            self.button = PageButton(screen,self.sign[:-1]+'1',self._lang,jump_to,self.nor,self.over,self.pressed,(screen.get_width()-325,0))

    def setFontColor(self,color):
        self.img = self.font.render(self._lang.get(self.sign,self._lang._lang), True, color)

    def draw(self, pre: Thing):
        m_pos,x,y = self.pos
        if m_pos == 'under':
            self.rect.left, self.rect.top = \
                                pre.rect.left + x, \
                                pre.rect.bottom + y
        elif m_pos == 'over':
            self.rect.left, self.rect.bottom = \
                                pre.rect.left + x, \
                                pre.rect.top + y
        elif m_pos == 'free':
            self.rect.left, self.rect.top = x, y
        elif m_pos == 'center':
            self.rect.center = self.father.get_rect().center
            self.rect.left -=x
            self.rect.top -= y
        elif m_pos == 'center_obj':
            self.rect.center = self.father_obj.rect.center
            self.rect.left -=x
            self.rect.top -= y
        if self.pos[0] != 'free':
            pygame.draw.line(self.screen,(255, 215, 100),(0,pre.button.rect.bottom + 10),(self.screen.get_width(),pre.button.rect.bottom + 10))
            self.button.pos = ('free',self.button.pos[1],pre.button.rect.bottom+20)
            self.rect.center = (self.rect.center[0],self.button.rect.center[1])
        else:
            self.button.pos = ('free',self.button.pos[1],self.rect.top)
        self.rect.center = (self.rect.center[0],self.button.rect.center[1])
        self.screen.blit(self.img, self.rect)
        self.button.draw()
        if self._type == 'bool' or self._type == 'choose':
            if self.is_listing:
                if not self.moved:
                    self.moved = True
                    for btn in self.list.chooses:
                        btn.pos = ('free',btn.pos[1],btn.pos[2]+self.rect.top)
                self.list.draw()

    def check(self):
        if pygame.mouse.get_pressed()[0]:
            self.click = True
            temp = True
            pos = pygame.mouse.get_pos()
            if self.button.rect.left < pos[0] < self.button.rect.right and \
                self.button.rect.top < pos[1] < self.button.rect.bottom:
                if (not self.is_listing) or self._type == 'enter':
                    self.button.img = self.button.img_click
            else:
                if self._type != 'enter':
                    for btn in self.list.chooses:
                        if btn.rect.left < pos[0] < btn.rect.right and \
                            btn.rect.top < pos[1] < btn.rect.bottom:
                            temp = False
            if ((self.is_listing and temp) or self._type == 'enter') and self.app_info['settings']['mix']:
                self.is_listing = False
                self.button_click_sound.play()
                self.button.img = self.button.img_nor
                self.button.rect = self.button.rect_nor
                return False
        elif not pygame.mouse.get_pressed()[0] and not self.click:
            pos = pygame.mouse.get_pos()
            if self.button.rect.left < pos[0] < self.button.rect.right and \
                self.button.rect.top < pos[1] < self.button.rect.bottom:
                if (not self.is_listing) or self._type == 'enter':
                    self.button.img = self.button.img_over
                    self.button.rect = self.button.rect_over
                if not self._over:
                    if self.app_info['settings']['mix']:
                        self.button_over_sound.play()
                    self._over = True
            else:
                if (not self.is_listing) or self._type == 'enter':
                    self.button.img = self.button.img_nor
                    self.button.rect = self.button.rect_nor
                self._over = False
        elif not pygame.mouse.get_pressed()[0] and self.click:
            self.click = False
            pos = pygame.mouse.get_pos()
            if self.button.rect.left < pos[0] < self.button.rect.right and \
                self.button.rect.top < pos[1] < self.button.rect.bottom:
                if self.app_info['settings']['mix']:
                    self.button_click_sound.play()
                if self.is_listing or self._type == 'enter':
                    self.button.img = self.button.img
                    self.is_listing = False
                if self._type == 'enter':
                    self.jump_to(**self.argv)
                else:
                    self.button.img = self.list1
                    self.is_listing = True
        if self.is_listing:
            self.is_listing = self.list.check()
            if not self.is_listing:
                return True
            return False