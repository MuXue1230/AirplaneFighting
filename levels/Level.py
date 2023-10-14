from time import time
import json

from plugin.Listener import Listener

class Level(Listener):
    planes = {}
    timer = 0
    is_running = False

    def __init__(self,name):
        with open('assets/level/'+name+'.json','r') as f:
            self.planes = json.load(f)

    def start(self):
        self.timer = time()
        self.is_running = True
    
    def stop(self):
        self.is_running = False
    
    def get_planes_num(self):
        return self.planes['num']
    
    def handle(self, argv):
        if self.is_running:
            for item in range(len(self.planes['add_small_enemies'])):
                if (time() - self.timer) >= float(self.planes['add_small_enemies'][item]['time']):
                    if self.planes['add_small_enemies'][item]['active']:
                        self.planes['add_small_enemies'][item]['plane'] = argv['tool'].add_small_enemies(argv['small_enemies'],argv['enemies'],1,argv['eventBus'],argv,True)
                        self.planes['add_small_enemies'][item]['plane'].set_top(-50)
                        self.planes['add_small_enemies'][item]['active'] = False
                    else:
                        if self.planes['add_small_enemies'][item]['plane'].active:
                            self.planes['add_small_enemies'][item]['plane'].rect.centerx = argv['screen'].get_width() * (self.planes['add_small_enemies'][item]['x'] / 100)
            
            for item in range(len(self.planes['add_mid_enemies'])):
                if (time() - self.timer) >= float(self.planes['add_mid_enemies'][item]['time']):
                    if self.planes['add_mid_enemies'][item]['active']:
                        self.planes['add_mid_enemies'][item]['plane'] = argv['tool'].add_mid_enemies(argv['mid_enemies'],argv['enemies'],1,argv['eventBus'],argv,True)
                        self.planes['add_mid_enemies'][item]['plane'].set_top(-100)
                        self.planes['add_mid_enemies'][item]['active'] = False
                    else:
                        if self.planes['add_mid_enemies'][item]['plane'].active:
                            self.planes['add_mid_enemies'][item]['plane'].rect.centerx = argv['screen'].get_width() * (self.planes['add_mid_enemies'][item]['x'] / 100)
            
            for item in range(len(self.planes['add_big_enemies'])):
                if (time() - self.timer) >= float(self.planes['add_big_enemies'][item]['time']):
                    if self.planes['add_big_enemies'][item]['active']:
                        self.planes['add_big_enemies'][item]['plane'] = argv['tool'].add_big_enemies(argv['big_enemies'],argv['enemies'],1,argv['eventBus'],argv,True)
                        self.planes['add_big_enemies'][item]['plane'].set_top(-260)
                        self.planes['add_big_enemies'][item]['active'] = False
                    else:
                        if self.planes['add_big_enemies'][item]['plane'].active:
                            self.planes['add_big_enemies'][item]['plane'].rect.centerx = argv['screen'].get_width() * (self.planes['add_big_enemies'][item]['x'] / 100)