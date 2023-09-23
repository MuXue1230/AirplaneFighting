from time import time


class Level:
    planes = {}
    timer = 0

    def start(self):
        self.timer = time()
    
    