# Audio-to-text
Tiny streamlit app or windows app to convert pre-recorded audio or live recording into text file

This repository contains the source scripts and a lightweight CPU-based Streamlit/Windows app for converting pre-recorded audio files (.wav, .mp3, .m4a, .mp4, .webm, .ogg, .flac, .aac) and microphone-recorded audio into text. A Windows desktop version of the app can be created using the options described below, while the Streamlit version can be run in any Python virtual environment, also described below.

Further information can be obtained by writing to Arka Bhowmik (arkabhowmik@yahoo.co.uk).

![desktop_app_version](https://github.com/user-attachments/assets/5db82e26-bb12-4649-9da1-ba124fe66cb4)

## ⊞  Window app (follow below to create .exe file)
Users can simply use the files (main\win_audio2text\) and use following steps to create an exe file:

#### Step I: Download App Files 
[MRI_triage_app](https://drive.google.com/file/d/1N9k4Le-vWJWAuTUiGJM-GX2C4uM8Q1aH/view?usp=sharing) and start docker engine in local machine by running docker desktop

#### Step II: Load the downloaded Docker Image 
Open command prompt(Win)
```
cd C:\Users\Arka\Downloads                  (window command)
cd /Users/Arka/Downloads/                   (other OS)
docker load -i mri_triage_app.tar.gz
```
*The image will appear in dashboard of Docker desktop after completion of loading.*

#### Step IV: RUN the downloaded Docker Image 
Now, in the command prompt(Win) or terminal(Mac/Linux)
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
