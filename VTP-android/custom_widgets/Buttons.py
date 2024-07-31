"""
API:

FilledButton: class
---

    background_color: rgba
        The color of the button while not pressing. This should always be (0, 0, 0, 0)
        to keep alpha in zero.

    filled_color: rgba
        The color of FilledButton while not pressing.

    filled_color_down: rgba
        The color of FilledButton while pressing.
    
    text: str
        The words that display on the FilledButton.

    on_press: Callback
        This method will callback when the button is pressed.
        
"""
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty
import os
module_path = os.path.abspath(__file__)  
module_dir = os.path.dirname(module_path)  
file_path = os.path.join(module_dir, "Buttons.kv")  
build = Builder.load_file(file_path)


class FilledButton(Button):

    background_color = (0, 0, 0, 0)  # Do not set this property to any other value.
    filled_color = ListProperty((1, 1, 1, 1))
    filled_color_down = ListProperty((0.8, 0.8, 0.8, 0.8))

    def __init__(self, filled_color=None, filled_color_down=None, **kwargs):
        self.filled_color = filled_color if filled_color else (0, 0, 0, 0)
        self.filled_color_down = filled_color_down if filled_color_down else (
            self.filled_color[0],
            self.filled_color[1],
            self.filled_color[2],
            self.filled_color[3] / 2,
        )
        super().__init__(**kwargs)


class TextButton(Button):
    outline_color = ListProperty([0, 0, 1, 1])
    disabled_color = ListProperty([0, 0, 0, 1])
    background_color = (0, 0, 0 ,0)
    filled_color = ListProperty((1, 1, 1, 1))
    filled_color_down = ListProperty((0.8, 0.8, 0.8, 1))
    btn_text = StringProperty("")
    
    def __init__(self, btn_text=None, outline_color=None, filled_color=None, filled_color_down=None, disabled_color=None, **kwargs):
        self.outline_color = outline_color if outline_color else [0, 0, 1, 1]
        self.filled_color = filled_color if filled_color else (1, 1, 1, 1)
        self.filled_color_down = filled_color_down if filled_color_down else (0.8, 0.8, 0.8, 1)
        self.btn_text = btn_text if btn_text else ""
        super().__init__(**kwargs)


if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.label import Label


    fl = FloatLayout()
    class Test(App):
        def build(self):
            fl.add_widget(FilledButton(
                text="Filled Button", 
                pos_hint={"center_x": 0.5, "center_y": 0.75}, 
                filled_color=(0.5, 0.5, 0.7, 1), 
            ))
            fl.add_widget(TextButton(
                size = (200, 65),
                size_hint = (None, None),
                pos_hint = {"center_x": 0.5, "center_y": 0.25}, 
            ))
            return fl
    Test().run()

    print
