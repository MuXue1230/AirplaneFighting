import pygame
import lang
from gui.components.Button import Button

class PageButton(Button):
    def __init__(self, screen:pygame.surface.Surface, sign:str, _lang:lang.Language, press, img_nor, img_over, img_click, \
                 pos:tuple=(0,10)):
        super().__init__(screen,press,img_nor,img_over,img_click,None,('free',*pos),None,None)
        self._lang = _lang
        self.sign = sign
        self.is_clicked = False

    def draw(self):
        super().draw(None)
        
        if 'lang' in self.sign:font = pygame.font.Font(self._lang.get_font(self._lang.get(self.sign+'.id',None)),36)
        else:font = pygame.font.Font(self._lang.get_font(self._lang._lang),36)
        text_surface = font.render(self._lang.get(self.sign,self._lang._lang), True, (0, 0, 0))
        text_rect = text_surface.get_rect()

        text_rect.center = self.rect.center

        self.screen.blit(text_surface, text_rect)