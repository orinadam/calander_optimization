@echo off

cd /D "%~dp0"
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit/b)

@echo on
call run_server.bat
call run_website.bat