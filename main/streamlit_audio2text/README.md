## ✨ Streamlit Audio-to-Text App

<img width="1464" height="1246" alt="streamlit_app" src="https://github.com/user-attachments/assets/faff7744-138f-4381-9d1c-a6449200b055" />

Users can use the files in `main\streamlit_audio2text\` and follow the steps below to run the app.

This Streamlit app lets a user either **upload an audio file** or **record audio directly** and then transcribe it to text. The current recording path can capture **microphone input and computer/system audio together**, mix them into one enhanced WAV source, play the audio in the UI, transcribe it with `faster-whisper`, display timestamped segments, and export the transcript as **TXT** or **DOCX**.

---

## Main features

- Upload audio files for transcription.
- Record directly inside Streamlit.
- Preferred desktop recording path captures microphone audio and computer/system audio together.
- Recording continues until the user clicks **Stop Recording**; there is no fixed duration limit.
- Automatic audio cleanup is applied after recording:
  - DC-offset removal,
  - high-pass filtering,
  - spectral noise reduction with `scipy` when available,
  - fallback NumPy-based cleanup when advanced suppression is unavailable,
  - RMS normalization,
  - peak limiting.
- Microphone and system-audio tracks are enhanced and balanced before mixing.
- The enhanced mixed WAV becomes the current audio source for playback and transcription.
- Optional enhancement of uploaded WAV files using `ENHANCE_UPLOADED_AUDIO=1`.
- Transcription with `faster-whisper` by default.
- Environment-variable control for model, device, compute type, decoding, VAD, chunking, and optional diarization.
- Optional source-aware transcription for recorded audio: mixed audio, microphone-only audio, and system-audio-only audio can be transcribed and merged.
- Optional chunked transcription for longer recordings.
- Optional WhisperX ASR backend if installed.
- Optional pyannote speaker diarization if installed and configured.
- Speaker/source/backend labels are shown in timestamped segments when available.
- Transcript export as TXT and DOCX.
- Header includes app icon and help image/PDF link.

---

## Project files

```text
streamlit_audio2text/
├── app.py                       # Main Streamlit app
├── requirements_streamlit.txt   # Required Python packages for the basic app
├── README.md                    # This documentation
├── .streamlit/
│   └── config.toml              # Streamlit theme/server configuration
└── assets/
    ├── app_icon.png
    ├── Help_picture.png
    └── help_audio_to_text.pdf
```

---

## Required Python packages

The current `requirements_streamlit.txt` includes:

```text
streamlit
faster-whisper
python-docx
pandas
streamlit-mic-recorder
numpy
soundcard
scipy
```

`scipy` is used for the advanced spectral noise-suppression path. If `scipy` is unavailable, the app falls back to the built-in NumPy cleanup path.

For best compatibility with uploaded compressed audio formats and optional WhisperX workflows, install **FFmpeg** on the system.

---

## Step I: Download and install Python

### Windows

Open **Command Prompt** or **PowerShell** and run:

```cmd
winget install Python.Python.3.12
python --version
pip --version
```

Use `python --version` and `pip --version` to confirm that Python was installed correctly.

### Linux / Ubuntu

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip ffmpeg libsndfile1
python3 --version
pip3 --version
```

---

## Step II: Copy the app files

Copy the downloaded files from:

```text
main\streamlit_audio2text\
```

to a local folder such as:

```text
C:\Users\YourName\streamlit_audio2text
```

On Linux, an example path is:

```bash
/home/yourname/streamlit_audio2text
```

---

## Step III: Create an environment and install requirements

### Windows Command Prompt

```cmd
cd C:\Users\YourName\streamlit_audio2text\
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements_streamlit.txt
```

### Windows PowerShell

```powershell
cd C:\Users\YourName\streamlit_audio2text\
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements_streamlit.txt
```

### Linux / macOS terminal

```bash
cd /home/yourname/streamlit_audio2text
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements_streamlit.txt
```

---

## Step IV: Run the app

```bash
streamlit run app.py
```

This will provide a local URL such as:

```text
http://localhost:8501
```

Open that URL in a web browser.

To bind to a specific local address and port:

