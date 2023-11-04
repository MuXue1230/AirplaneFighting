import time
import os

from sys import stdout, argv
from debug import LoggerType

class Logger:
    def __init__(self, out=stdout):
        self.out = out
        for x in range(99):
            if 'log'+str(x)+'.log' in os.listdir('log'):
                continue
            break
        self.file = open('log/log'+str(x)+'.log','w')
        self.debug('Logger is ready (in',self,'\b)')
    
    def output(self, *text, _type):
        print('['+time.ctime()[11:-5]+'|'+('DEBUG' if _type==LoggerType.DEBUG else 'LOG' if _type==LoggerType.LOG else 'ERROR' if _type==LoggerType.ERROR else 'UNKNOW')+']',*text)
        self.file.write('['+time.ctime()[11:-5]+'|'+('DEBUG' if _type==LoggerType.DEBUG else 'LOG' if _type==LoggerType.LOG else 'ERROR' if _type==LoggerType.ERROR else 'UNKNOW')+'] ')
        for item in text:
            self.file.write(' '+str(item))
        self.file.write('\n')
    
    def debug(self, *text):
        if '--debug' in argv:
            self.output(*text, _type=LoggerType.DEBUG)
    
    def log(self, *text):
        self.output(*text, _type=LoggerType.LOG)
    
    def error(self, *text):
        self.output(*text, _type=LoggerType.ERROR)