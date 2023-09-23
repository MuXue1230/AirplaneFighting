import plugin

class BombListener(plugin.Listener):
    def handle(_,event):
        if event.argv['bomb_num'][0]:
            event.argv['bomb_num'][0] -= 1
            if event.argv['conf'].settings['mix']: event.argv['bomb_sound'].play()
            for each in event.argv['enemies']:
                if each.rect.bottom > 0:
                    each.active = False