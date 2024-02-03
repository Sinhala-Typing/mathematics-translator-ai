import json

class Config:
    DATA = 
    
    @staticmethod
    def __load_json():
        with open("config.json", "r", encoding='utf-8') as file:
            Config.DATA = json.load(file)
    
    def 
            