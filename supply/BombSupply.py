from supply import Supply

class BombSupply(Supply):
    def __init__(self, bg_size, assets_path, eventBus, argv):
        super().__init__(bg_size, assets_path, 'bomb', eventBus, argv)
