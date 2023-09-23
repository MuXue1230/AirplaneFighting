import plane

class Tools:
    def __init__(self, bg_size, conf):
        self.bg_size = bg_size
        self.conf = conf

    def add_small_enemies(self, group1, group2, num, eventBus, argv):
        for i in range(num):
            e1 = plane.SmallEnemyPlane(self.bg_size,self.conf.assets_path, eventBus, argv)
            group1.add(e1)
            group2.add(e1)

    def add_mid_enemies(self, group1, group2, num, eventBus, argv):
        for i in range(num):
            e2 = plane.MiddleEnemyPlane(self.bg_size,self.conf.assets_path, eventBus, argv)
            group1.add(e2)
            group2.add(e2)

    def add_big_enemies(self, group1, group2, num, eventBus, argv):
        for i in range(num):
            e3 = plane.BigEnemyPlane(self.bg_size,self.conf.assets_path, eventBus, argv)
            group1.add(e3)
            group2.add(e3)

    def inc_speed(self, target, inc):
        for each in target:
            each.speed += inc