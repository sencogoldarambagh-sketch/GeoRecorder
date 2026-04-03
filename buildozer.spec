[app]
title = GPS Enterprise Collector
package.name = gpscollector
package.domain = com.sanjoy.enterprise
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,bin
version = 1.0.0

# RE-MATCHED REQUIREMENTS
requirements = python3,kivy==2.3.0,plyer,pyjnius,android

orientation = portrait
fullscreen = 0

# ANDROID SETTINGS
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.enable_androidx = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# RE-MATCHED PERMISSIONS (Formatted for Buildozer)
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,ACCESS_NETWORK_STATE,CAMERA,FOREGROUND_SERVICE

# STABILITY FIXES
android.enable_androidx = True
android.accept_sdk_license = True
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 0
