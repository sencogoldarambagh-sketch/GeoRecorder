[app]
title = GeoRecorder
package.name = georecorder
package.domain = org.sanjoy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# Simplified to prevent 14-minute recipe crashes
requirements = python3,kivy==2.3.0,plyer,pyjnius,android

# Single line - no spaces after commas
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,ACCESS_NETWORK_STATE,CAMERA,FOREGROUND_SERVICE

android.api = 33
android.minapi = 24
android.ndk = 25b
android.enable_androidx = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
