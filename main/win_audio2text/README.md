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
