import os
from datetime import datetime
from kivy.app import App
from kivy.utils import platform as kivy_platform
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# Get app directory (works on both Android and Desktop)
def get_app_dir():
    if kivy_platform == 'android':
        from android.storage import app_storage_path
        base_path = app_storage_path()
    else:
        base_path = os.getcwd()
    
    app_dir = os.path.join(base_path, "GeoRecorder")
    os.makedirs(app_dir, exist_ok=True)
    return app_dir


APP_DIR = get_app_dir()
LOG_FILE = os.path.join(APP_DIR, "georecorder.log")


def log(msg):
    """Simple logging function that works on Android"""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : {msg}\n")
        print(msg)  # Also print to console for debugging
    except Exception as e:
        print(f"Logging failed: {e}")


class GeoRecorderApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # Title
        title = Label(
            text="GeoRecorder",
            font_size="28sp",
            bold=True,
            size_hint_y=None,
            height=60
        )

        # Status label
        self.status = Label(
            text="READY",
            font_size="20sp",
            color=(0, 1, 0, 1)  # Green color
        )

        # Test button
        btn = Button(
            text="TEST STORAGE & LOG",
            size_hint_y=None,
            height=100,
            font_size="18sp"
        )
        btn.bind(on_press=self.test_action)

        # Add widgets
        root.add_widget(title)
        root.add_widget(self.status)
        root.add_widget(btn)

        # Initial log
        log("App started successfully")
        
        return root

    def test_action(self, instance):
        """Called when button is pressed"""
        log("Button pressed - Storage and logging test successful")
        self.status.text = "LOG WRITTEN SUCCESSFULLY ✓"
        self.status.color = (0, 1, 0, 1)  # Green


if __name__ == "__main__":
    GeoRecorderApp().run()
