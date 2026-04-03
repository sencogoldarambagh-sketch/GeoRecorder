import os
from datetime import datetime
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from plyer import storagepath

def get_app_dir():
    """Finds a safe internal folder for logs and data."""
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
QUEUE_FILE = os.path.join(APP_DIR, "queue.json")

def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf8") as f:
            f.write(f"{datetime.now()} : {msg}\n")
    except:
        pass

class GeoRecorderApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.status_label = Label(text="SYSTEM READY", color=(0, 1, 0, 1))
        
        # UI Inputs
        self.name_input = TextInput(hint_text="Customer Name", size_hint_y=None, height=50)
        root.add_widget(self.name_input)
        
        # Save Button
        save_btn = Button(text="SAVE RECORD", size_hint_y=None, height=60, background_color=(0.2, 0.6, 1, 1))
        save_btn.bind(on_press=self.simple_save)
        
        root.add_widget(save_btn)
        root.add_widget(self.status_label)
        return root

    def simple_save(self, instance):
        log(f"Manual Save Triggered for: {self.name_input.text}")
        self.status_label.text = "RECORD SAVED LOCALLY"
        Clock.schedule_once(lambda dt: self.reset_status(), 3)

    def reset_status(self):
        self.status_label.text = "SYSTEM READY"

if __name__ == "__main__":
    GeoRecorderApp().run()
