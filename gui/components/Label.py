import pygame
import lang
from gui.components.Thing import Thing

class Label(Thing):
    def __init__(self, screen:pygame.surface.Surface, sign:str, _lang:lang.Language, \
                    _size:int=48, pos:tuple=('under',0,10), father:pygame.surface.Surface|None=None, \
                    father_obj=None, color=(0,0,0)):
        self._size = _size
        self.font = pygame.font.Font(_lang.get_font(_lang._lang), self._size)
        super().__init__(screen,self.font.render(_lang.get(sign,_lang._lang), True, color),pos,father,father_obj)
        self._lang = _lang
        self.sign = sign
        self.color = color
    
    def set_text(self,sign:str):
        self.sign = sign
        self.img = self.font.render(self._lang.get(self.sign,self._lang._lang), True, self.color)
        self.rect = self.img.get_rect()
    
    def set_size(self,_size:int):
        self._size = _size
        self.font = pygame.font.Font(self._lang.get_font(self._lang._lang), self._size)
        self.img = self.font.render(self._lang.get(self.sign,self._lang._lang), True, self.color)
        self.rect = self.img.get_rect()
    
    def setFontColor(self,color):
        self.img = self.font.render(self._lang.get(self.sign,self._lang._lang), True, color)

    def draw(self,pre:object):
        super().draw(pre)

        self.screen.blit(self.img, self.rect)