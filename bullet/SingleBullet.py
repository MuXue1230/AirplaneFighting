from bullet import Bullet

class SingleBullet(Bullet):
    def __init__(self, position, assets_path, eventBus, argv):
        super().__init__(position, assets_path, 1, eventBus, argv)
        self.speed = 1200
