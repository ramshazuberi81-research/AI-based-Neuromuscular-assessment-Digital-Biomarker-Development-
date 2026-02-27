import streamlit as st
import cv2
import os
import time
import pandas as pd
import numpy as np
import joblib
import queue
import av
import soundfile as sf
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from core.facial_engine import extract_landmarks, calculate_facial_metrics, clinical_house_brackmann
from core.speech_engine import analyze_audio
from core.plots import radar_chart, weekly_chart
from core.pdf_report import generate_pdf_report

# -----------------------------------
# Setup
# -----------------------------------
st.set_page_config(layout="wide")
st.title("AI Facial & Speech Clinical Telemedicine Platform")

for folder in ["data", "charts", "reports"]:
    os.makedirs(folder, exist_ok=True)

mode = st.radio("Select Mode", ["Patient", "Doctor"])
patient_id = st.text_input("Patient ID", "Patient_001")

# -----------------------------------
# Load ML model (optional)
# -----------------------------------
clf = None
le = None
if os.path.exists("core/models/housebrackmann_model.pkl"):
    clf = joblib.load("core/models/housebrackmann_model.pkl")
    le = joblib.load("core/models/label_encoder.pkl")

# -----------------------------------
# Safe CSV
# -----------------------------------
csv_path = "data/sessions.csv"
columns = ['patient_id','timestamp','mouth_asym','eye_asym','brow_asym',
           'fsi','pitch_var','jitter','shimmer','clarity_score',
           'clinical_grade','ml_grade']

if os.path.exists(csv_path):
    try:
        df_sessions = pd.read_csv(csv_path)
    except:
        df_sessions = pd.DataFrame(columns=columns)
else:
    df_sessions = pd.DataFrame(columns=columns)

# -----------------------------------
# CAMERA SECTION
# -----------------------------------
st.subheader("Facial Assessment")

if "camera" not in st.session_state:
    st.session_state.camera = None

col1, col2 = st.columns(2)

with col1:
    if st.button("Start Camera"):
        st.session_state.camera = cv2.VideoCapture(0)

with col2:
    if st.button("Stop Camera") and st.session_state.camera:
        st.session_state.camera.release()
        st.session_state.camera = None

frame_placeholder = st.empty()

m=e=b=fsi=0
clinical_grade="N/A"

if st.session_state.camera:
    ret, frame = st.session_state.camera.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        landmarks = extract_landmarks(frame)

        if landmarks:
            fsi, m, e, b, _ = calculate_facial_metrics(landmarks)
            clinical_grade = clinical_house_brackmann(fsi)

            if mode == "Patient":
                emoji = "😄" if fsi>0.75 else "🙂" if fsi>0.5 else "😐" if fsi>0.3 else "😢"
                cv2.putText(frame_rgb,
                            f"Face Symmetry: {fsi*100:.1f}% {emoji}",
                            (30,50),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                st.metric("Symmetry Score", f"{fsi*100:.1f}%")
            else:
                cv2.putText(frame_rgb,
                            f"FSI: {fsi:.2f}",
                            (30,50),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                cv2.putText(frame_rgb,
                            f"M:{m:.2f} E:{e:.2f} B:{b:.2f}",
                            (30,90),
                            cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),2)

                st.subheader("Clinical House–Brackmann (Auto)")
                st.success(clinical_grade)

            radar_chart(patient_id, m, e, b, fsi)

        frame_placeholder.image(frame_rgb, channels="RGB")

# -----------------------------------
# MANUAL DOCTOR SCORING
# -----------------------------------
if mode == "Doctor":
    st.subheader("Manual Clinical Scoring")

    forehead_score = st.slider("Forehead (0–3)",0,3,3)
    eye_score = st.slider("Eye Closure (0–3)",0,3,3)
    mouth_score = st.slider("Smile (0–3)",0,3,3)

    manual_total = forehead_score + eye_score + mouth_score
    st.write("Manual Score:", manual_total)

# -----------------------------------
# SPEECH SECTION
# -----------------------------------
st.subheader("Speech Assessment")

audio_frames = queue.Queue()

def audio_callback(frame: av.AudioFrame):
    audio = frame.to_ndarray()
    audio_frames.put(audio)
    return frame

webrtc_ctx = webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDRECV,
    audio_frame_callback=audio_callback,
    media_stream_constraints={"audio": True, "video": False},
)

pitch_var=jitter=shimmer=clarity=0

if st.button("Analyze Speech"):
    audio_data=[]
    while not audio_frames.empty():
        audio_data.append(audio_frames.get())

    if len(audio_data)>0:
        audio_np=np.concatenate(audio_data,axis=1).T
        sf.write("temp_live.wav",audio_np,48000)

        mean_f0,pitch_var,jitter,shimmer,clarity=analyze_audio("temp_live.wav")

        if mode=="Doctor":
            st.metric("Pitch Var",f"{pitch_var:.3f}")
            st.metric("Jitter",f"{jitter:.3f}")
            st.metric("Shimmer",f"{shimmer:.3f}")
            st.metric("Clarity",f"{clarity:.1f}")
        else:
            st.metric("Speech Clarity",f"{clarity:.1f}%")

# -----------------------------------
# SAVE SESSION
# -----------------------------------
if st.button("Save Session"):

    ml_grade="N/A"
    if clf and mode=="Doctor":
        features=[[m,e,b,fsi,pitch_var,jitter,shimmer,clarity]]
        pred=clf.predict(features)
        ml_grade=le.inverse_transform(pred)[0]

    new_row={
        'patient_id':patient_id,
        'timestamp':time.time(),
        'mouth_asym':m,
        'eye_asym':e,
        'brow_asym':b,
        'fsi':fsi,
        'pitch_var':pitch_var,
        'jitter':jitter,
        'shimmer':shimmer,
        'clarity_score':clarity,
        'clinical_grade':clinical_grade,
        'ml_grade':ml_grade
    }

    df_sessions=pd.concat([df_sessions,pd.DataFrame([new_row])],ignore_index=True)
    df_sessions.to_csv(csv_path,index=False)

    weekly_chart(patient_id)

    st.success("Session Saved")

    if os.path.exists(f"charts/{patient_id}_weekly.png"):
        st.image(f"charts/{patient_id}_weekly.png")

# -----------------------------------
# PDF REPORT
# -----------------------------------
if st.button("Generate Clinical PDF"):
    path=generate_pdf_report(patient_id)
    if path:
        st.success("PDF Generated")
        with open(path,"rb") as f:
            st.download_button("Download PDF",f,file_name=os.path.basename(path))