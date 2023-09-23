from supply import Supply

class BulletSupply(Supply):
    def __init__(self, bg_size, assets_path, eventBus, argv):
        super().__init__(bg_size, assets_path, 'bullet', eventBus, argv)
