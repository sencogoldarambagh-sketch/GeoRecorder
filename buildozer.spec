[app]
title = GeoRecorder
package.name = georecorder
package.domain = org.sanjoy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# Keep it minimal — you already did a good job simplifying
requirements = python3,kivy==2.3.0,plyer,pyjnius,android

# Permissions — looks okay, but add POST_NOTIFICATIONS if you ever use notifications
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,ACCESS_NETWORK_STATE,CAMERA,FOREGROUND_SERVICE

android.api = 33
android.minapi = 24
android.ndk = 25b          # This is still the most commonly working version

android.enable_androidx = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
