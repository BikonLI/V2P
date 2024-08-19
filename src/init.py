import os
import threading
import time
from videotopictures import Extract as VideoExtract
from utils import resources as res
from kivy.logger import Logger
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex, platform
from plyer import filechooser, storagepath

# --- --- ---
from kivymd.app import MDApp
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.metrics import sp
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.behaviors import ButtonBehavior, TouchRippleButtonBehavior
from kivy.animation import Animation

from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.progressindicator import MDLinearProgressIndicator


from kivy.properties import (
    BoundedNumericProperty, 
    BooleanProperty,
    StringProperty,
    ObjectProperty,
    ColorProperty,
    ListProperty,
)
from kivy.lang import Builder

if platform == "android":
    from android.permissions import (
        Permission, 
        request_permissions, 
        check_permissions
    )
    
else:
    # Window.size = (300, 620)
    Window.size = 700, 600
    
appPath = storagepath.get_application_dir()
picStoragePath = os.path.join(storagepath.get_documents_dir(), "Extraction")
resPath = res.resPath

os.makedirs(picStoragePath, exist_ok=True)

HMBOLD = os.path.join(resPath, "MiSans-Bold.ttf")
HMMEDIUM = os.path.join(resPath, "MiSans-Normal.ttf")
HMREGULAR = os.path.join(resPath, "MiSans-Regular.ttf")

LabelBase.register(name="MiSans", fn_regular=HMREGULAR, fn_bold=HMBOLD)  


class VTP(MDApp):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.font_styles["MiSans"] = {
            "large": {
                "line-height": 1.64,
                "font-name": "MiSans",
                "font-size": sp(57),
            },
            "medium": {
                "line-height": 1.52,
                "font-name": "MiSans",
                "font-size": sp(18),
            },
            "small": {
                "line-height": 1.44,
                "font-name": "MiSans",
                "font-size": sp(11),
            },
        }
    
    def build(self):
        
        return None
    
vtp = VTP()
