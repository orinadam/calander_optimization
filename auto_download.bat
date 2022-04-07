@echo off

cd /D "%~dp0"
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit/b)

@echo on

Rem install choco
powershell -command "Set-ExecutionPolicy Bypass -Scope Process"
powershell -command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"

Rem install software
powershell -command "choco install python -y"
powershell -command "choco install nodejs -y"
powershell -command "choco install git -y"


Rem install python packages
pip install pandas
pip install flask
pip install flask_cors
pip install flask-session
pip install openpyxl
pip install flask-core

Rem clone from git
git clone https://github.com/yalikadman1/calander_optimization.git
cd calander_optimization


