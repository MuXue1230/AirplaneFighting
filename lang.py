import os

class Language:
    def __init__(self,dir,_lang):
        self.dir = dir
        self._lang = _lang
        try:
            self.lang_files = self._filter(os.listdir(self.dir+'lang'),".lang")
        except:
            print("[ERROR]语言文件不全，无法导入！\n路径"+dir+'lang'+"无效")
            self.lang_files = []
        self.internationalized_text = {}
        for _file in self.lang_files:
            try:
                with open(self.dir+"lang/"+_file,'r',encoding="utf-8") as f:
                    try:
                        self.internationalized_text[_file[:-5]]= \
                            {**self.internationalized_text[_file[:-5]], \
                             **self._segmentation(f.read().split('\n'))}
                    except:
                        self.internationalized_text[_file[:-5]]= \
                            {**self._segmentation(f.read().split('\n'))}
            except:
                pass
    
    def _filter(self,file_list:list, filter:str="")->list:
        result = []
        for _file in file_list:
            if filter in _file:
                result.append(_file)
        return result

    def _segmentation(self,lst:list,split:str="=")->dict:
        result = {}
        for item in lst:
            if item != '':
                key, value = item.split(split)
                result[key] = value
        return result
    
    def get(self,iSign:str,lang:str):
        if 'game.set_option.language.' in iSign:
            try:
                return list(self.get_language_list().values())[int(iSign[-1:])-1]
            except:
                try:
                    return list(self.get_language_list().keys())[int(iSign[-4:-3])-1]
                except:
                    pass
        try:
            return self.internationalized_text[lang][iSign]
        except:
            try:
                return self.internationalized_text['en_us'][iSign]
            except:
                return iSign
    
    def get_language_list(self):
        result={}
        for _lang in self.lang_files:
            result[_lang[:-5]] = self.get("lang.name.text",_lang[:-5])
        return result
    
    def get_font(self,lang:str)->str|None:
        try:
            font_files = self._filter(os.listdir(self.dir+'font'),".ttf")
        except:
            print("[ERROR]语言文件不全，无法导入！\n路径"+self.dir+'font'+"无效")
            font_files = []
        if lang+".ttf" in font_files:
            return self.dir+'font/'+lang+'.ttf'
        else:
            print("[ERROR]语言文件不全，无法导入！\n文件"+self.dir+'font/'+lang+'.ttf'+"无效")
            return None
    
    def add_path(self,path):
        for _file in self.lang_files:
            try:
                with open(path+"lang/"+_file,'r',encoding="utf-8") as f:
                    try:
                        self.internationalized_text[_file[:-5]]= \
                            {**self.internationalized_text[_file[:-5]], \
                             **self._segmentation(f.read().split('\n'))}
                    except:
                        self.internationalized_text[_file[:-5]]= \
                            {**self._segmentation(f.read().split('\n'))}
            except:
                pass
