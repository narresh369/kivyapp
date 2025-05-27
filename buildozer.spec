[app]
title = Save a Life
package.name = savealife
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,git+https://github.com/narresh369/pyjnius.git@master
#requirements = python3,kivy,./libs/pyjnius
orientation = portrait
osx.python_version = 3
# Prevent Buildozer from copying these problematic scripts into the APK
exclude_source = */googletest/scripts/*
#exclude_patterns = */googletest/scripts/gen_gtest_pred_impl.py
exclude_patterns = */tests/*,*/test/*,*/__pycache__/*,*/docs/*,*/examples/*,*/googletest/scripts/*,*/gen_gtest_pred_impl.py


#Android  specific
android.api = 31
#android.sdk = 31
android.ndk_api = 21
android.minapi = 21
android.permissions = INTERNET
android.sdk_path = /home/runner/android-sdk
android.ndk = 25b
android.ndk_path = /home/runner/android-sdk/ndk/25.2.9519653
android.ignore_setup_py = True

android.accept_sdk_license = True
android.skip_update = False

p4a.local_recipes = ./recipes

[buildozer]
log_level = 2
warn_on_root = 0

[hooks]
# Custom shell commands to run before/after build
# prebuild = path/to/script.sh
# postbuild = path/to/script.sh
prebuild = ./patch_googletest.sh

