import empty
from plane import EnemyPlane

import pygame
import random

class BigEnemyPlane(EnemyPlane):
    energy = 20
    def __init__(self, bg_size, assets_path, eventBus, argv) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.image1 = empty.load_image(assets_path+"images/big_enemy_1.png", eventBus, argv).convert_alpha()
        self.image2 = empty.load_image(assets_path+"images/big_enemy_2.png", eventBus, argv).convert_alpha()
        self.image_hit = empty.load_image(assets_path+"images/big_enemy_hit.png", eventBus, argv).convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            empty.load_image(assets_path+"images/big_enemy_destroy_1.png", eventBus, argv).convert_alpha(), \
            empty.load_image(assets_path+"images/big_enemy_destroy_2.png", eventBus, argv).convert_alpha(), \
            empty.load_image(assets_path+"images/big_enemy_destroy_3.png", eventBus, argv).convert_alpha(), \
            empty.load_image(assets_path+"images/big_enemy_destroy_4.png", eventBus, argv).convert_alpha(), \
            empty.load_image(assets_path+"images/big_enemy_destroy_5.png", eventBus, argv).convert_alpha(), \
            empty.load_image(assets_path+"images/big_enemy_destroy_6.png", eventBus, argv).convert_alpha() \
            ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 250
        self.active = True
        self.rect.left, self.rect.top = \
                        random.randint(0, self.width - self.rect.width), \
                        random.randint(-15 * self.height, -5 * self.height)
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = BigEnemyPlane.energy
        self.hit = False
        self.pos_temp = 0
        self.destroy_index = 0
        self.fly_sound = empty.load_sound(assets_path + "sound/big_enemy_flying.wav", eventBus, argv)
        self.fly_sound.set_volume(0.5)
        self.down_sound = empty.load_sound(assets_path + "sound/big_enemy_destroy.wav", eventBus, argv)
        self.down_sound.set_volume(0.5)
        self.reset()
    
    def reset(self):
        super().reset()
        self.energy = BigEnemyPlane.energy
        self.down_sound.fadeout(1000)
