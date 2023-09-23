import pygame
import sys

import plugin

class ExitListener(plugin.Listener):
    def handle(_,event):
        pygame.quit()
        sys.exit()
