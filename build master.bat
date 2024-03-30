@echo off
set "PDIR=%~dp0"

cd /d "%PDIR%"

title DM-Bot build master

del DM-Bot.exe /q

python -m nuitka --remove-output --jobs=4 --standalone --onefile --no-pyi-file --windows-icon-from-ico=icon.png Code.DM-Bot/main.py

ren main.exe DM-Bot.exe

pause
