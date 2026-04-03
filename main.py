# ==========================================================
# GEORECORDER — ENTERPRISE STABLE VERSION (RE-MATCHED)
# ==========================================================

import os
import json
import threading
import webbrowser
from datetime import datetime
from urllib.parse import quote

from kivy.app import App
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from plyer import storagepath

# Android-specific imports
if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    from android.storage import app_storage_path
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')

# ==========================================================
# STORAGE PATHS & LOGGING
# ==========================================================

def get_app_dir():
    try:
        # Try public documents first
        path = os.path.join(storagepath.get_documents_dir(), "GeoRecorder")
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path
    except Exception:
        # Fallback to internal app storage if permission denied
        path = os.path.join(app_storage_path(), "GeoRecorder")
        os.makedirs(path, exist_ok=True)
        return path

APP_DIR = get_app_dir()
DB_FILE = os.path.join(APP_DIR, "records.json")
QUEUE_FILE = os.path.join(APP_DIR, "queue.json")
LOG_FILE = os.path.join(APP_DIR, "georecorder.log")

def log(msg):
    with open(LOG_FILE, "a", encoding="utf8") as f:
        f.write(f"{datetime.now()} : {msg}\n")

# ==========================================================
# RELIABILITY QUEUE
# ==========================================================

class ReliabilityLayer:
    def __init__(self):
        self.lock = threading.Lock()
        if not os.path.exists(QUEUE_FILE):
            self._write([])

    def _read(self):
        try:
            with open(QUEUE_FILE, "r", encoding="utf8") as f:
                return json.load(f)
        except:
            return []

    def _write(self, data):
        with open(QUEUE_FILE, "w", encoding="utf8") as f:
            json.dump(data, f, indent=2)

    def add(self, record):
        with self.lock:
            data = self._read()
            data.append(record)
            self._write(data)
        log("Record queued")

    def export_bin(self):
        src = self._read()
        path = os.path.join(APP_DIR, "export.bin")
        with open(path, "wb") as f:
            f.write(json.dumps(src).encode("utf8"))
        log(f"BIN exported to {path}")

# ==========================================================
# DATA MODEL
# ==========================================================

class CustomerRecord:
    def __init__(self):
        self.name = ""
        self.phone = ""
        self.status = "NEW"
        self.landmark = ""
        self.pin = ""
        self.address = ""

# ==========================================================
# MAIN APP
# ==========================================================

class GeoRecorderApp(App):

    def build(self):
        self.record = CustomerRecord()
        self.reliability = ReliabilityLayer()
        self.current_lat = 0.0
        self.current_lon = 0.0

        # Initial Permission Request
        if platform == 'android':
            self.request_android_permissions()

        root = BoxLayout(orientation="vertical", padding=8, spacing=6)

        # ---------------- INPUTS ----------------
        self.name_input = TextInput(hint_text="NAME", size_hint_y=None, height=45)
        self.phone_input = TextInput(hint_text="PHONE", input_filter="int", size_hint_y=None, height=45)
        self.landmark_input = TextInput(hint_text="LANDMARK", size_hint_y=None, height=45)
        self.pin_input = TextInput(hint_text="PIN CODE", input_filter="int", size_hint_y=None, height=45)
        self.address_input = TextInput(hint_text="DETAILED ADDRESS", size_hint_y=None, height=80)

        root.add_widget(self.name_input)
        root.add_widget(self.phone_input)
        root.add_widget(self.landmark_input)
        root.add_widget(self.pin_input)
        root.add_widget(self.address_input)

        # ---------------- STATUS BUTTONS ----------------
        status_box = BoxLayout(size_hint_y=None, height=50)
        for s in ["ACTIVE", "DORMANT", "NEW"]:
            btn = ToggleButton(text=s, group="status", state='down' if s == "NEW" else 'normal')
            btn.bind(on_press=self.set_status)
            status_box.add_widget(btn)
        root.add_widget(status_box)

        # ---------------- ACTION BUTTONS ----------------
        root.add_widget(self.make_btn("SAVE RECORD", self.save_record))
        root.add_widget(self.make_btn("SEARCH NEARBY", self.search_nearby))
        root.add_widget(self.make_btn("NAVIGATE", self.navigate))
        root.add_widget(self.make_btn("EMAIL REPORT", self.send_email))
        root.add_widget(self.make_btn("ADMIN PANEL", self.open_admin))

        self.status_label = Label(text="SYSTEM READY", color=(0, 1, 0, 1))
        root.add_widget(self.status_label)

        return root

    def make_btn(self, text, fn):
        b = Button(text=text, size_hint_y=None, height=55, background_color=(0.2, 0.6, 1, 1))
        b.bind(on_press=fn)
        return b

    def set_status(self, btn):
        self.record.status = btn.text

    def request_android_permissions(self):
        # First request Foreground Location
        request_permissions([
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION
        ], self.check_background_permission)

    def check_background_permission(self, permissions, grants):
        if all(grants):
            # Then request Background Location separately
            request_permissions([Permission.ACCESS_BACKGROUND_LOCATION])
            log("Foreground permissions granted. Requesting Background...")

    def save_record(self, *_):
        data = {
            "name": self.name_input.text,
            "phone": self.phone_input.text,
            "status": self.record.status,
            "landmark": self.landmark_input.text,
            "pin": self.pin_input.text,
            "address": self.address_input.text,
            "lat": self.current_lat,
            "lon": self.current_lon,
            "time": datetime.now().isoformat()
        }
        self.reliability.add(data)
        self.status_label.text = f"Saved to Queue at {datetime.now().strftime('%H:%M')}"
        Clock.schedule_once(lambda dt: self.reset_status(), 3)

    def reset_status(self):
        self.status_label.text = "SYSTEM READY"

    def search_nearby(self, *_):
        webbrowser.open(f"https://www.google.com/maps/search/?api=1&query={self.current_lat},{self.current_lon}")

    def navigate(self, *_):
        webbrowser.open(f"https://www.google.com/maps/dir/?api=1&destination={self.current_lat},{self.current_lon}")

    def send_email(self, *_):
        if platform != 'android': return
        
        subject = f"GeoRecorder Report: {self.name_input.text}"
        body = f"Name: {self.name_input.text}\nStatus: {self.record.status}\nCoords: {self.current_lat}, {self.current_lon}"
        uri = f"mailto:?subject={quote(subject)}&body={quote(body)}"
        
        intent = Intent(Intent.ACTION_VIEW)
        intent.setData(Uri.parse(uri))
        PythonActivity.mActivity.startActivity(intent)

    def open_admin(self, *_):
        box = BoxLayout(orientation="vertical", spacing=10, padding=10)
        
        btn_export = Button(text="EXPORT DATA (.BIN)")
        btn_export.bind(on_press=lambda x: self.reliability.export_bin())
        
        btn_clear = Button(text="CLEAR LOCAL LOGS", background_color=(1, 0, 0, 1))
        btn_clear.bind(on_press=lambda x: self.clear_logs())

        box.add_widget(btn_export)
        box.add_widget(btn_clear)

        popup = Popup(title="Admin Controls", content=box, size_hint=(0.8, 0.4))
        popup.open()

    def clear_logs(self):
        with open(LOG_FILE, "w") as f: f.close()
        self.status_label.text = "Logs Cleared"

if __name__ == "__main__":
    GeoRecorderApp().run()
