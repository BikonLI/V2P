import os
from android.storage import app_storage_path
from write import Write
from kivy.logger import Logger, LOG_LEVELS

# Logger.setLevel(LOG_LEVELS["debug"])

# write = Write()  # 测试

app_dir = app_storage_path()

head, tail = os.path.split(__file__)
setting_path = os.path.join(head, "settings")
logging_path = os.path.join(head, "log")

os.makedirs(setting_path, exist_ok=True)
os.makedirs(logging_path, exist_ok=True)

setting_path = os.path.join(setting_path, "settings.json")
logging_path = os.path.join(logging_path, "vtp_log.txt")

write = Write(setting_path, logging_path)
data = write.settings
data["permissions"] = []
write.settings = data
