# Audio-to-text
Tiny streamlit app or windows app to convert pre-recorded audio or live recording into text file

This repository contains the source scripts and a lightweight CPU-based Streamlit/Windows app for converting pre-recorded audio files (.wav, .mp3, .m4a, .mp4, .webm, .ogg, .flac, .aac) and microphone-recorded audio into text (output: .txt or .docx). A Windows desktop version of the app can be created using the options described below, while the Streamlit version can be run in any Python virtual environment, also described below.

Further information can be obtained by writing to Arka Bhowmik (arkabhowmik@yahoo.co.uk).

## ⊞ Windows app (follow the steps below to create the `.exe` file)
![desktop_app](https://github.com/user-attachments/assets/c6722515-47a0-460f-a253-7b8bc9f323c3)
Users can use the files in `main\win_audio2text\` and follow these steps to create the EXE file.

#### Step I: Download and install Python
Open **Command Prompt** on Windows and run:

```cmd
winget install Python.Python.3.12
python --version
pip --version
```
Use python --version and pip --version to confirm that Python was installed correctly. 

#### Step II: Copy the downloaded files from *main\win_audio2text\* to:
```
C:\Users\YourName\win_audio2text
```
#### Step III: Build the .bat file inside win_audio2text to create the one-file EXE
In Command Prompt, run:
```cmd
cd C:\Users\YourName\win_audio2text\
python -m venv venv
venv\Scripts\activate
build_exe.bat
```
Executing the above commands creates the one-file EXE at:
```
C:\Users\YourName\win_audio2text\dist\AudioToText.exe
```
#### Step IV: Run the created one-file EXE
- Double-click `AudioToText.exe` in `C:\Users\YourName\win_audio2text\dist\`
- The app opens directly as a desktop window
- No browser or Streamlit server is required


## ✨ Streamlit app (follow the steps below to run the app)
<img width="1464" height="1246" alt="streamlit_app" src="https://github.com/user-attachments/assets/faff7744-138f-4381-9d1c-a6449200b055" />
Users can use the files in `main\streamlit_audio2text\` and follow these steps to run the app.

#### Step I: Download and install Python

Open **Command Prompt** on Windows and run:
```cmd
winget install Python.Python.3.12
python --version
pip --version
```
Use python --version and pip --version to confirm that Python was installed correctly.

#### Step II: Copy the downloaded files from *main\streamlit_audio2text\* to:
```
C:\Users\YourName\streamlit_audio2text
```
#### Step III: Run the `requirements_streamlit.txt` file inside streamlit_audio2text inside environment
In Command Prompt, run:
```cmd
cd C:\Users\YourName\streamlit_audio2text\
python -m venv venv
venv\Scripts\activate
pip install -r requirements_streamlit.txt
```
#### Step IV: Run the `app.py` file
In Command Prompt, run:
```cmd
streamlit run app.py
```
*This will provide an url (e.g., "http://localhost:8501") for the app that can be copied to the browser of local machine.* 

## Notes:
- The Whisper model itself is still downloaded on first use and then cached locally by `faster-whisper`.
- Browser microphone recording requires microphone permission in the browser while using streamlit.
- If `streamlit-mic-recorder` is unavailable, the app falls back to Streamlit's native `audio_input` widget.
- Available language: `English`
- Default model: `small.en`
- Default device: `cpu`
- Default compute type: `int8`
- The Help image <img width="30" height="50" alt="Help_picture" src="https://github.com/user-attachments/assets/498e33cd-80a1-4f57-a6f1-7e82978b67b6" /> saves a local copy of the bundled help PDF.
