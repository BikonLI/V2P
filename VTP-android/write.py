import os
import json
import time


class Write:
    
    app_path = None   # 这两个都是文件路径 "settings.json", "vtp_log.txt"
    log_path = None
    
    def __init__(self, app_path=None, log_path=None) -> None:
        self.app_path = app_path
        self.log_path = log_path
        
        app_path_exist = os.path.exists(app_path)
        log_path_exist = os.path.exists(log_path)
        
        if not app_path_exist:
            with open(self.app_path, 'w', encoding="utf-8") as f:
                json.dump({"Settings": []}, f, indent=4)
                
        if not log_path_exist:
            with open(self.log_path, 'w', encoding="utf-8") as f:
                now = time.localtime()
                formatted_now = time.strftime("%Y-%m-%d %H:%M:%S", now)  
                print(f"[VTP-start-logging]  {formatted_now}", file=f)
    
    @property
    def get_time(self) -> str:
        now = time.localtime()
        formatted_now = time.strftime("%Y-%m-%d %H:%M:%S", now)
        return formatted_now
    
    def log(self, name, content) -> None:
        with open(self.log_path, 'a', encoding="utf-8") as f: 
            print(f"[{name}]  {content}  {self.get_time}", file=f)
        self.STDO(name, content)
    
    def STDO(self, name, content) -> None:
        print(f"[{name}]  {content}  {self.get_time}")
        
    @property
    def settings(self) -> dict:
        with open(self.app_path, 'r', encoding="utf-8") as f:
            _settings = json.load(f)
        return _settings
    
    @settings.setter
    def settings(self, value) -> None:
        with open(self.app_path, 'w', encoding="utf-8") as f:
            json.dump(value, f)
      

# 测试类      
# class Write:
#     def __init__(self, *args, **kwargs) -> None:
#         pass
#     def log(*args, **kwargs):
#         pass
#     def settings(*args, **kwargs):
#         pass
# write = Write()
            
            
if __name__ == "__main__":
    write = Write(app_path="./settings.json", log_path="./log.txt")
    write.log("error", "permission denied.")
    print(write.settings.get("Settings"))
            