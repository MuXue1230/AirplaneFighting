import plugin

class NoHitListener(plugin.Listener):
    def handle(_,event):
        event.argv['me'].invincible = False