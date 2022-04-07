@echo off

cd /D "%~dp0"
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit/b)

@echo on
call npx -y kill-port 5000
cd ../server
call python app.py