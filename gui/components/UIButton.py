import pygame
import lang
import empty
from gui.components.Button import Button

class UIButton(Button):
    def __init__(self, screen:pygame.surface.Surface, sign:str, _lang:lang.Language,eventBus,arg,press, \
                    over, pos:tuple=('under',0,10), father:pygame.surface.Surface|None=None, \
                    father_obj=None,asset_path="", **argv):
        self.img_nor  = empty.load_image(asset_path+"images/button.png",eventBus,arg).convert_alpha()
        self.img_over  = empty.load_image(asset_path+"images/button_over.png",eventBus,arg).convert_alpha()
        self.img_click  = empty.load_image(asset_path+"images/button_pressed.png",eventBus,arg).convert_alpha()
        super().__init__(screen,press,self.img_nor,self.img_over,self.img_click,over,pos,father,father_obj,**argv)
        self._lang = _lang
        self.sign = sign

    def draw(self,pre:object):
        super().draw(pre)
        
        font = pygame.font.Font(self._lang.get_font(self._lang._lang), 32)
        text_surface = font.render(self._lang.get(self.sign,self._lang._lang), True, (0, 0, 0))
        text_rect = text_surface.get_rect()

        text_rect.center = self.rect.center

        self.screen.blit(text_surface, text_rect)