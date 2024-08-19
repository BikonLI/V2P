# utf-8
from init import *
from Help import helpPopup

videoExtract: VideoExtract = VideoExtract('')
"Global v"

def isVideo(filePath):
    if filePath:
            head, ext = os.path.splitext(filePath)

            if ext in ['.mkv', '.mp4', '.mov', '.avi', '.wmv', '.avi', '.3gp']:
                isShow = True
            else: isShow = False
    else: isShow = False
    return isShow
    

class ExtractPage(MDFloatLayout):
    pass


class ChooseFileButton(ButtonBehavior, Label):
    
    filePath = StringProperty('')
    textColor = ColorProperty((0, 0, 0, 1))
    fresh: callable = lambda *args: None
    fresh1: callable = lambda *args: None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enable()

    def on_press(self):
        self.filePath = ''
        Clock.schedule_once(self.disable)
        self.chooseFile()
        Clock.schedule_once(self.enable, 2)
        return super().on_press()
    
    def enable(self, *args):
        self.chooseFile = self.__chooseFile
        
    def disable(self, *args):
        self.chooseFile = lambda *args: None
    
    def chooseFile(self, *args):
        pass
    
    def __chooseFile(self, *args):
        filechooser.open_file(on_selection=self.__on_selection)
    
    def __on_selection(self, selections):
        if selections:
            self.filePath = selections[0]
            self.refresh()
            
    def refresh(self):
        Clock.schedule_once(self.fresh)
        Clock.schedule_once(self.fresh1)
        
        
    def enDisable(self, ifShow):
        color = (0, 0, 0, 1) if ifShow else (0, 0, 0, 0)
        ani = Animation(textColor=color, duration=1.5)

        ani.start(self)
        

class FileIcon(MDFloatLayout):
    
    value = BoundedNumericProperty(0)  # 0 ~ 1
    
    def displayText(self, filePath):
        path, name = os.path.split(filePath)
        
        self.ids["label"].text = name
        
        self.flashProgressBar()
        self.getTotalFrame(filePath)
    
    def flashProgress(self, value):
        pass
    
    def flashProgressBar(self):
        self.value = 0
        def setValue(*args):
            self.value += 1
        def flash(*args):
            for i in range(100):
                if self.value <= 100:
                    Clock.schedule_once(setValue)
                    time.sleep(0.02)
        thread = threading.Thread(target=flash)
        Clock.schedule_once(lambda *args: thread.start(), 1)
        
    def getTotalFrame(self, videoPath):
        global videoExtract
        videoExtract = VideoExtract(videoPath)
        thread = threading.Thread(target=videoExtract.getTotalFrame)
        thread.start()


class ChooseBox(FloatLayout):
    
    aniColor = ColorProperty((1, 1, 1, 0))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notChoose = ChooseFileButton(size_hint=(1, 1), pos_hint={"center_x": .5, "center_y": .5})
        self.yesChoose = FileIcon(size_hint=(1, 1), pos_hint={"center_x": .5, "center_y": .5})
        self.add_widget(self.notChoose)
        
    def display(self, filePath):
        isShow = isVideo(filePath)
        if isShow:
            self.notChoose.textColor =  (0, 0, 0, 0)
            self.notChoose.enDisable(not isShow)
            self.aniColor = (1, 1, 1, 1)
            
            ani = Animation(aniColor=(1, 1, 1, 0), duration=0.5, transition='in_back')
            ani.start(self)
            
            self.clear_widgets()
            self.add_widget(self.notChoose)
            self.add_widget(self.yesChoose)
            
            self.yesChoose.displayText(filePath)
        else:
            self.notChoose.textColor = (0, 0, 0, 0)
            self.notChoose.enDisable(not isShow)
            
            self.clear_widgets()
            self.add_widget(self.notChoose)
            
            
        
class MenuHeader(MDBoxLayout):    
    text = StringProperty('')
    icon = StringProperty('')

    
class ConfigDropDown(ButtonBehavior, MDLabel):
    
    itemsList: 'ListProperty[str]' = ListProperty([])
    menu: MDDropdownMenu = None
    menuHeader: MenuHeader = None
    menuHeaderText = StringProperty('')
    menuHeaderIcon = StringProperty('')
    hor_growth = "left"
    ver_growth = "down"
    position = "bottom"
    menuWidth = 300
    offset_x = BoundedNumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        items = []
        self.menuHeader = MenuHeader(
                text=self.menuHeaderText,
                icon = self.menuHeaderIcon
            )

        self.menu = MDDropdownMenu(
            header_cls = self.menuHeader,
            caller = self, 
            items = items, 
            position = self.position, 
            hor_growth = self.hor_growth, 
            ver_growth = self.ver_growth, 
            width = self.menuWidth
        )

    def on_menuHeaderIcon(self, *args):
        self.menuHeader.icon = self.menuHeaderIcon
        
    def on_menuHeaderText(self, *args):
        self.menuHeader.text = self.menuHeaderText
        
    def openMenu(self):
        items = [
            {
                "text": item,
                "on_release": lambda item=item: self.menuDismiss(item),
                "leading_icon": "check" if self.text == item else '',
                "leading_icon_color": "orange",
            } for item in self.itemsList]

        self.menu.items = items
        self.menu.open()
        
    def menuDismiss(self, text):
        self.text = text
        Clock.schedule_once(lambda *args: self.menu.dismiss(), 0.1)
        
        
