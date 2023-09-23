from plane import EnemyPlane
import empty

class MiddleEnemyPlane(EnemyPlane):
    energy = 8
    def __init__(self, bg_size, assets_path, eventBus, argv) -> None:
        super().__init__(bg_size, assets_path, 'middle', eventBus, argv)
        self.image_hit = empty.load_image(assets_path+"images/middle_enemy_hit.png", eventBus, argv).convert_alpha()
        self.energy = MiddleEnemyPlane.energy
        self.speed = 250
        self.hit = False

    def reset(self):
        super().reset()
        self.energy = MiddleEnemyPlane.energy
