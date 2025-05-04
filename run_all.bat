@echo off
REM Change this to venv or new_venv if needed
set VENV_DIR=.venv

REM Activate virtual environment
call %VENV_DIR%\Scripts\activate.bat

REM Start Redis server in a new window
start "Redis Server" cmd /k "cd /d Redis\Redis-7.4.3-Windows-x64-msys2 && redis-server.exe redis.conf"

REM Wait a few seconds for Redis to start
timeout /t 5

REM Start Django development server
python manage.py runserver

REM (Optional) To start Celery worker, uncomment the next line:
REM start "Celery Worker" cmd /k "call %VENV_DIR%\Scripts\activate.bat && celery -A expensetracker_enhanced worker --loglevel=info"