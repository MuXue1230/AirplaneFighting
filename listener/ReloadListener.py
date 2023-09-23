import subprocess
import sys
import pygame

import plugin

class ReloadListener(plugin.Listener):
    def handle(_,event):
        print('reload')
        pygame.quit()
        if '.py' in sys.argv[0]:
            subprocess.run(['py',*sys.argv], stdout=sys.stdout, stderr=sys.stderr)
        else:
            subprocess.run(sys.argv, stdout=sys.stdout, stderr=sys.stderr)
        sys.exit()