"""
API:

Radio: class
---
    selected: kv.bool 
        If Radio is selected.
    
    background_color: rgba
        The color of the whole widget

    radio_color: rgba
        The color of the radio box
    
    radio_selected_color: rgba
        The color that fill in the radio box after it's selected.

    ids["Label"]: Label
        Display info with a sub widget.
    
    on_state_change: Callback
        Callbacks when the radio button (hidding) is pressed. But 
        remenber to call it self first if you overide it.

    duration: float
        A property that determine the duration of select animation.

"""
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Ellipse 
from kivy.properties import BooleanProperty, NumericProperty, ListProperty, StringProperty
from kivy.animation import Animation

import os
module_path = os.path.abspath(__file__)  
module_dir = os.path.dirname(module_path)  
file_path = os.path.join(module_dir, "Selections.kv")  
build = Builder.load_file(file_path)


class Radio(Widget):

    radius = NumericProperty(20)
    background_color = ListProperty((0, 0, 0, 0))
    radio_color = ListProperty((0, 0, 0, 0))
    radio_selected_color = ListProperty((0, 0, 0, 0))
    selected = BooleanProperty(False)
    radius_selected = NumericProperty(0)
    duration = NumericProperty(0.27)

    def __init__(
            self, 
            radius=20, 
            background_color=None, 
            radio_color=None,
            radio_selected_color=None,
            duration=None,
            **kwargs
    ):
        self.radius = radius
        self.background_color = background_color if background_color else (0, 0, 0, 1)
        self.radio_color = radio_color if radio_color else (0, 0, 1, 1)
        self.radio_selected_color = radio_selected_color if radio_selected_color else (0, 1, 0, 1)
        self.state_color = self.background_color
        self.duration = duration if duration else 0.27
        super().__init__(**kwargs)

    def on_state_change(self, **kwargs):
        self.selected = not self.selected
        if self.selected:
            Animation(radius_selected=self.radius * 0.55, t="in_out_back", duration=self.duration).start(self)
        else:
            Animation(radius_selected=0, t="in_out_back", duration=self.duration).start(self)


class Dropdown(FloatLayout):

    outline_color = ListProperty([0, 0, 1, 1])
    background_color = ListProperty([0.5, 0.5, 0.5, 1])
    volumn = NumericProperty(3)
    label = StringProperty("Color")
    chosen = StringProperty("")
    label_pos_hint = NumericProperty(0.3)
    array_color = ListProperty([0.5, 0.5, 0.5, 1])
    other_kw_to_dropdown_list = None
    dropdown_list = None
    text_list = ListProperty(["text1", "text2", "text3"])

    def __init__(self, lable=None, text_list=None, outline_color=None, backgound_color=None, volunm=None, label_pos_hint=None, other_kw_to_dropdown_list=None, **kwargs):
        self.label = lable if lable else "Color"
        self.text_list = text_list if text_list else self.text_list
        self.outline_color = outline_color if  outline_color else [0, 0, 1, 1]
        self.background_color = backgound_color if backgound_color else [0.8, 0.8, 0.8, 1]
        self.volumn = volunm if volunm else 3
        self.label_pos_hint = label_pos_hint if label_pos_hint else 0.3
        self.other_kw_to_dropdown_list = other_kw_to_dropdown_list if other_kw_to_dropdown_list else None
        self.chosen = ""
        super().__init__(**kwargs)

    def show_list(self, *args):
        tp_pos=(self.pos[0] - 2, self.pos[1] + self.size[1] + 10)
        # popup = Popup(
        #     title = '',
        #     size_hint = (None, None),
        #     size = self.size,
        #     background = "",
        #     background_color = (0, 0, 0, 0),
        #     border = (0, 0, 0, 0),
        #     pos = (tp_pos[0], tp_pos[1] - self.size[1]),
        #     auto_dismiss = True
        # )
        # with popup.canvas:
        #     Color(rgba=(1, 0, 0, 1))
        #     Rectangle(size=(500, 500), pos=(500, 500))
        btn = Dropdown_list(
            root = self,
            text_list=self.text_list,
            rows=self.volumn,
            tp_pos=tp_pos,
            background_color=self.background_color,
            button_color=(0.8, 0.8, 0.8, 1),
            size_x=self.size[0] + 10,
            button_height=self.size[1]
        )
        # popup.content = btn
        # popup.open()
        # self.ids["fl"].add_widget(popup)
        self.parent.add_widget(btn)


class Dropdown_list(Widget):

    button_height = NumericProperty(80)
    button_color = ListProperty([0, 0, 1, 1])
    rows = NumericProperty(3)
    tp_pos=ListProperty([0, 0])
    text_list = ListProperty(["text1", "text2", "text3"])
    size_x = NumericProperty(360)
    root = None

    def __init__(self,rows=None, tp_pos=None, size_x=None, root=None, text_list=None, button_height=None, background_color=None, **kwargs):
        self.rows = rows if rows else 3
        self.button_height = button_height if button_height else 80
        self.background_color = background_color if background_color else [1, 1, 1, 1]
        self.tp_pos = tp_pos if tp_pos else (0, 0)
        self.size = (360, self.rows * self.button_height)
        self.text_list = text_list if text_list else ["text1", "text2", "text3"]
        self.option = None
        self.size_x = size_x if size_x else 360
        self.root = root
        super().__init__(**kwargs)

        for i in range(self.rows):
            self.ids["gdt"].add_widget(cell := FloatLayout())
            cell.add_widget(
                btn := Button(
                    background_color = (0, 0, 0, 0),
                    background_normal = "",
                    pos_hint = {"center_x": 0.5, "center_y": 0.5}
                )
                )

            btn.bind(on_release=self.on_release)
            cell.add_widget(Label(
                text = self.text_list[i],
                color = (0, 0, 0, 1),
                pos_hint = {"center_x": 0.5, "center_y": 0.5}
            ))
    def on_release(self, instance):
        self.root.chosen = instance.parent.children[0].text
        self.parent.remove_widget(self)


if __name__ == "__main__":
    from kivy.app import App
    
    from kivy.graphics import Rectangle
    radio = Radio(
                background_color=(1, 1, 1, 1),
                radio_color=(0, 0, 1, 1),
                radio_selected_color=(0.5, 0.5, 0.5, 1)
            )
    radio.pos_hint = {"center_x": 0.5, "center_y": 0.7}

    dropdown = Dropdown(other_kw_to_dropdown_list={"rows": 5, "button_color": (0.7, 0.8, 0.8, 1)}, text_list = ["text0", "text1", "text2", "text3", "text4", "text5"])
    dropdown.pos_hint = {"center_x": 0.5, "center_y": 0.3}

    dropdown_list = Dropdown_list(rows = 3)
    dropdown_list.pos_hint = {"center_x": 0.25, "center_y": 0.5}
    dropdown_list.background_color = (1, 0, 0, 1)

    fl = FloatLayout()
    fl.add_widget(radio)
    fl.add_widget(dropdown)
    # fl.add_widget(dropdown_list)
    fl.size = (1600, 1200)
    with fl.canvas.before:
        Color(rgba=(1, 1, 1, 1))
        Rectangle(size=fl.size, pos=fl.pos)
    
    class Test(App):
        
        def build(self):
            
            return fl
    Test().run()
