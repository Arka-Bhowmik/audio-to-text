# Audio-to-text
Tiny streamlit app or windows app to convert pre-recorded audio or live recording into text file

This repository contains the source scripts and a lightweight CPU-based Streamlit/Windows app for converting pre-recorded audio files (.wav, .mp3, .m4a, .mp4, .webm, .ogg, .flac, .aac) and microphone-recorded audio into text (output: .txt or .docx). A Windows desktop version of the app can be created using the options described below, while the Streamlit version can be run in any Python virtual environment, also described below.

Further information can be obtained by writing to Arka Bhowmik (arkabhowmik@yahoo.co.uk).

![desktop_app_version](https://github.com/user-attachments/assets/5db82e26-bb12-4649-9da1-ba124fe66cb4)

## ⊞ Windows app (follow the steps below to create the `.exe` file)

Users can use the files in `main\win_audio2text\` and follow these steps to create the EXE file.

#### Step I: Download and install Python
Open **Command Prompt** on Windows and run:

```cmd
winget install Python.Python.3.12
python --version
pip --version
```
Use python --version and pip --version to confirm that Python was installed correctly. Next, copy the downloaded files from *main\win_audio2text\* to:
```
C:\Users\YourName\win_audio2text
```
*Copy the files from /main/win_audio2text --> C:\Users\Arka\win_audio2text*
#### Step II: Build the .bat file inside win_audio2text to create the one-file EXE

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
#### Step III: Run the created one-file EXE
- Double-click `AudioToText.exe` in `C:\Users\YourName\win_audio2text\dist\`
- The app opens directly as a desktop window
- No browser or Streamlit server is required


```
docker run -v "/c/Users/Arka/Desktop/image_dataset":/data -p 5000:5000 mri_triage:latest    (window command)
docker run -v "/Users/Arka/Desktop/image_dataset":/data -p 5000:5000 mri_triage:latest      (other OS)
```
*This will provide an url (e.g., "http://0.0.0.0:5000") for the app that can be copied to the browser of local machine.* In the above command, use an appropriate path for -v "/path/" to mount the raw data or image path of the local machine with the docker container that can be accessed inside docker from /data.

#### Step V: Modify Image Path in CSV
The app runs inference for single image or batch of NIFTI images. Batch of images are accepted by the app in the form of a file with extension (.csv or .xlsx) having the absolute image paths ordered in row (*see* input folder for csv headers). The uploaded csv file should have same header to avoid error while the app attempt to save the probabilities.
```
Also modify all "File_path" column in CSV/XLSX during batch run
(e.g., C:/Users/Arka/Desktop/image_dataset/XYZ/abc.nii.gz   to   /data/XYZ/abc.nii.gz)
since docker already mounted /c/Users/Arka/Desktop/image_dataset/    as    /data   in step IV
```
Next, upload the .xlsx or .csv file and run the inference.

#### Step VI: COPY output files
The app saves output "probability.csv" and ROC plot in folder output. The app only generate "roc.png" if the ground truth positive or negative is greater than #15. The saved output files can be copied from docker container from Docker desktop dashboard terminal (*see* [output](https://github.com/Arka-Bhowmik/MRI_triage_app/tree/main/output)). 
```
cp /output/probability.csv /data/
cp /output/roc.png /data/       (only applicable for list of images)
```
This will save the output files in the mounted folder "/Users/Arka/Desktop/image_dataset".


##### Note: For restricted server (*see* [Steps](https://github.com/Arka-Bhowmik/MRI_triage_app/blob/main/tempDir/README.md)).
