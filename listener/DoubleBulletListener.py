import plugin

class DoubleBulletListener(plugin.Listener):
    def handle(_,event):
        event.argv['is_double_bullet'][0] = False