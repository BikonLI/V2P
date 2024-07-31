"""
API:

ProcessBar: class
---

    max: int
        The max process.

    current: int
        The current process.

    proportion: float
        The rate. This value should always between 0 ~ 1.05.

    background_width: 
        The background line's width.
    
    line_width:
        The processing line's width.

    background_color:
        The background line's color.
    
    line_color:
        The processing line's color.

    background_cap:
        "none", "round", "square", "none" is default and reconmended.
        https://kivy.org/doc/stable/_images/line-instruction.png
    
    line_cap:
        "none", "round", "square", "none" is default and reconmended.
        https://kivy.org/doc/stable/_images/line-instruction.png

"""

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, BoundedNumericProperty, OptionProperty

import os
module_path = os.path.abspath(__file__)  
module_dir = os.path.dirname(module_path)  
file_path = os.path.join(module_dir, "ProcessBar.kv")  
build = Builder.load_file(file_path)


class ProcessBar(Widget):

    max = NumericProperty(1000)
    current = NumericProperty(0)
    proportion = BoundedNumericProperty(0, min=0, max=1.05)
    background_width = NumericProperty(10)
    line_width = NumericProperty(10)
    background_color: ListProperty = ListProperty([1, 1, 1, 1])
    line_color: ListProperty = ListProperty([])
    background_cap = OptionProperty("none", options=["none", "round", "square"])
    line_cap = OptionProperty("none", options=["none", "round", "square"])

    def __init__(self, max=None, current=None, background_width=None, line_width=None, background_color=None, line_color=None, background_cap=None, line_cap=None, **kwargs):
        self.max = max if max else 1000
        self.current = current if current else 0
        self.background_width = background_width if background_width else 10
        self.line_width = line_width if line_width else 10
        self.background_color = background_color if background_color  else [1, 1, 1, 1]
        self.line_color = line_color if line_color else [0, 1, 0, 1]
        self.background_cap = background_cap if background_cap else "none"
        self.line_cap = line_cap if line_cap else "none"
        super().__init__(**kwargs)

    def on_current(self, *args, **kwargs):
        if self.proportion <= 1.05:
            self.proportion = self.current / self.max
    
    def on_max(self, *args, **kwargs):
        if self.proportion <= 1.05:
            self.proportion = self.current / self.max


if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.uix.floatlayout import FloatLayout
    class Test(App):
        def build(self):
            def p(*args):
                pcb.proportion += 0.05
            bx = FloatLayout()
            bx.add_widget(Button(
                size = (200, 200),
                pos = (0, 0),
                on_press = p
            ))
            bx.add_widget(pcb := ProcessBar(
                size=(1000, 20),
                size_hint=(None, None),
                pos_hint = {'center_x': 0.5,'center_y': 0.5}
            ))
            return bx
    Test().run()
