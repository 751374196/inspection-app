[app]
title = 检测设备采数APP
package.name = inspection_app

source.dir = .

source.include_exts = py,png,jpg,kv,atlas,ttf,ttc,json,sql,db
source.exclude_exts = spec,pyc

version = 1.0.0

android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

android.archs = armeabi-v7a, arm64-v8a

android.minapi = 21
android.targetapi = 33

android.numeric_version = 20240101

android.presplash_color = #FFFFFF
android.presplash_filename = assets/presplash.png

android.icon = assets/icon.png

android.entrypoint = org.kivy.android.PythonActivity

android.whitelist = google.com, google.com.*

android.minsdk = 21

[buildozer]
log_level = 2

[android]

# Disable Cython deprecation warnings
android.gradle_dependencies =
    com.github.cython:cython-android:0.3.0
require = python3,kivy,pyjnius,kivyandroid,pygments,pytesseract,pillow,opencv-python-headless,pyodbc,pymysql,reportlab,beautifulsoup4,lxml,numpy

android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

android.allow_backup = False

[app:android]
fullscreen = 0
orientation = portrait

[app:android.private]
include_assets = 1
include_resources = 1

[app:android.debug]
signing.debug = yes

[app:android.release]
signing.release = yes

[macos]
require = python3,kivy

[windows]
require = python3,kivy,pytesseract,pillow,opencv-python-headless,pyodbc,pymysql

[linux]
require = python3,kivy,pytesseract,pillow,opencv-python-headless,pyodbc,pymysql
