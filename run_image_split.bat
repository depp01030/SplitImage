@echo off

cd /d "D:\PyLearning\SplitImage"
call venv\Scripts\activate.bat
uvicorn main:app --host=127.0.0.1 --port=8888