[app]

# -------------------------------------------------
# APP INFO
# -------------------------------------------------
title = GPS Enterprise Collector
package.name = gpscollector
package.domain = com.sanjoy.enterprise

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,bin

version = 1.0.0

requirements = python3,kivy,plyer,requests,sqlite3

orientation = portrait

fullscreen = 0

# Android API (stable for Android 15–16)
android.api = 34
android.minapi = 24
android.sdk = 34
android.ndk = 25b

# -------------------------------------------------
# PERMISSIONS (ENTERPRISE SET)
# -------------------------------------------------
android.permissions = 
    INTERNET,
    ACCESS_FINE_LOCATION,
    ACCESS_COARSE_LOCATION,
    ACCESS_BACKGROUND_LOCATION,
    WRITE_EXTERNAL_STORAGE,
    READ_EXTERNAL_STORAGE,
    MANAGE_EXTERNAL_STORAGE,
    ACCESS_NETWORK_STATE,
    CAMERA

# Needed for Android 13+
android.enable_androidx = True

# -------------------------------------------------
# EMAIL + INTENT SUPPORT
# -------------------------------------------------
android.gradle_dependencies = androidx.core:core:1.12.0

# -------------------------------------------------
# MAPPLS SUPPORT
# -------------------------------------------------
android.meta_data = 
    com.mappls.sdk.key=YOUR_MAPPLS_STATIC_KEY

# -------------------------------------------------
# ICON / SPLASH (optional)
# -------------------------------------------------
# icon.filename = icon.png
# presplash.filename = presplash.png

# -------------------------------------------------
# LOGGING (ADMIN FUNCTION SUPPORT)
# -------------------------------------------------
log_level = 2

# -------------------------------------------------
# STORAGE LOCATION
# -------------------------------------------------
android.private_storage = False

# -------------------------------------------------
# GIST / FILE ACCESS SUPPORT
# -------------------------------------------------
android.allow_backup = True

# -------------------------------------------------
# PYTHON SETTINGS
# -------------------------------------------------
p4a.branch = master
p4a.bootstrap = sdl2

# -------------------------------------------------
# ARCHITECTURE
# -------------------------------------------------
android.archs = arm64-v8a, armeabi-v7a

# -------------------------------------------------
# OPTIMIZATION (ENTERPRISE STABILITY)
# -------------------------------------------------
android.release_artifact = apk
android.debug = False

# Avoid random crashes
android.add_compile_options = "-Xlint:none"

# -------------------------------------------------
# SERVICES (future reliability layer ready)
# -------------------------------------------------
# android.services = GPSService:services/gpsservice.py

# -------------------------------------------------
# BUILD OPTIONS
# -------------------------------------------------
warn_on_root = 0

[buildozer]

log_level = 2
warn_on_root = 0