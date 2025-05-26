[app]
title = Save a Life
package.name = savealife
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
osx.python_version = 3
# Android specific
android.api = 31
android.sdk = 31
android.ndk = 23b
android.ndk_api = 21
android.minapi = 21
android.permissions = INTERNET
android.sdk_path = $HOME/android-sdk


[buildozer]
log_level = 2
warn_on_root = 0
