from plane import Plane
import empty

import pygame
import random

class EnemyPlane(Plane):
    def __init__(self, bg_size, assets_path, name, eventBus, argv) -> None:
        super().__init__(bg_size, assets_path, name+'_enemy', eventBus, argv)
        self.image = empty.load_image(assets_path+"images/"+name+"_enemy.png", eventBus, argv).convert_alpha()
        self.rect.left, self.rect.top = \
                        random.randint(0, self.width - self.rect.width), \
                        random.randint(-5 * self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_temp = 0
        self.destroy_index = 0
        self.reset()
    
    def move(self,delay_time):
        if self.rect.top < self.height:
            self.pos_temp += self.speed*delay_time
            self.rect.top = int(self.pos_temp)
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = \
                        random.randint(0, self.width - self.rect.width), \
                        random.randint(-5 * self.height, 0)
        self.pos_temp = self.rect.top
        self.down_sound.fadeout(1000)
