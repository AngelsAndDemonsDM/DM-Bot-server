@echo off
set "PDIR=%~dp0"
cd /d "%PDIR%"

title DM-Bot build master updater
del DM-Bot-updater.exe /q

python -m nuitka --remove-output --jobs=4 --standalone --onefile --no-pyi-file --windows-icon-from-ico=Sprites.DM-Bot/exe-updater-icon.png Updater.DM-Bot/updater_main.py
ren updater_main.exe DM-Bot-updater.exe

exit
