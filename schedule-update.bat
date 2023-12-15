@echo off
SET script_path=C:\path\to\your\main.py
SET task_name=MyPythonScriptTask

REM Check if the task already exists
schtasks /Query | findstr /I %task_name% >nul
IF %ERRORLEVEL% EQU 0 (
    ECHO Task exists. Updating...
    schtasks /Delete /TN %task_name% /F
) ELSE (
    ECHO Task does not exist. Creating...
)

REM Create or Update the task
schtasks /Create /SC HOURLY /TN %task_name% /TR "python %script_path%" /F

ECHO Task has been created or updated.
PAUSE
