@echo off
set "PDIR=%~dp0"

cd /d "%PDIR%"

title DM-Bot

python main.py

for /d /r %%d in (__pycache__) do (
  rmdir /s /q "%%d" 2>nul
)

exit
