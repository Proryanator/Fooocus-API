@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

@echo off

echo ===== Fooocus API Setup Script =====

:: Go to the directory, including separate/external drives
pushd "%~dp0"

:: Check for conda
IF NOT EXIST "C:\Miniconda3" (
    echo Conda not found. Launching Miniconda installer...

    :: Launch install_miniconda.bat in a new admin command window
    powershell -NoProfile -Command "Start-Process cmd.exe -ArgumentList '/k \"%CD%\install_miniconda.bat\"' -Verb RunAs"

    echo Miniconda installation started in new window. Please wait for it to complete...
    exit /B
)

echo Conda already installed. Setting PATH...

SET "PATH=C:\Miniconda3;C:\Miniconda3\Scripts;%PATH%"

:: Create environment if it doesn't exist
echo Creating conda environment...
conda create -y -n fooocus-api python=3.10

:: Download models using model_loader
echo Downloading models...
call conda run -n fooocus-api --live-stream python -c "from fooocusapi.utils.model_loader import download_models; download_models()"

:: Launch the run script
call run.bat