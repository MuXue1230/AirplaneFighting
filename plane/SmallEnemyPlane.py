from plane import EnemyPlane

class SmallEnemyPlane(EnemyPlane):
    def __init__(self, bg_size, assets_path, eventBus, argv) -> None:
        super().__init__(bg_size, assets_path, 'small', eventBus, argv)
        self.speed = 480
