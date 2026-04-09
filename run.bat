@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

@echo off

SET "PATH=C:\Miniconda3;C:\Miniconda3\Scripts;%PATH%"

:: Get local IP
FOR /F "tokens=2 delims=:" %%A IN ('ipconfig ^| findstr /i "IPv4"') DO (
    SET "LOCAL_IP=%%A"
    SET "LOCAL_IP=!LOCAL_IP:~1!"
    GOTO :breakLoop
)
:breakLoop

echo ======================================
echo Starting Fooocus API...
echo It will be accessible on your network at:
echo http://%LOCAL_IP%:8888
echo ======================================

:: Just runs the server; please run setup.bat if you have not already
conda run -n fooocus-api --live-stream python main.py --host 0.0.0.0
pause