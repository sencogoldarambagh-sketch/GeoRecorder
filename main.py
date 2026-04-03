import os
from datetime import datetime
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

def get_app_dir():
    if platform == 'android':
        from android.storage import app_storage_path
        path = os.path.join(app_storage_path(), "GeoRecorder")
    else:
        path = os.path.join(os.getcwd(), "GeoRecorder")
    
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

APP_DIR = get_app_dir()
LOG_FILE = os.path.join(APP_DIR, "georecorder.log")

def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf8") as f:
            f.write(f"{datetime.now()} : {msg}\n")
    except:
        pass

class GeoRecorderApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=20)
        self.status = Label(text="READY TO BUILD", font_size='20sp')
        
        btn = Button(text="TEST STORAGE & LOG", size_hint_y=None, height=100)
        btn.bind(on_press=self.test_action)
        
        root.add_widget(self.status)
        root.add_widget(btn)
        return root

    def test_action(self, instance):
        log("Button pressed - App is functional")
        self.status.text = "LOG WRITTEN SUCCESSFULLY"

if __name__ == "__main__":
    GeoRecorderApp().run()
