from bullet import Bullet

class DoubleBullet(Bullet):
    def __init__(self, position, assets_path, eventBus, argv):
        super().__init__(position, assets_path, 2, eventBus, argv)
        self.speed = 2400
