@echo off
setlocal

if exist venv (
    call venv\Scripts\activate
)

python -m pip install --upgrade pip
pip install -r requirements_desktop.txt

pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name AudioToText ^
  --icon app_icon.ico ^
  --add-data "app_icon.png;." ^
  --add-data "Help_picture.png;." ^
  --add-data "help_audio_to_text.pdf;." ^
  --collect-all faster_whisper ^
  --collect-all ctranslate2 ^
  --collect-all av ^
  --collect-all tokenizers ^
  audio_to_text_desktop.py

if %errorlevel% neq 0 (
    echo Build failed.
    exit /b %errorlevel%
)

echo.
echo Build complete.
echo EXE path: dist\AudioToText.exe
endlocal
