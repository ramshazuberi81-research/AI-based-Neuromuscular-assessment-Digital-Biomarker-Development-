import librosa
import numpy as np
import soundfile as sf

def analyze_audio(file):
    y, sr = librosa.load(file, sr=16000)
    f0, _, _ = librosa.pyin(y, fmin=75, fmax=300)
    f0_clean = f0[~np.isnan(f0)]

    mean_f0 = np.mean(f0_clean)
    pitch_var = np.std(f0_clean)
    jitter = np.mean(np.abs(np.diff(f0_clean))) / mean_f0
    shimmer = np.std(y) / np.mean(np.abs(y))
    clarity_score = 100 - (pitch_var*0.5 + jitter*50)

    return mean_f0, pitch_var, jitter, shimmer, clarity_score