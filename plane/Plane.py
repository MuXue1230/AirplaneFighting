import pygame

import empty

class Plane(pygame.sprite.Sprite):
    def __init__(self, bg_size, assets_path, name, eventBus, argv) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image1 = empty.load_image(assets_path+"images/"+name+"_1.png", eventBus, argv).convert_alpha()
        self.image2 = empty.load_image(assets_path+"images/"+name+"_2.png", eventBus, argv).convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            empty.load_image(assets_path+"images/"+name+"_destroy_1.png", eventBus, argv).convert_alpha(), \
            empty.load_image(assets_path+"images/"+name+"_destroy_2.png", eventBus, argv).convert_alpha(), \
            empty.load_image(assets_path+"images/"+name+"_destroy_3.png", eventBus, argv).convert_alpha(), \
            empty.load_image(assets_path+"images/"+name+"_destroy_4.png", eventBus, argv).convert_alpha() \
            ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 0
        self.active = True
        self.down_sound = empty.load_sound(assets_path + "sound/"+name+"_destroy.wav", eventBus, argv)
        self.down_sound.set_volume(0.5)
    
    def reset(self):
        pass