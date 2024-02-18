@echo off
set PDIR=%~dp0

cd %PDIR%
for /d /r %%d in (__pycache__) do (
  if exist "%%d" (
    rmdir /s /q "%%d"
  )
)