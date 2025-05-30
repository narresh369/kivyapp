[app]
title = My Kivy App
package.name = mykivyapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,js,css
#source.include_patterns = map.html, *.js, *.css, assets/*
source.include_patterns = assets/*

version = 1.0
requirements = python3,kivy,requests,certifi,pyjnius
orientation = portrait
osx.python_version = 3
android.target = 33
android.api = 33
android.minapi = 21
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION
android.private_storage = True
android.add_assets = content/assets/

[buildozer]
log_level = 2
warn_on_root = 0
