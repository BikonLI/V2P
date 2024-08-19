import os
import json
from kivy.logger import Logger

    
class ReadRes:
    
    resPath = ""
    
    def __init__(self) -> None:
        libPath, fileName = os.path.split(__file__)
        appPath, _ = os.path.split(libPath)
        resPath = os.path.join(appPath, "res")
        
        self.resPath = resPath
        
    def getString(self, key, lang: str="Zh") -> None:
        
        if isinstance(key, int):
            key = f'{key:04}'
        
        stringPath = os.path.join(self.resPath, "string")
        langPath = os.path.join(stringPath, lang + '.json')
        
        with open(langPath, 'r', encoding="utf-8") as f:
            textJson = json.load(f)
        
        try:
            text = textJson[key]
        except KeyError:
            Logger.debug("TEXT: Can't find the text")
            text = ''
            
        return text
    
    def getFont(self, fontName: str):
        return fontName
      
resources = ReadRes()

if __name__ == "__main__":

    print(resources.getString(0))
      