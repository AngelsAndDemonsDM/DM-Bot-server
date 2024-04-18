@echo off
set "PDIR=%~dp0"
cd /d "%PDIR%"

title DM-Bot build master main

del DM-Bot /q
python -m nuitka --remove-output --jobs=4 --standalone --no-pyi-file --windows-icon-from-ico=Sprites.DM-Bot/icons/exe-main-icon.png Code.DM-Bot/main.py
ren main.dist DM-Bot

python pack.py --file1=DM-Bot --output=DM-Bot

exit
