import random

import plugin

class SupplyListener(plugin.Listener):
    def handle(self,event):
        if event.argv['conf'].settings['mix']:
            event.argv['supply_sound'].play()
        if random.choice([True,False]):
            event.argv['bomb_supply'].reset()
        else:
            event.argv['bullet_supply'].reset()