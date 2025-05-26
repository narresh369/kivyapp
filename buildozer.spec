[app]
title = Save a Life
package.name = savealife
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,pyjnius,https://github.com/kivy/pyjnius/archive/master.zip
orientation = portrait
osx.python_version = 3

# Android specific
## android.api = 31
android.sdk = 31
android.ndk_api = 21
android.minapi = 21
android.permissions = INTERNET
android.sdk_path = /home/runner/android-sdk
android.ndk = 25b
android.ndk_path = /home/runner/android-sdk/ndk/25.2.9519653

android.accept_sdk_license = True
android.skip_update = False

[buildozer]
log_level = 2
warn_on_root = 0
