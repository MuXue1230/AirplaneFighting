import pygame

from plane import Plane

class PlayerPlane(Plane):
    def __init__(self, bg_size, assets_path, sensitivity, eventBus, argv) -> None:
        super().__init__(bg_size, assets_path, 'player', eventBus, argv)
        self.rect.left, self.rect.top = \
                        (self.width - self.rect.width) // 2, \
                        self.height - self.rect.height - 60
        self.speed = sensitivity
        self.invincible = False
        self.mask = pygame.mask.from_surface(self.image1)
        self.pos_temp = [self.rect.left,self.rect.top]
    
    def moveUp(self,delay_time):
        if self.rect.top > 0:
            self.pos_temp[1] -= self.speed*delay_time
            self.rect.top = int(self.pos_temp[1])
        else:
            self.rect.top = 0

    def moveDown(self,delay_time):
        if self.rect.bottom < self.height - 60:
            self.pos_temp[1] += self.speed*delay_time
            self.rect.top = int(self.pos_temp[1])
        else:
            self.rect.bottom = self.height - 60

    def moveLeft(self,delay_time):
        if self.rect.left > 0:
            self.pos_temp[0] -= self.speed*delay_time
            self.rect.left = int(self.pos_temp[0])
        else:
            self.rect.left = 0

    def moveRight(self,delay_time):
        if self.rect.right < self.width:
            self.pos_temp[0] += self.speed*delay_time
            self.rect.left = int(self.pos_temp[0])
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left, self.rect.top = \
                        (self.width - self.rect.width) // 2, \
                        self.height - self.rect.height - 60
        self.active = True
        self.invincible = True
        self.pos_temp = [self.rect.left,self.rect.top]
