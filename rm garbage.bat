@echo off
set "PDIR=%~dp0"

cd /d "%PDIR%"
for /d /r %%d in (__pycache__ Data) do (
  rmdir /s /q "%%d" 2>nul
)
