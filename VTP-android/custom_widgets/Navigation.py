from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import TouchRippleButtonBehavior
from kivy.properties import ListProperty, NumericProperty
from  kivy.app import App
import os
module_path = os.path.abspath(__file__)
module_dir = os.path.dirname(module_path)
file_path = os.path.join(module_dir, "Navigation.kv")
build = Builder.load_file(file_path)

def getText(string: str):
    string = string.strip("[color=#00000000]").strip("[/color]")
    return string


class NavigationBar(Widget):
    
    background_color = ListProperty([1, 1, 1, 1])
    flag = NumericProperty(0)
    alpha0 = NumericProperty(1)
    alpha1 = NumericProperty(0.3)
    
    def __init__(self, **kwargs):  
        super().__init__(**kwargs)
        
    def get_pic(self, *args):
        if self.flag == 0:
            return (
                "./res/home_16dp_5F6368_FILL1_wght400_GRAD0_opsz20.png",
                "./res/info_16dp_5F6368_FILL0_wght400_GRAD0_opsz20.png"
            )
        if self.flag == 1:
            return (
                "./res/home_16dp_5F6368_FILL0_wght400_GRAD0_opsz20.png",
                "./res/info_16dp_5F6368_FILL1_wght400_GRAD0_opsz20.png"
            )

        
class RippleButton(TouchRippleButtonBehavior, Label):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_press_func(self):
        pass
    
    def on_release_func(self):
        text = getText(self.text)
        if text == "btn0":
            print("123")
            self.parent.parent.flag = 0
            Animation(alpha0=1, duration=0.5, t='out_cubic').start(self.parent.parent)
            Animation(alpha1=0.3, duration=0.5, t='in_cubic').start(self.parent.parent)
        else:
            self.parent.parent.flag = 1
            Animation(alpha0=0.3, duration=0.5, t='in_cubic').start(self.parent.parent)
            Animation(alpha1=1, duration=0.5, t='out_cubic').start(self.parent.parent)
        

if __name__ == "__main__":
    # build = Builder.load_file(file_path)
    
    fl = FloatLayout()
    class Test(App):
        def build(self):
            return build
        
        def run(self):
            
            return super().run()
    
    Test().run()
