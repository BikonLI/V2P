from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.app import App

import os
from utility import write
module_path = os.path.abspath(__file__)  
module_dir = os.path.dirname(module_path)  
file_path = os.path.join(module_dir, "page1.kv")  
build = Builder.load_file(file_path)

font_path_bold = os.path.join(module_dir, "res/HarmonyOS_SansSC_Bold.ttf")
font_path_regular = os.path.join(module_dir, "res/HarmonyOS_SansSC_Regular.ttf")

LabelBase.register(name='Roboto',  
                   fn_regular=font_path_regular,  
                   fn_bold=font_path_bold) 

# Window.size = (300, 620)


def getPage1():
    return build
    