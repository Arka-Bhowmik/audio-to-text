from __future__ import annotations

import base64
import html
import io
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
from docx import Document

try:
    from faster_whisper import WhisperModel
except Exception:  # pragma: no cover
    WhisperModel = None

try:
    from streamlit_mic_recorder import mic_recorder
except Exception:  # pragma: no cover
    mic_recorder = None

APP_TITLE = "Audio to Text"
DEFAULT_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "small.en")
DEFAULT_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
DEFAULT_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
SUPPORTED_EXTENSIONS = ["wav", "mp3", "m4a", "mp4", "webm", "ogg", "flac", "aac"]

BG_APP = "#F5F7FB"
BG_CARD = "#FFFFFF"
BG_NOTE = "#F8FAFD"
TEXT_MUTED = "#4B5563"
BORDER = "#D6DCE8"
TITLE = "#111827"
BUTTON_BG = "#E8ECEF"
BUTTON_BORDER = "#A7AFBC"

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
ICON_PATH = ASSET_DIR / "app_icon.png"
HELP_IMAGE_PATH = ASSET_DIR / "Help_picture.png"
HELP_PDF_PATH = ASSET_DIR / "help_audio_to_text.pdf"


@dataclass
class TranscriptResult:
    text: str
    language: str | None
    duration: float | None
    segments: list[dict[str, Any]]


class WhisperTranscriber:
    def __init__(self, model_size: str = DEFAULT_MODEL_SIZE) -> None:
        self.model_size = model_size
        self._model: Any | None = None

    def get_model(self) -> Any:
        if WhisperModel is None:
            raise RuntimeError(
                "faster-whisper is not installed. Install requirements_streamlit.txt before running the app."
            )
        if self._model is None:
            self._model = WhisperModel(
                self.model_size,
                device=DEFAULT_DEVICE,
                compute_type=DEFAULT_COMPUTE_TYPE,
            )
        return self._model

    def transcribe(self, audio_path: str) -> TranscriptResult:
        model = self.get_model()
        segments, info = model.transcribe(
            audio_path,
            language="en",
            vad_filter=True,
            beam_size=5,
        )

        collected_segments: list[dict[str, Any]] = []
        full_text_parts: list[str] = []
        for seg in segments:
            seg_text = (seg.text or "").strip()
            collected_segments.append(
                {
                    "start": round(seg.start, 2),
                    "end": round(seg.end, 2),
                    "text": seg_text,
                }
            )
            if seg_text:
                full_text_parts.append(seg_text)

        transcript = " ".join(full_text_parts).strip()
        return TranscriptResult(
            text=transcript,
            language=getattr(info, "language", None),
            duration=getattr(info, "duration", None),
            segments=collected_segments,
        )


@st.cache_resource(show_spinner=False)
def get_transcriber(model_size: str) -> WhisperTranscriber:
    return WhisperTranscriber(model_size=model_size)


