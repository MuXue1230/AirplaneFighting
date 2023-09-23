import pygame
import random

import empty

class Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size, assets_path, type, eventBus, argv):
        pygame.sprite.Sprite.__init__(self)

        self.image = empty.load_image(assets_path+"images/"+type+"_supply.png", eventBus, argv).convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.width - self.rect.width), -100
        self.speed = 150
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_temp = 0

    def move(self,delay_time):
        if self.rect.top < self.height:
            self.pos_temp += self.speed*delay_time
            self.rect.top = int(self.pos_temp)
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.pos_temp = 0
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.width - self.rect.width), -100