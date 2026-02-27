import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

# ------------------------------
# Radar Chart
# ------------------------------
def radar_chart(patient_id, mouth, eye, brow, fsi):
    categories = ['Mouth', 'Eye', 'Brow', 'FSI']
    values = [mouth, eye, brow, fsi]
    values += values[:1]  # close the loop

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4,4), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='r', linewidth=2)
    ax.fill(angles, values, color='r', alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticks([0,0.25,0.5,0.75,1])
    ax.set_ylim(0,1)

    os.makedirs("charts", exist_ok=True)
    plt.savefig(f"charts/{patient_id}_radar.png")
    plt.close()

# ------------------------------
# Weekly Chart
# ------------------------------
def weekly_chart(patient_id):
    csv_file = "data/sessions.csv"
    try:
        df = pd.read_csv(csv_file)
    except:
        df = pd.DataFrame()

    if df.empty or patient_id not in df['patient_id'].values:
        return

    df = df[df['patient_id']==patient_id]
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df.sort_values('timestamp')
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(df['timestamp'], df['fsi'], marker='o', label='FSI')
    ax.set_xlabel("Date")
    ax.set_ylabel("FSI")
    ax.set_title(f"Weekly FSI for {patient_id}")
    ax.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(f"charts/{patient_id}_weekly.png")
    plt.close()

# ------------------------------
# Daily Chart
# ------------------------------
def daily_chart(patient_id):
    csv_file = "data/sessions.csv"
    try:
        df = pd.read_csv(csv_file)
    except:
        df = pd.DataFrame()
    if df.empty or patient_id not in df['patient_id'].values:
        return
    df = df[df['patient_id']==patient_id]
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    today = pd.Timestamp.now().normalize()
    df_today = df[df['timestamp'].dt.normalize()==today]
    if df_today.empty:
        return
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(df_today['timestamp'], df_today['fsi'], marker='o', color='blue', label='FSI')
    ax.set_xlabel("Time")
    ax.set_ylabel("FSI")
    ax.set_title(f"Today's FSI for {patient_id}")
    ax.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(f"charts/{patient_id}_daily.png")
    plt.close()