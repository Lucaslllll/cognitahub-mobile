# CognitaHub App

CognitaHub is a mobile application built with **Python + Kivy/KivyMD** designed to help users follow courses, track progress, and manage learning activities.

This repository contains the **mobile version** of the CognitaHub app.

---

## 🧰 Technologies
- Python 3
- Kivy
- KivyMD
- Buildozer (Android)

---

## 📦 Dependencies
- Python 3.x

---

## ▶️ Running locally

1. Stay in the project root directory  
2. Create a virtual environment:

   python3 -m venv venv

3. Activate the virtual environment:

   source venv/bin/activate

4. Install dependencies:

   pip install -r requirements.txt

5. Run the application:

   python3 main.py --size=360x720

You can change the resolution if needed.

---

## 🤖 Build for Android

### System dependencies (Ubuntu / Debian)

sudo apt update  
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
python3-virtualenv autoconf libtool pkg-config zlib1g-dev \
libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev \
libssl-dev automake autopoint gettext

---

### Buildozer setup

Initialize Buildozer:

buildozer init

This will create a buildozer.spec file.  
Edit it and update the following fields:

requirements = python3,kivy,https://github.com/kivymd/KivyMD/archive/master.zip,kaki==0.1.8,materialyoucolor,jnius,plyer,requests-toolbelt,asynckivy,asyncgui

icon.filename = %(source.dir)s/assets/img/desenho-cognitahub.png

build_cython = True  
cythonize_opts = --compiler=c++

source.include_exts = py,png,jpg,kv,atlas,json,svg,ttf  
source.include_patterns = assets/*,assets/img/*,assets/images/*.png,assets/fonts/*

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, READ_MEDIA_VIDEO, READ_MEDIA_IMAGES

android.ndk = 25b  
android.ndk_api = 21  
android.api = 34  
android.minapi = 21

android.add_aapt_options = --setProperty android:requestLegacyExternalStorage=true  
android.add_src = false

android.extra_manifest_application_arguments = ./src/android/extra_manifest_application_arguments.xml

android.archs = armeabi-v7a

You can change android.archs according to your device:
- armeabi-v7a
- arm64-v8a
- x86
- x86_64

---

### Build and run on device

buildozer android debug deploy run

---

## 📱 Supported architectures
- armeabi-v7a
- arm64-v8a
- x86
- x86_64
