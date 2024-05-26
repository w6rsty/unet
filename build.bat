@echo off

rmdir /s /q output

pip install -r requirements.txt

mkdir output

pyinstaller --onefile app.py --noconsole --icon=assets/unet.ico --name=unet

copy dist\unet.exe output\unet.exe

xcopy assets output\assets /E /Y