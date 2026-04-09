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