```bash
streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

---

## Basic usage

### Upload audio

1. Open the app.
2. Upload an audio file from the upload area.
3. Click **Play audio** to preview it.
4. Click **Transcribe**.
5. Review the transcript and timestamped segments.
6. Download the transcript as TXT or DOCX if needed.

Supported upload extensions are defined in `app.py`:

```text
wav, mp3, m4a, mp4, webm, ogg, flac, aac
```

### Record audio

1. Click **Start Recording**.
2. Speak into the microphone and/or play system audio.
3. Click **Stop Recording** when finished.
4. The app enhances the captured audio automatically.
5. Click **Play audio** to preview the enhanced recording.
6. Click **Transcribe**.
7. Review the transcript and timestamped segments.

The preferred recording path uses the `soundcard` package to capture microphone and computer/system audio. If desktop system-audio capture is unavailable, the app falls back to browser microphone recording when possible.

---

## Computer/system audio capture notes

System-audio capture depends on the operating system and available loopback/monitor devices.

### Windows

The app attempts to use the default speaker loopback through `soundcard`. If system audio is not captured:

- confirm that the correct output device is selected as the Windows default speaker,
- check whether WASAPI loopback is available,
- check whether “Stereo Mix” or a similar loopback source is enabled,
- restart the app after changing audio devices.

### Linux

The app looks for PulseAudio/PipeWire monitor sources. If system audio is not captured:

- confirm that PulseAudio or PipeWire is running,
- check monitor sources in your sound settings,
- ensure the correct output device is active before starting the app,
- restart the app after changing audio devices.

If only microphone capture is available, the app should show a warning instead of silently failing.

---

## Audio enhancement behavior

For recorded audio, enhancement is automatic after **Stop Recording**. There is no separate noise-reduction button.

The app currently performs layered cleanup:

1. Converts audio safely to `float32`.
2. Removes DC offset.
3. Applies high-pass filtering to reduce low-frequency rumble.
4. Estimates the noise floor from lower-energy regions.
5. Applies spectral noise reduction using `scipy.signal.stft` when available.
6. Falls back to NumPy-based soft gating when advanced suppression is unavailable.
7. Normalizes RMS levels.
8. Applies peak limiting to avoid clipping.

For recorded audio, microphone and system-audio tracks are enhanced separately before mixing, then the final mixed audio is enhanced again.

For uploaded audio, enhancement is disabled by default. To enhance uploaded WAV files before transcription:

```bash
export ENHANCE_UPLOADED_AUDIO=1
```

On Windows Command Prompt:

```cmd
set ENHANCE_UPLOADED_AUDIO=1
```

Only uploaded WAV enhancement is supported directly inside the app.

---

## Transcription defaults

The default transcription backend is `faster-whisper`.

Default settings are CPU-friendly:

```text
WHISPER_MODEL / WHISPER_MODEL_SIZE = small.en
WHISPER_DEVICE = cpu
WHISPER_COMPUTE_TYPE = int8
WHISPER_LANGUAGE = en
```

The app displays the active model, device, compute type, backend, enhancement status, chunking status, and diarization status in the left-side status panel.

---

## Environment variables

You can configure the app by setting environment variables before running `streamlit run app.py`.

### Core Whisper / faster-whisper settings

| Variable | Default | Purpose |
|---|---:|---|
| `WHISPER_MODEL` | `small.en` | Primary model name. |
| `WHISPER_MODEL_SIZE` | `small.en` | Alternate model variable if `WHISPER_MODEL` is not set. |
| `WHISPER_DEVICE` | `cpu` | Use `cpu` or `cuda`. |
| `WHISPER_COMPUTE_TYPE` | `int8` | CPU default. For GPU, commonly `float16`. |
| `WHISPER_LANGUAGE` | `en` | Language hint. Use empty/unset for auto-detection. |
| `WHISPER_BEAM_SIZE` | `5` | Beam-search size. |
| `WHISPER_BEST_OF` | `5` | Candidate count for decoding. |
| `WHISPER_VAD_FILTER` | `True` | Enables VAD filtering. |
| `WHISPER_NO_SPEECH_THRESHOLD` | `0.25` | Lower value is less aggressive about skipping quiet speech. |
| `WHISPER_LOG_PROB_THRESHOLD` | `-1.2` | Controls low-confidence filtering. |
| `WHISPER_CONDITION_ON_PREVIOUS_TEXT` | `False` | Helps reduce repetition/drift in some recordings. |
| `WHISPER_TEMPERATURE` | `0.0` | Decoding temperature. |

### Multi-speaker and long-audio behavior

| Variable | Default | Purpose |
|---|---:|---|
| `ASR_QUALITY_PRESET` | `balanced` | UI/status guidance: `cpu_fast`, `balanced`, `high_accuracy`, or `multispeaker`. |
| `TRANSCRIBE_SOURCES_SEPARATELY` | `True` | For recorded audio, transcribe mixed, microphone-only, and system-only tracks when available, then merge results. |
| `ENABLE_CHUNKED_TRANSCRIPTION` | `True` | Enables chunked transcription for longer WAV recordings. |
| `CHUNK_LENGTH_SECONDS` | `30.0` | Chunk size for long recordings. |
| `CHUNK_OVERLAP_SECONDS` | `3.0` | Overlap used to reduce missed words at chunk boundaries. |

### Backend selection

| Variable | Default | Purpose |
|---|---:|---|
| `TRANSCRIPTION_BACKEND` | `faster_whisper` | Supported values: `faster_whisper`, `whisperx`, `auto`, `nemo`. |
| `WHISPERX_MODEL` | `large-v3` | WhisperX model name if WhisperX is installed and selected. |
| `WHISPERX_DEVICE` | same as `WHISPER_DEVICE` | WhisperX device. |
| `WHISPERX_COMPUTE_TYPE` | same as `WHISPER_COMPUTE_TYPE` | WhisperX compute type. |
| `WHISPERX_BATCH_SIZE` | `8` | WhisperX batch size. |

Notes:

- `faster_whisper` is the default and recommended baseline.
- `whisperx` is optional and used only if installed.
- `auto` tries WhisperX if available, otherwise falls back to faster-whisper.
- `nemo` is currently a prepared placeholder; if selected, the app reports that NeMo is not implemented and falls back to faster-whisper.

### Optional diarization settings

| Variable | Default | Purpose |
|---|---:|---|
| `ENABLE_DIARIZATION` | `False` | Enables optional speaker diarization. |
| `DIARIZATION_BACKEND` | `pyannote` | Supported diarization backend in the current app. |
| `HF_TOKEN` | empty | Hugging Face token needed for pyannote models that require access. |
| `PYANNOTE_MODEL` | `pyannote/speaker-diarization-3.1` | pyannote model ID. |
| `MIN_SPEAKERS` | unset | Optional minimum number of speakers. |
| `MAX_SPEAKERS` | unset | Optional maximum number of speakers. |
| `DIARIZATION_TRANSCRIBE_TURNS` | same as `ENABLE_DIARIZATION` | If enabled, transcribes diarized speaker turns separately. |

Diarization is disabled by default because it may require extra dependencies, Hugging Face authentication, and model-access approval.

---

## Example configurations

### Default CPU mode

```bash
streamlit run app.py
```

### Higher-accuracy CPU mode, slower

```bash
export WHISPER_MODEL=medium.en
export WHISPER_DEVICE=cpu
export WHISPER_COMPUTE_TYPE=int8
streamlit run app.py
```

Windows Command Prompt equivalent:

```cmd
set WHISPER_MODEL=medium.en
set WHISPER_DEVICE=cpu
set WHISPER_COMPUTE_TYPE=int8
streamlit run app.py
```

### GPU mode

```bash
export WHISPER_MODEL=large-v3
export WHISPER_DEVICE=cuda
export WHISPER_COMPUTE_TYPE=float16
streamlit run app.py
```

Use GPU mode only after installing a PyTorch/CUDA stack compatible with your machine.

### Multi-speaker focused mode with faster-whisper

```bash
export ASR_QUALITY_PRESET=multispeaker
export TRANSCRIPTION_BACKEND=faster_whisper
export TRANSCRIBE_SOURCES_SEPARATELY=1
export ENABLE_CHUNKED_TRANSCRIPTION=1
export WHISPER_BEAM_SIZE=5
export WHISPER_BEST_OF=5
export WHISPER_NO_SPEECH_THRESHOLD=0.25
export WHISPER_LOG_PROB_THRESHOLD=-1.2
export WHISPER_CONDITION_ON_PREVIOUS_TEXT=False
streamlit run app.py
```

### Optional WhisperX backend

Install optional packages first:

```bash
pip install whisperx
```

Then run:

```bash
export TRANSCRIPTION_BACKEND=whisperx
export WHISPERX_MODEL=large-v3
export WHISPERX_DEVICE=cpu
export WHISPERX_COMPUTE_TYPE=int8
streamlit run app.py
```

If WhisperX is not installed or fails, the app falls back to faster-whisper and reports the fallback in the status panel.

### Optional pyannote diarization

Install optional package:

```bash
pip install pyannote.audio
```

Set the required environment variables:

```bash
export ENABLE_DIARIZATION=1
export DIARIZATION_BACKEND=pyannote
export HF_TOKEN="your_huggingface_token_here"
export PYANNOTE_MODEL="pyannote/speaker-diarization-3.1"
streamlit run app.py
```

You may also set:

```bash
export MIN_SPEAKERS=2
export MAX_SPEAKERS=4
```

If pyannote is not installed, the token is missing, or diarization fails, the app continues normal transcription and reports the issue in the UI.

---

## Optional advanced packages

These are not required for the basic app:

```bash
pip install whisperx
pip install pyannote.audio
```

For NeMo experiments, use a separate environment. NeMo is currently not fully implemented in `app.py`; the app contains a safe fallback placeholder.

```bash
conda create -n nemo_asr python=3.10 -y
conda activate nemo_asr
pip install "nemo_toolkit[asr]"
```

Do not add NeMo to the basic Streamlit environment unless you specifically need to develop that backend.

---

## Multi-speaker transcription notes

The app includes several strategies to reduce missed speech in multi-speaker recordings:

- less aggressive no-speech filtering,
- VAD padding,
- beam decoding,
- source-aware transcription of mixed/microphone/system tracks when recorded sources are available,
- chunked transcription for longer recordings,
- optional pyannote diarization and speaker-turn transcription.

However, no open-source ASR system can perfectly recover speech if speakers strongly overlap, if one speaker is much louder than another, or if a speaker is masked by system audio. For best results:

- keep the microphone close to the local speaker,
- keep system volume moderate,
- avoid speaker overlap when possible,
- use headphones to reduce echo/bleed,
- try a larger Whisper model or GPU when higher accuracy is required,
- enable diarization when speaker labels are important.

---

## Transcript output

After transcription, the right panel shows:

- transcript text,
- word and segment summary,
- timestamped segment table.

When available, timestamped segments include:

- start time,
- end time,
- speaker label,
- source label,
- backend label,
- text.

TXT and DOCX exports include the formatted transcript and timestamped segments.

---

## Troubleshooting

### The app does not start

Reinstall the requirements inside the active environment:

```bash
pip install -r requirements_streamlit.txt
```

Then verify the app compiles:

```bash
python -m py_compile app.py
```

### `faster-whisper` is not installed

```bash
pip install faster-whisper
```

or reinstall all requirements:

```bash
pip install -r requirements_streamlit.txt
```

### Computer/system audio is not captured

- Confirm `soundcard` is installed.
- Confirm your default output device is active.
- On Windows, check WASAPI loopback or Stereo Mix.
- On Linux, check PulseAudio/PipeWire monitor sources.
- Restart Streamlit after changing sound devices.

### Recording has noise

Noise suppression is automatic for recorded audio. If the audio is still noisy:

- reduce microphone gain,
- use headphones,
- reduce background fans/room noise,
- move closer to the microphone,
- avoid playing system audio too loudly through speakers.

### Only one speaker is transcribed

Try the multi-speaker configuration:

```bash
export ASR_QUALITY_PRESET=multispeaker
export TRANSCRIBE_SOURCES_SEPARATELY=1
export ENABLE_CHUNKED_TRANSCRIPTION=1
export WHISPER_MODEL=medium.en
streamlit run app.py
```

For speaker labels, install and enable pyannote diarization:

```bash
pip install pyannote.audio
export ENABLE_DIARIZATION=1
export HF_TOKEN="your_huggingface_token_here"
streamlit run app.py
```

### Large models are slow on CPU

Use a smaller model such as `small.en`, or use a GPU with:

```bash
export WHISPER_DEVICE=cuda
export WHISPER_COMPUTE_TYPE=float16
```

---

## Developer verification

From the project folder:

```bash
python -m py_compile app.py
streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Recommended manual checks:

1. Upload an audio file and transcribe it.
2. Record microphone-only speech.
3. Record system audio plus microphone speech.
4. Play the enhanced recording.
5. Transcribe the recording.
6. Confirm timestamped segments appear.
7. Download TXT and DOCX transcript exports.
8. Test Clear output.
9. If optional packages are installed, test `TRANSCRIPTION_BACKEND=whisperx` and `ENABLE_DIARIZATION=1`.

---

## Important notes

- The app is primarily a transcription tool, not a manual audio-saving application.
- Recorded audio is used as the current audio source for playback and transcription.
- Optional advanced dependencies should be installed only when needed.
- Basic transcription should continue to work even when optional WhisperX, pyannote, or NeMo dependencies are not installed.
