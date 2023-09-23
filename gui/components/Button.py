import pygame
from gui.components.Thing import Thing

class Button(Thing):
    def __init__(self, screen:pygame.surface.Surface,press, img_nor, img_over, img_click, \
                    over, pos:tuple=('under',0,10), father:pygame.surface.Surface|None=None, \
                    father_obj=None, **argv):
        self.img_nor = img_nor
        self.img_over = img_over
        self.img_click = img_click
        self.rect_nor = self.img_nor.get_rect()
        self.rect_over = self.img_over.get_rect()
        self.rect_click = self.img_click.get_rect()
        super().__init__(screen,self.img_nor,pos,father,father_obj)
        self.press = False
        self.over = False
        self.press = press
        self.over = over
        self.argv = argv
    
    def draw(self,pre:object):
        super().draw(pre)