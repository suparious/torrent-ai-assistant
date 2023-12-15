@echo off
SET task_name=MyPythonScriptTask

REM Remove the task
schtasks /Delete /TN %task_name% /F
IF %ERRORLEVEL% EQU 0 (
    ECHO Task has been removed.
) ELSE (
    ECHO Task could not be found or removed.
)

PAUSE
