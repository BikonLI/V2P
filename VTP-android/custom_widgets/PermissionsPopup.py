from kivy.lang import Builder
from kivy.uix.popup import Popup
import os

module_path = os.path.abspath(__file__)
module_dir = os.path.dirname(module_path)
file_path = os.path.join(module_dir, "PermissionsPopup.kv")
# build = Builder.load_file(file_path)

class PermissionsPopup(Popup):
    
    func = print
    
    def dismiss(self, *_args, **kwargs):
        return super().dismiss(animation=True)
    
    def confirm(self):
        # do smth
        super().dismiss(animation=True)
        self.func()
        # get_external_storage_permission()
    
    def open(self, *args, **kwargs):
        super().open(animation=True)
        
    
Builder.load_file(file_path)
get_storage_permission_popup = PermissionsPopup()