def init_state() -> None:
    defaults = {
        "status": "Ready",
        "current_audio_bytes": None,
        "current_audio_name": "",
        "current_audio_source": "",
        "current_audio_format": "",
        "recorded_audio_bytes": None,
        "last_transcript": "",
        "last_segments": [],
        "last_language": None,
        "last_duration": None,
        "last_timestamp": "",
        "play_recording": False,
        "uploader_nonce": 0,
        "recorder_nonce": 0,
        "last_recording_id": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def to_base64(path: Path) -> str:
    return base64.b64encode(read_bytes(path)).decode("utf-8")


def clickable_help_html(image_path: Path, pdf_path: Path) -> str:
    img_b64 = to_base64(image_path)
    pdf_b64 = to_base64(pdf_path)
    return f'''
    <div class="help-wrap">
      <a href="data:application/pdf;base64,{pdf_b64}" download="help_audio_to_text.pdf" title="Download help PDF">
        <img src="data:image/png;base64,{img_b64}" alt="Help" class="help-image" />
      </a>
    </div>
    '''


def build_docx_bytes() -> bytes:
    document = Document()
    document.add_heading("Audio Transcript", level=1)
    meta = document.add_paragraph()
    meta.add_run("Source: ").bold = True
    meta.add_run(st.session_state.current_audio_source or "audio")
    meta.add_run("\nFilename: ").bold = True
    meta.add_run(st.session_state.current_audio_name or "N/A")
    meta.add_run("\nGenerated: ").bold = True
    meta.add_run(st.session_state.last_timestamp or "N/A")
    meta.add_run("\nLanguage: ").bold = True
    meta.add_run(st.session_state.last_language or "N/A")
    meta.add_run("\nDuration (s): ").bold = True
    duration_text = (
        str(st.session_state.last_duration)
        if st.session_state.last_duration is not None
        else "N/A"
    )
    meta.add_run(duration_text)

    document.add_heading("Transcript", level=2)
    document.add_paragraph(st.session_state.last_transcript)

    if st.session_state.last_segments:
        document.add_heading("Time-stamped Segments", level=2)
        for seg in st.session_state.last_segments:
            document.add_paragraph(
                f"[{seg.get('start', 0):.2f}s → {seg.get('end', 0):.2f}s] {seg.get('text', '')}"
            )

    buffer = io.BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def export_stem() -> str:
    name = st.session_state.current_audio_name.strip()
    if not name:
        return "audio"
    return Path(name).stem or "audio"


def set_current_audio(audio_bytes: bytes, name: str, source: str, audio_format: str) -> None:
    st.session_state.current_audio_bytes = audio_bytes
    st.session_state.current_audio_name = name
    st.session_state.current_audio_source = source
    st.session_state.current_audio_format = audio_format
    st.session_state.status = (
        "Recording captured. Click Transcribe to continue."
        if source == "recorded audio"
        else "Audio file selected. Click Transcribe to continue."
    )
    if source != "recorded audio":
        st.session_state.recorded_audio_bytes = None
        st.session_state.play_recording = False


def clear_all() -> None:
    st.session_state.current_audio_bytes = None
    st.session_state.current_audio_name = ""
    st.session_state.current_audio_source = ""
    st.session_state.current_audio_format = ""
    st.session_state.recorded_audio_bytes = None
    st.session_state.last_transcript = ""
    st.session_state.last_segments = []
    st.session_state.last_language = None
    st.session_state.last_duration = None
    st.session_state.last_timestamp = ""
    st.session_state.play_recording = False
    st.session_state.last_recording_id = None
    st.session_state.uploader_nonce += 1
    st.session_state.recorder_nonce += 1
    st.session_state.status = "Input and output cleared."
    st.rerun()


def save_current_audio_to_tempfile() -> str:
    audio_bytes = st.session_state.current_audio_bytes
    if not audio_bytes:
        raise RuntimeError("No audio is currently selected.")

    suffix = ".wav"
    name = st.session_state.current_audio_name or "audio.wav"
    ext = Path(name).suffix.lower()
    if ext in {f".{x}" for x in SUPPORTED_EXTENSIONS}:
        suffix = ext

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(audio_bytes)
        return tmp.name


def apply_transcript_result(result: TranscriptResult) -> None:
    st.session_state.last_transcript = result.text
    st.session_state.last_segments = result.segments
    st.session_state.last_language = result.language
    st.session_state.last_duration = result.duration
    st.session_state.last_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.status = "Transcription complete."


def transcribe_current_audio() -> None:
    if not st.session_state.current_audio_bytes:
        st.session_state.status = "Please open an audio file or record audio first."
        return

    temp_path = None
    try:
        temp_path = save_current_audio_to_tempfile()
        result = get_transcriber(DEFAULT_MODEL_SIZE).transcribe(temp_path)
        apply_transcript_result(result)
    finally:
        if temp_path and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
            except Exception:
                pass


def summary_text() -> str:
    word_count = len(st.session_state.last_transcript.split()) if st.session_state.last_transcript else 0
    source = st.session_state.current_audio_source or "N/A"
    last_run = st.session_state.last_timestamp or "N/A"
    return f"Words: {word_count} | Segments: {len(st.session_state.last_segments)} | Source: {source} | Last run: {last_run}"


def selected_audio_label() -> str:
    if st.session_state.current_audio_name:
        return f"Selected: {st.session_state.current_audio_name}"
    return "No audio selected"


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {BG_APP};
        }}
        header[data-testid="stHeader"] {{
            display: none;
        }}
        div[data-testid="stToolbar"] {{
            display: none;
        }}
        #MainMenu {{
            visibility: hidden;
        }}
        .stAppViewContainer {{
            padding-top: 0;
        }}
        .main .block-container {{
            max-width: 1320px;
            padding-top: 0.55rem;
            padding-bottom: 1rem;
        }}
        .app-header {{
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: flex-start;
            margin-bottom: 0.7rem;
        }}
        .brand-row {{
            display: flex;
            gap: 0.9rem;
            align-items: flex-start;
        }}
        .brand-icon {{
            width: 44px;
            height: 44px;
            object-fit: contain;
            margin-top: 4px;
        }}
        .brand-title {{
            font-size: 2.0rem;
            font-weight: 700;
            color: {TITLE};
            line-height: 1.1;
            margin: 0;
        }}
        .brand-subtitle {{
            color: {TEXT_MUTED};
            font-size: 0.98rem;
            margin-top: 0.35rem;
        }}
        .header-right {{
            display: flex;
            align-items: flex-start;
            gap: 0.9rem;
        }}
        .note-box {{
            background: {BG_NOTE};
            border: 1px solid {BORDER};
            padding: 0.65rem 0.9rem;
            border-radius: 0;
            font-size: 0.92rem;
            color: #1F2937;
            font-style: italic;
            text-align: center;
            min-width: 290px;
        }}
        .help-wrap {{
            text-align: center;
        }}
        .help-image {{
            width: 116px;
            height: auto;
            display: block;
        }}
        .card-title {{
            font-weight: 700;
            font-size: 1.03rem;
            color: {TITLE};
            margin-bottom: 0.65rem;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 0;
            padding: 0.35rem 0.35rem 0.2rem 0.35rem;
            margin-bottom: 0.75rem;
        }}
        .section-label {{
            font-weight: 700;
            margin-top: 0.8rem;
            margin-bottom: 0.5rem;
            color: {TITLE};
        }}
        .muted-text {{
            color: {TEXT_MUTED};
            font-size: 0.94rem;
        }}
        .summary-line {{
            color: {TEXT_MUTED};
            font-size: 0.96rem;
            margin-top: 0.25rem;
            margin-bottom: 0.25rem;
        }}
        .subheading {{
            color: {TEXT_MUTED};
            font-size: 0.98rem;
            margin-top: 0.6rem;
            margin-bottom: 0.35rem;
        }}
        .stButton > button, .stDownloadButton > button {{
            width: 100%;
            background: {BUTTON_BG};
            color: #111827;
            border: 1px solid {BUTTON_BORDER};
            border-radius: 0;
            min-height: 2.6rem;
            font-size: 0.98rem;
            box-shadow: none;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            border-color: #8A94A3;
            background: #EFF2F5;
            color: #111827;
        }}
        .stButton > button:disabled {{
            color: #8B93A1;
            background: #ECECEC;
        }}
        .transcript-box {{
            border: 1px solid {BORDER};
            background: #FFFFFF;
            min-height: 260px;
            max-height: 260px;
            overflow-y: auto;
            padding: 0.85rem;
            white-space: pre-wrap;
            color: {TITLE};
            font-size: 1rem;
        }}
        .status-box {{
            color: {TITLE};
            font-size: 0.98rem;
            margin-bottom: 0.5rem;
        }}
        .meta-box {{
            color: {TEXT_MUTED};
            font-size: 0.92rem;
        }}
        div[data-testid="stFileUploader"] section {{
            border: 1px solid {BUTTON_BORDER};
            border-radius: 0;
            background: #FAFBFC;
        }}
        div[data-testid="stFileUploader"] button {{
            border-radius: 0;
        }}
        div[data-testid="stAudioInput"] button {{
            width: 100%;
            border-radius: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    icon_b64 = to_base64(ICON_PATH)
    disclaimer = html.escape("Note: This code is created with the help of OpenAI\ncontact: arkabhowmik@yahoo.co.uk").replace(
        "\n", "<br>"
    )
    header_html = f'''
    <div class="app-header">
      <div class="brand-row">
        <img class="brand-icon" src="data:image/png;base64,{icon_b64}" alt="App icon">
        <div>
          <h1 class="brand-title">Audio to Text</h1>
          <div class="brand-subtitle">Desktop audio transcription using microphone recording or audio-file upload.</div>
        </div>
      </div>
      <div class="header-right">
        <div class="note-box">{disclaimer}</div>
        {clickable_help_html(HELP_IMAGE_PATH, HELP_PDF_PATH)}
      </div>
    </div>
    '''
    st.markdown(header_html, unsafe_allow_html=True)


def render_left_panel() -> None:
    with st.container(border=True):
        st.markdown('<div class="card-title">Input</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Open audio file",
            type=SUPPORTED_EXTENSIONS,
            key=f"uploader_{st.session_state.uploader_nonce}",
            label_visibility="visible",
        )
        if uploaded_file is not None:
            set_current_audio(
                audio_bytes=uploaded_file.getvalue(),
                name=uploaded_file.name,
                source="uploaded audio",
                audio_format=Path(uploaded_file.name).suffix.lower().lstrip(".") or "wav",
            )

        st.markdown(f'<div class="muted-text">{html.escape(selected_audio_label())}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Microphone</div>', unsafe_allow_html=True)

        recorded_from_component = False
        if mic_recorder is not None:
            mic_audio = mic_recorder(
                start_prompt="Start recording",
                stop_prompt="Stop recording",
                just_once=False,
                use_container_width=True,
                key=f"mic_{st.session_state.recorder_nonce}",
            )
            if mic_audio and isinstance(mic_audio, dict):
                recording_id = mic_audio.get("id")
                if recording_id != st.session_state.last_recording_id:
                    st.session_state.last_recording_id = recording_id
                    audio_bytes = mic_audio.get("bytes")
                    if audio_bytes:
                        st.session_state.recorded_audio_bytes = audio_bytes
                        st.session_state.play_recording = False
                        set_current_audio(
                            audio_bytes=audio_bytes,
                            name="recorded_audio.wav",
                            source="recorded audio",
                            audio_format="wav",
                        )
                        recorded_from_component = True
        else:
            audio_input = st.audio_input(
                "Start recording",
                key=f"audio_input_{st.session_state.recorder_nonce}",
            )
            if audio_input is not None:
                audio_bytes = audio_input.getvalue()
                st.session_state.recorded_audio_bytes = audio_bytes
                st.session_state.play_recording = False
                set_current_audio(
                    audio_bytes=audio_bytes,
                    name="recorded_audio.wav",
                    source="recorded audio",
                    audio_format="wav",
                )
                recorded_from_component = True

        play_clicked = st.button(
            "Play recording",
            disabled=not bool(st.session_state.recorded_audio_bytes),
            key="play_recording_button",
        )
        if play_clicked and st.session_state.recorded_audio_bytes:
            st.session_state.play_recording = True

        if st.session_state.play_recording and st.session_state.recorded_audio_bytes:
            st.audio(st.session_state.recorded_audio_bytes, format="audio/wav")

        if recorded_from_component:
            st.session_state.status = "Recording captured. Click Transcribe to continue."

    with st.container(border=True):
        st.markdown('<div class="card-title">Actions</div>', unsafe_allow_html=True)
        if st.button("Transcribe", key="transcribe_button"):
            try:
                with st.spinner("Loading model and transcribing audio..."):
                    transcribe_current_audio()
            except Exception as exc:
                st.session_state.status = f"Transcription failed: {exc}"
                st.error(st.session_state.status)
        if st.button("Clear output", key="clear_button"):
            clear_all()

    with st.container(border=True):
        st.markdown('<div class="card-title">Status</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-box">{html.escape(st.session_state.status)}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="meta-box">Model: {html.escape(DEFAULT_MODEL_SIZE)} | Device: {html.escape(DEFAULT_DEVICE)} | Compute: {html.escape(DEFAULT_COMPUTE_TYPE)}</div>',
            unsafe_allow_html=True,
        )


def render_right_panel() -> None:
    export_col1, export_col2, _ = st.columns([1.1, 1.1, 5.8])
    txt_bytes = st.session_state.last_transcript.encode("utf-8") if st.session_state.last_transcript else b""
    with export_col1:
        st.download_button(
            "Download TXT",
            data=txt_bytes,
            file_name=f"{export_stem()}_transcript.txt",
            mime="text/plain",
            disabled=not bool(st.session_state.last_transcript),
            key="download_txt",
        )
    with export_col2:
        st.download_button(
            "Download DOCX",
            data=build_docx_bytes() if st.session_state.last_transcript else b"",
            file_name=f"{export_stem()}_transcript.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            disabled=not bool(st.session_state.last_transcript),
            key="download_docx",
        )

    with st.container(border=True):
        st.markdown('<div class="card-title" style="margin-top:0.1rem;">Transcript</div>', unsafe_allow_html=True)
        transcript = html.escape(st.session_state.last_transcript)
        st.markdown(f'<div class="transcript-box">{transcript}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line">{html.escape(summary_text())}</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="subheading" style="margin-top:0.1rem;">Time-stamped Segments</div>', unsafe_allow_html=True)
        if st.session_state.last_segments:
            df = pd.DataFrame(st.session_state.last_segments)
            df = df.rename(columns={"start": "Start (s)", "end": "End (s)", "text": "Text"})
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=280,
            )
        else:
            empty_df = pd.DataFrame(columns=["Start (s)", "End (s)", "Text"])
            st.dataframe(empty_df, use_container_width=True, hide_index=True, height=280)


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=str(ICON_PATH) if ICON_PATH.exists() else None,
        layout="wide",
    )
    init_state()
    inject_css()
    render_header()
    left_col, right_col = st.columns([1.05, 4.2], gap="medium")
    with left_col:
        render_left_panel()
    with right_col:
        render_right_panel()


if __name__ == "__main__":
    main()
