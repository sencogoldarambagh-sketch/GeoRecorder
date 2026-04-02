# ==========================================================
# GEORECORDER — ENTERPRISE STABLE VERSION
# ==========================================================

import os
import json
import threading
import webbrowser
from datetime import datetime
from urllib.parse import quote

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from plyer import storagepath

from jnius import autoclass
from android.permissions import request_permissions, Permission

# ==========================================================
# ANDROID CLASSES
# ==========================================================

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')

# ==========================================================
# STORAGE PATHS
# ==========================================================

APP_DIR = os.path.join(storagepath.get_documents_dir(), "GeoRecorder")
os.makedirs(APP_DIR, exist_ok=True)

DB_FILE = os.path.join(APP_DIR, "records.json")
QUEUE_FILE = os.path.join(APP_DIR, "queue.json")
LOG_FILE = os.path.join(APP_DIR, "georecorder.log")

# ==========================================================
# LOGGER
# ==========================================================

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
        with open(QUEUE_FILE, "r", encoding="utf8") as f:
            return json.load(f)

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
        log("BIN exported")


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

    # ------------------------------------------------------

    def build(self):

        self.record = CustomerRecord()
        self.reliability = ReliabilityLayer()

        self.current_lat = 0.0
        self.current_lon = 0.0

        request_permissions([
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION,
            Permission.ACCESS_BACKGROUND_LOCATION
        ])

        self.start_foreground_service()

        root = BoxLayout(orientation="vertical", padding=8, spacing=6)

        # ---------------- INPUTS ----------------

        self.name_input = TextInput(
            hint_text="NAME",
            size_hint_y=None,
            height=45
        )

        self.phone_input = TextInput(
            hint_text="PHONE",
            input_filter="int",
            size_hint_y=None,
            height=45
        )

        self.landmark_input = TextInput(
            hint_text="LANDMARK",
            size_hint_y=None,
            height=45
        )

        self.pin_input = TextInput(
            hint_text="PIN CODE",
            input_filter="int",
            size_hint_y=None,
            height=45
        )

        self.address_input = TextInput(
            hint_text="DETAILED ADDRESS",
            size_hint_y=None,
            height=80
        )

        root.add_widget(self.name_input)
        root.add_widget(self.phone_input)
        root.add_widget(self.landmark_input)
        root.add_widget(self.pin_input)
        root.add_widget(self.address_input)

        # ---------------- STATUS BUTTONS ----------------

        status_box = BoxLayout(size_hint_y=None, height=50)

        self.status_buttons = {}
        for s in ["ACTIVE", "DORMANT", "NEW"]:
            btn = ToggleButton(text=s, group="status")
            btn.bind(on_press=self.set_status)
            status_box.add_widget(btn)
            self.status_buttons[s] = btn

        root.add_widget(status_box)

        # ---------------- ACTION BUTTONS ----------------

        root.add_widget(self.make_btn("SAVE", self.save_record))
        root.add_widget(self.make_btn("SEARCH NEARBY", self.search_nearby))
        root.add_widget(self.make_btn("NAVIGATE", self.navigate))
        root.add_widget(self.make_btn("EMAIL REPORT", self.send_email))
        root.add_widget(self.make_btn("ADMIN", self.open_admin))

        self.status_label = Label(text="READY")
        root.add_widget(self.status_label)

        return root

    # ------------------------------------------------------

    def make_btn(self, text, fn):
        b = Button(text=text, size_hint_y=None, height=50)
        b.bind(on_press=fn)
        return b

    # ------------------------------------------------------

    def set_status(self, btn):
        self.record.status = btn.text

    # ------------------------------------------------------
    # FOREGROUND SERVICE START
    # ------------------------------------------------------

    def start_foreground_service(self):
        try:
            service = autoclass(
                'org.sanjoy.georecorder.LocationForegroundService'
            )
            activity = PythonActivity.mActivity
            intent = Intent(activity, service)
            activity.startForegroundService(intent)
            log("Foreground service started")
        except Exception as e:
            log(f"Service start error {e}")

    # ------------------------------------------------------
    # SAVE RECORD
    # ------------------------------------------------------

    def save_record(self, *_):

        self.record.name = self.name_input.text
        self.record.phone = self.phone_input.text
        self.record.landmark = self.landmark_input.text
        self.record.pin = self.pin_input.text
        self.record.address = self.address_input.text

        data = {
            "name": self.record.name,
            "phone": self.record.phone,
            "status": self.record.status,
            "landmark": self.record.landmark,
            "pin": self.record.pin,
            "address": self.record.address,
            "lat": self.current_lat,
            "lon": self.current_lon,
            "time": datetime.now().isoformat()
        }

        self.reliability.add(data)

        self.status_label.text = "Saved ✓"

    # ------------------------------------------------------
    # MAP FEATURES
    # ------------------------------------------------------

    def search_nearby(self, *_):
        webbrowser.open(
            f"https://www.google.com/maps/search/?api=1&query={self.current_lat},{self.current_lon}"
        )

    def navigate(self, *_):
        webbrowser.open(
            f"https://www.google.com/maps/dir/?api=1&destination={self.current_lat},{self.current_lon}"
        )

    # ------------------------------------------------------
    # EMAIL REPORT
    # ------------------------------------------------------

    def send_email(self, *_):

        subject = f"GeoRecorder {datetime.now():%d-%m-%Y %H:%M}"

        body = f"""
NAME: {self.record.name}
PHONE: {self.record.phone}
STATUS: {self.record.status}

LANDMARK: {self.record.landmark}
PIN: {self.record.pin}
ADDRESS:
{self.record.address}

LAT: {self.current_lat}
LON: {self.current_lon}
"""

        uri = f"mailto:?subject={quote(subject)}&body={quote(body)}"

        intent = Intent(Intent.ACTION_VIEW)
        intent.setData(Uri.parse(uri))
        PythonActivity.mActivity.startActivity(intent)

    # ------------------------------------------------------
    # ADMIN PANEL
    # ------------------------------------------------------

    def open_admin(self, *_):

        box = BoxLayout(orientation="vertical", spacing=5)

        export_btn = Button(text="EXPORT .BIN")
        export_btn.bind(on_press=lambda x: self.reliability.export_bin())

        clear_btn = Button(text="CLEAR LOGS")
        clear_btn.bind(on_press=lambda x: self.clear_logs())

        box.add_widget(export_btn)
        box.add_widget(clear_btn)

        Popup(
            title="ADMIN",
            content=box,
            size_hint=(0.8, 0.5)
        ).open()

    def clear_logs(self):
        open(LOG_FILE, "w").close()
        self.status_label.text = "Logs cleared"

# ==========================================================

if __name__ == "__main__":
    GeoRecorderApp().run()