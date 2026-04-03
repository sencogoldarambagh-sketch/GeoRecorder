[app]
title = GeoRecorder
package.name = georecorder
package.domain = org.sanjoy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# 1. Cleaned Requirements
requirements = python3,kivy==2.3.0,plyer,pyjnius,android

# 2. Single-line Permissions (No spaces after commas!)
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,ACCESS_NETWORK_STATE,CAMERA,FOREGROUND_SERVICE

# 3. Critical Build Settings
android.api = 33
android.minapi = 24
android.ndk = 25b
android.enable_androidx = True
android.accept_sdk_license = True
android.skip_update = False

# 4. Architecture support
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
