from init import *


class HelpPopup(FloatLayout):
    
    def ani(self):
        pass
    
    def on_click_callback(self):
        try: 
            # self.parent.remove_widget(self)
            # self.parent.parent.remove_widget(self)
            vtp.root.remove_widget(self)
        except:
            pass
        
helpPopup = Builder.load_file("./Help.kv")
        
if __name__ == "__main__":
    
    vtp.build = lambda *args: helpPopup
    vtp.run()        