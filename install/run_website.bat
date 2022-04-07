@echo off

cd /D "%~dp0"
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit/b)

@echo on
call npx -y kill-port 4000
cd ../frontend
call npm ci
call npm install
call npm audit
call npm run build
call npm install -g serve
call npm fund
call serve -s build -l 4000


