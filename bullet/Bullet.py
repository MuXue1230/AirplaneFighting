import pygame
import empty

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, assets_path, id, eventBus, argv):
        pygame.sprite.Sprite.__init__(self)

        self.image = empty.load_image(assets_path+"images/bullet_"+str(id)+".png", eventBus, argv).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 0
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_temp = 0

    def move(self,delay_time):
        self.pos_temp -= self.speed*delay_time
        self.rect.top = int(self.pos_temp)

        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True
        self.pos_temp = self.rect.top
