from kivy.lang import Builder
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

from plyer import filechooser, storagepath
from android.permissions import Permission, check_permission
from android.storage import primary_external_storage_path

import threading as td

from custom_widgets import FilledButton, Radio, ProcessBar, Dropdown, TextButton
from utility import Logger
from videotopictures import extract

import os
from utility import write
# 测试专用
# extract = None
# write = None



module_path = os.path.abspath(__file__)  
module_dir = os.path.dirname(module_path)  
file_path = os.path.join(module_dir, "page0.kv")  
build = Builder.load_file(file_path)
font_path_bold = os.path.join(module_dir, "res/HarmonyOS_SansSC_Bold.ttf")
font_path_regular = os.path.join(module_dir, "res/HarmonyOS_SansSC_Regular.ttf")
LabelBase.register(name='Roboto',  
                   fn_regular=font_path_regular,  
                   fn_bold=font_path_bold) 
# Window.size = (300, 620)


selected_file: str | None = None
isExtracting: bool = False

# content = BoxLayout(orientation="vertical")
# content.add_widget(Label(text="该应用需要申请外部存储权限以读取.../Downloads/文件夹来存储提取的照片。", color="black"))
# content.add_widget(btns := BoxLayout(orientation="horizontal"))

# btns.add_widget(btn0 := Button(text="取消", background_color=(0, 0, 0, 0), background_normal = "normal"))
# btns.add_widget(btn0 := Button(text="确定", background_color=(0, 0, 0, 0), background_normal = "normal", ))

    


# def get_external_storage_permission():
#     settings = write.settings
#     permission_list = settings.get("permissions")
    
#     if not ("WRITE_EXTERNAL_STORAGE" in permission_list):
#         Logger.info("Get storage permission: try to get WRITE_EXTERNAL_STORAGE permission from user")
#         write.log("Get storage permission", "try to get WRITE_EXTERNAL_STORAGE permission from user")
#         request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
#         permission_list.append("WRITE_EXTERNAL_STORAGE")
#         settings["permissions"] = permission_list.copy()
#         write.settings = settings
        
#     else:
#         ex_dir = primary_external_storage_path()
#         p.extract_path = os.path.join(ex_dir, "Downloads")
#         write.log("Get extract path", p.extract_path)
#         Logger.info(f"Get extract path: {p.extract_path}")

# get_storage_permission_popup = PermissionsPopup()
# get_storage_permission_popup = Popup(
#     title = "申请外部存储权限",
#     content = content,
#     auto_dismiss = False,
#     size_hint = (0.9, 0.3),
#     pos_hint = {"center_x": 0.5, "center_y": 0.5}
# )


def getInfo():
    dropdown = build.ids
    return {
        "video": selected_file,
        "size": dropdown["size"].chosen,
        "frame": dropdown["frame"].chosen,
        "format": dropdown["format"].chosen,
        "spin": dropdown["spin"].chosen,
    }
    
class p:
    pb = None
    video = None
    size = None
    frame = None
    format = None
    spin = None
    handle = None
    new_thread = None
    extract_path = None
p = p()

def press(*args):
    global isExtracting
    if not isExtracting:
        a = getInfo()
        write.log(f"INFO", a)    
        p.video = a["video"]
        if a["size"] == "默认" or a["size"] == None or a['size'] == '':
            p.size = None
        else:
            p.size = a["size"].strip('()').split(', ')
            p.size = tuple((int(p.size[0]), int(p.size[1])))
        if a["frame"]:
            p.frame = int(a["frame"])
        else:
            p.frame = None
        if a["format"]:
            p.format = a["format"]
        else:
            p.format = None
        if a["spin"]:
            p.spin = int(a["spin"])
        else: 
            p.spin = None

        if not p.video:
            write.log("INFO", "Video path has not chosen.")
            build.add_widget(lb := Label(text="请先选择视频文件！", size_hint = (0.5, 0.05), pos_hint = {"left": 1, "center_y": 0.3}, color = (0, 0, 0, 1)))
            def remove(*args):
                build.remove_widget(lb)
            Clock.schedule_once(remove, 3)

        if not p.frame:
            p.frame = 1
        if not p.format:
            p.format = ".jpg"
        if p.video:
            p.pb = ProgressBar(
                max = 0, 
                size_hint = (0.9, None),
                size = (0, 20),
                pos_hint = {"center_x": 0.5, "center_y": 0.3}
            )
            build.add_widget(p.pb)

def release(*args):  
    global isExtracting
    def flash(*args):
        global isExtracting
        if p.pb.max == 0 and p.pb.value == 0:
            Logger.debug(f"ProgressBar: {p.pb.max} {extract.total_frame}")
            p.pb.max = extract.total_frame
        if p.pb.value < extract.total_frame:
            p.pb.value = extract.count
        if not p.new_thread.is_alive():
            build.remove_widget(p.pb)
            Clock.unschedule(p.handle)
            isExtracting = 0
            
    def stop_schedule(*args):
        pass
    
    write.log("Extract", f"Try to get extract path")
    dn_dir = storagepath .get_documents_dir()
    p.extract_path = os.path.join(dn_dir, "ExtractPictures")
    # p.extract_path = dn_dir
    write.log("Extract", f"Extract path accessed {p.extract_path}")
    per = check_permission(Permission.WRITE_EXTERNAL_STORAGE)
    if per:
        os.makedirs(p.extract_path, exist_ok=True)
    if p.video and not isExtracting and per:
        isExtracting = 1
        p.handle = Clock.schedule_interval(flash, 0.5)
        args = (p.video, p.size, p.frame, p.format, p.spin, p.extract_path, stop_schedule)
        p.new_thread = td.Thread(target=extract.start, args=args)
        p.new_thread.daemon = True
        p.new_thread.start()
        write.log("INFO", "start extracting pictures")
    # Clock.unschedule(handle)
    
        
build.ids["extract"].on_press = press
build.ids["extract"].on_release = release


def select_file(*args):
    def on_file_selected(selections):
        write.log("INFO", "start to select file")
        filter = "video files", "*.mp4;*.avi;*.mov"
        global selected_file
        if selections:
            write.log("filechooser", f"{selections}")
            spliter = os.path.splitext(selections[0])
            if spliter[-1] in [".mp4", ".3gp", ".avi", ".mkv", ".mov", ".wmv", ".flv"]:
                selected_file = selections[0]
                write.log("filechooser", "file selected")
            else:
                selected_file = ""
            
    filechooser.open_file(on_selection=on_file_selected, filter=filter)
build.ids["choose_file"].on_release = select_file

def getPage0():
    return build
    
if __name__ == "__main__":
    
    
    class Test(App):

        def build(self):
            return build

    Test().run()