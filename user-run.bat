@echo off
rem Activate Anaconda environment
call C:\Users\vdocv\Anaconda3\Scripts\activate.bat ai_stuff

rem Navigate to the script location
cd C:\AI\ComfyUI\

rem Run the Python script with arguments
python main.py --auto-launch

rem Deactivate the Anaconda environment
call C:\Users\vdocv\Anaconda3\Scripts\deactivate.bat
