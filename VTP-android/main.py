from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import SlideTransition
from kivy.clock import Clock
from kivy.logger import Logger
from android.permissions import request_permissions, check_permission, Permission

import os

from custom_widgets import NavigationBar
from custom_widgets.Navigation import getText
from custom_widgets.PermissionsPopup import get_storage_permission_popup

from page0 import getPage0, p
from page1 import getPage1
 
from utility import write

# Window.size = (300, 620)

rootInterface = FloatLayout()
sm = ScreenManager(size_hint = (1, 1))
nv = NavigationBar(background_color=(0.95, 0.96, 0.96, 1))

rootInterface.add_widget(sm)
rootInterface.add_widget(nv)

sm.add_widget(page0 := Screen(name="home"))
sm.add_widget(page1 := Screen(name="info"))

page0.add_widget(fl0 := FloatLayout(pos_hint = {"center_x": 0.5, "center_y": 0.5}))
page1.add_widget(fl1 := FloatLayout(pos_hint = {"center_x": 0.5, "center_y": 0.5}))

on_release_func_btn0 = nv.ids["btn0"].on_release_func
on_release_func_btn1 = nv.ids["btn1"].on_release_func

fl0.add_widget(getPage0())
fl1.add_widget(getPage1())
# fl0.add_widget(nv)

def switch(self):# -> Callable[..., None]:
    def inner(*args):
        text = getText(self.text)
        if text == "btn0":
            sm.transition = SlideTransition(direction = "right", duration = 0.3)
            on_release_func_btn0()
            sm.current = "home"
        else:
            sm.transition =  SlideTransition(direction = "left", duration = 0.3)
            on_release_func_btn1()
            sm.current = "info"
    return inner
        
nv.ids["btn0"].on_release_func = switch(nv.ids["btn0"])
nv.ids["btn1"].on_release_func = switch(nv.ids["btn1"])


class VTP(App):
    def build(self):
        write.log("Success", "building user interface")
        return rootInterface
    
    def on_start(self):
        write.log("Start", "starting the app")
        return super().on_start()
    
    def on_stop(self):
        write.log("Stop", "terminating the app")
        return super().on_stop()
    
    def on_pause(self):
        write.log("Pause", "pausing the app")
        return super().on_pause()
    
    def on_resume(self):
        write.log("Resume", "resuming the app")
        return super().on_resume()
    
    def request_permissions(self, *args):
        def __request_permissions():
            Logger.info("Get storage permission: try to get WRITE_EXTERNAL_STORAGE permission from user")
            write.log("Get storage permission", "try to get WRITE_EXTERNAL_STORAGE permission from user")
            request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE, 
            Permission.READ_MEDIA_VIDEO
                ])
        p0 = check_permission(Permission.READ_EXTERNAL_STORAGE)
        p1 = check_permission(Permission.WRITE_EXTERNAL_STORAGE)
        p2 = check_permission(Permission.READ_MEDIA_VIDEO)
        if not (p0 and p1 and p2):
            get_storage_permission_popup.func = __request_permissions
            get_storage_permission_popup.open(animation=True)
            
    
    def run(self):
        Clock.schedule_once(self.request_permissions)
        
        super().run()
                  
if __name__ == "__main__":
    VTP().run()





