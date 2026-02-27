import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

# -----------------------------
# Extract Facial Landmarks
# -----------------------------
def extract_landmarks(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if not results.multi_face_landmarks:
        return None

    landmarks = results.multi_face_landmarks[0].landmark
    return landmarks


# -----------------------------
# Calculate Facial Metrics
# -----------------------------
def calculate_distance(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def calculate_facial_metrics(landmarks):

    # Mouth corners
    left_mouth = landmarks[61]
    right_mouth = landmarks[291]

    mouth_asym = abs(left_mouth.y - right_mouth.y)

    # Eye (upper-lower)
    left_eye_top = landmarks[159]
    left_eye_bottom = landmarks[145]
    right_eye_top = landmarks[386]
    right_eye_bottom = landmarks[374]

    left_eye_open = calculate_distance(left_eye_top, left_eye_bottom)
    right_eye_open = calculate_distance(right_eye_top, right_eye_bottom)

    eye_asym = abs(left_eye_open - right_eye_open)

    # Brow
    left_brow = landmarks[70]
    right_brow = landmarks[300]

    brow_asym = abs(left_brow.y - right_brow.y)

    # Normalize values (simple scaling)
    mouth_score = 1 - min(mouth_asym * 10, 1)
    eye_score = 1 - min(eye_asym * 10, 1)
    brow_score = 1 - min(brow_asym * 10, 1)

    # Facial Symmetry Index
    fsi = np.mean([mouth_score, eye_score, brow_score])

    return fsi, mouth_score, eye_score, brow_score, landmarks


# -----------------------------
# Clinical House–Brackmann Rule
# -----------------------------
def clinical_house_brackmann(fsi):

    if fsi > 0.85:
        return "Grade I (Normal)"
    elif fsi > 0.70:
        return "Grade II (Mild)"
    elif fsi > 0.55:
        return "Grade III (Moderate)"
    elif fsi > 0.40:
        return "Grade IV (Moderately Severe)"
    elif fsi > 0.25:
        return "Grade V (Severe)"
    else:
        return "Grade VI (Total Paralysis)"