class ExtractProgressIndicator(MDLinearProgressIndicator):
    coverColor = ColorProperty((1, 1, 1, 1))

        
class Extract(TouchRippleButtonBehavior, Label):
    
    ifShow = BooleanProperty(False)
    isExtracting = BooleanProperty(False)
    textColor = ColorProperty((0, 0, 0, 1))
    buttonColor = ColorProperty(get_color_from_hex("#626567"))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progressIndicator = ExtractProgressIndicator()
        
    def enDisable(self, ifShow):
        if ifShow:
            self.functionality = self.__functionality
            self.__rippleEnabled()
            ani = Animation(textColor=get_color_from_hex("#000000FF"), buttonColor=get_color_from_hex("#5cade2"), duration=1, t='in_back')
            ani.start(self)
            return True
            
        else:
            self.ifShow = False
            self.functionality = lambda: None
            self.__rippleDisabled()
            ani = Animation(textColor=get_color_from_hex("#909497"), buttonColor=get_color_from_hex("#626567"), duration=1, t='out_back')
            ani.start(self)
            return False
        
    def remove_progress_bar(self, *args):
        extractarea.remove_widget(self.progressIndicator)

    def __functionality(self):
        global videoExtract
        configs: dict[str: any] = getConfig()

        size = configs.get("size")
        rate = configs.get("frame")
        format = configs.get("format")
        spin = configs.get("spin")
        path = configs.get("extractPlace")
        
        def flash(*args):
            videoExtract.total_frame = configs.get("totalFrame") if configs.get("totalFrame") else 100
            self.progressIndicator.value = videoExtract.count / videoExtract.total_frame * 100
        Clock.schedule_interval(flash, 0.3)
        
        def func(*args):
            def inner(*args):
                self.isExtracting = False
            
            ani = Animation(coverColor=get_color_from_hex("#FFFFFFFF"), duration=1)
            
            Clock.schedule_once(lambda *args: ani.start(self.progressIndicator))
            Clock.schedule_once(inner) 
            Clock.schedule_once(self.remove_progress_bar, 2)
            Clock.schedule_once(lambda *args: self.enDisable(isVideo(getConfig()["videoPath"])), .5)
        
        thread = threading.Thread(target=lambda *args: videoExtract.start(size, rate, format, spin, path, func))
        
        extractarea.remove_widget(self.progressIndicator)
        ani = Animation(coverColor=get_color_from_hex("#00000000"), duration=1)
        extractarea.add_widget(self.progressIndicator)
        ani.start(widget=self.progressIndicator)
        
        Clock.schedule_once(lambda *args: thread.start(), 1.5)
        
    def on_press(self):
        def disable(*args):
            self.functionality = lambda *args: None
            
        self.functionality()
        
        Clock.schedule_once(disable)
        Clock.schedule_once(lambda *args: self.enDisable(False), 1.5)
        
    def functionality(self):
        pass
    
    def __rippleDisabled(self):
        self.on_touch_down = lambda *args: None
        self.on_touch_up = lambda *args: None
        self.on_touch_move = lambda *args: None
    
    def __rippleEnabled(self):
        self.on_touch_down = super().on_touch_down
        self.on_touch_up = super().on_touch_up
        self.on_touch_move = super().on_touch_move


class ExtractArea(FloatLayout):
    """
        Extract:
        size_hint: .4, .3
        pos_hint: {"right": .5, "center_y": .25}
    """
    
    extract = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extract = Extract()
        self.add_widget(self.extract)
        self.display('')
        
    def display(self, filePath):
        isShow = isVideo(filePath)
        # textColor=get_color_from_hex("#909497"), buttonColor=get_color_from_hex("#626567"
        # self.extract.buttonColor = get_color_from_hex("#626567")
        # self.extract.textColor = get_color_from_hex("#909497")
        self.extract.enDisable(False)
        Clock.schedule_once(lambda *args: self.extract.enDisable(isShow), 3)
        
    def popup(self):
        try:
            vtp.root.add_widget(helpPopup)
        except:
            pass


        
buildInterface = Builder.load_file("./ExtractPage.kv")
choosebox = buildInterface.ids["choosebox"]
extractarea = buildInterface.ids["extract_area"]
choosebox.notChoose.fresh = lambda *args: choosebox.display(choosebox.notChoose.filePath)
choosebox.notChoose.fresh1 = lambda *args: extractarea.display(choosebox.notChoose.filePath)



def getConfig():
    
    chooseFileButton = choosebox.notChoose
    
    c0 = buildInterface.ids['frame'].text
    c1 = buildInterface.ids['size'].text
    c2 = buildInterface.ids['spin'].text
    c3 = buildInterface.ids['fromat'].text
    
    filePath = chooseFileButton.filePath
    frame = c0 if c0 else None
    size = c1 if c1 else None
    spin = c2 if c2 else None
    format = c3 if c3 else None
    
    frame = int(frame) if frame else 1
    spin = int(spin) if spin else 0
    format = format.strip('*') if format else '.jpg'
    
    size0, size1 = size.strip('()').split(', ')
    size = (int(size0), int(size1))
    
    extractPlace = picStoragePath
    
    return {
        "videoPath": filePath,
        "frame": frame,
        "size": size,
        "spin": spin,
        "format": format,
        "extractPlace": extractPlace,
        "totalFrame": videoExtract.total_frame
    }
    
    
if __name__ == "__main__":
    
    vtp.build = lambda *args: buildInterface
    vtp.run()
    print(getConfig())
    