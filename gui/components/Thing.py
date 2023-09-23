import pygame

class Thing:
    def __init__(self, screen:pygame.surface.Surface, image:pygame.surface.Surface, \
                 pos:tuple=('under',0,10), father:pygame.surface.Surface|None=None, \
                 father_obj=None):
        self.screen = screen
        self.img = image
        self.father = father
        self.father_obj = father_obj
        self.rect = self.img.get_rect()
        self.pos  = pos
    
    def draw(self,pre:object):
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
            self.rect.left -= x
            self.rect.top -= y
        elif m_pos == 'center_obj':
            self.rect.center = self.father_obj.rect.center
            self.rect.left -=x
            self.rect.top -= y
        
        self.screen.blit(self.img, self.rect)