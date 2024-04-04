@echo off
set "PDIR=%~dp0"
cd /d "%PDIR%"

title DM-Bot build master main
del DM-Bot.exe /q

python -m nuitka --remove-output --jobs=4 --standalone --onefile --no-pyi-file --windows-icon-from-ico=Sprites.DM-Bot/exe-main-icon.png Code.DM-Bot/main.py
ren main.exe DM-Bot.exe

python create_zip.py --name=DM-Bot.exe

exit
