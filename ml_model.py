# core/ml_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Paths
data_path = "data/sessions.csv"
model_dir = "core/models"
os.makedirs(model_dir, exist_ok=True)

# Load CSV
df = pd.read_csv(data_path)
df = df.dropna()  # remove incomplete rows

# Features & labels
X = df[['mouth_asym','eye_asym','brow_asym','fsi','pitch_var','jitter','shimmer','clarity_score']]
y = df['house_brackmann_grade']

# Encode labels
le = LabelEncoder()
y_enc = le.fit_transform(y)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y_enc)

# Save model
joblib.dump(clf, os.path.join(model_dir,"housebrackmann_model.pkl"))
joblib.dump(le, os.path.join(model_dir,"label_encoder.pkl"))
print("ML model trained and saved successfully.")