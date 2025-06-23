@echo off
run_image_split.bat
# cd /d "D:\PyLearning\SplitImage"
cd /d "/Applications/Depp/PyProject/SplitImage/"
call venv\Scripts\activate.bat
uvicorn main:app --host=127.0.0.1 --port=8888