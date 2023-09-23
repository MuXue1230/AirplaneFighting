import pygame

class GUI:
    def __init__(self,screen,swidth,sheight,is_open=False):
        self.screen = screen
        self.width = swidth
        self.height = sheight
        self.things = {}
        self.click = False
        self.is_open = is_open
    
    def open(self):
        self.is_open =  True

    def close(self):
        self.is_open = False
    
    def add_button(self,btn):
        for _id in range(1,11):
            if 'button'+str(_id) in self.things.keys():
                if _id == 10:
                    raise SyntaxError("Don't put mor than 10 object in 1 UI.")
                continue
            else:
                self.things['button'+str(_id)] = (btn,False)
                break
    
    def add_label(self,lab):
        for _id in range(1,11):
            if 'label'+str(_id) in self.things.keys():
                if _id == 10:
                    raise SyntaxError("Don't put mor than 10 object in 1 UI.")
                continue
            else:
                self.things['label'+str(_id)] = lab
                break
    
    def add_thing(self,img):
        for _id in range(1,21):
            if 'thing'+str(_id) in self.things.keys():
                if _id == 20:
                    raise SyntaxError("Don't put mor than 20 images in 1 UI.")
                continue
            else:
                self.things['thing'+str(_id)] = img
                break
    
    def draw(self):
        last = None
        for _id in self.things.keys():
            _object = self.things[_id]
            if 'label' in _id:
                _object.draw(last)
            elif 'button' in _id:
                _object[0].draw(last)
            elif 'thing' in _id:
                _object.draw(last)
            last = _object
    
    def check(self):
        if pygame.mouse.get_pressed()[0]:
            self.click = True
            for _id in self.things.keys():
                if 'button' in _id:
                    _object, _over = self.things[_id]
                    pos = pygame.mouse.get_pos()
                    if _object.rect.left < pos[0] < _object.rect.right and \
                        _object.rect.top < pos[1] < _object.rect.bottom:
                        _object.img = _object.img_click
                        _object.rect = _object.rect_click
        elif not pygame.mouse.get_pressed()[0] and self.click:
            self.click = False
            for _id in self.things.keys():
                if 'button' in _id:
                    _object, _over = self.things[_id]
                    pos = pygame.mouse.get_pos()
                    if _object.rect.left < pos[0] < _object.rect.right and \
                        _object.rect.top < pos[1] < _object.rect.bottom:
                        _object.press(_object.argv)
        elif not pygame.mouse.get_pressed()[0] and not self.click:
            for _id in self.things.keys():
                if 'button' in _id:
                    _object, _over = self.things[_id]
                    pos = pygame.mouse.get_pos()
                    if _object.rect.left < pos[0] < _object.rect.right and \
                        _object.rect.top < pos[1] < _object.rect.bottom:
                        _object.img = _object.img_over
                        _object.rect = _object.rect_over
                        if not _over:
                            _object.over(_object.argv)
                            self.things[_id] = (_object,True)
                    else:
                        _object.img = _object.img_nor
                        _object.rect = _object.rect_nor
                        self.things[_id] = (_object,False)