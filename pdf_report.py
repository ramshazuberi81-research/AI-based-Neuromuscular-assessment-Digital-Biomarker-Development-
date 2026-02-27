import os
import pandas as pd
from fpdf import FPDF

def generate_pdf_report(patient_id):
    os.makedirs("reports", exist_ok=True)
    file_path = "data/sessions.csv"

    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)

    if df.empty:
        return None

    df = df[df["patient_id"] == patient_id]
    if df.empty:
        return None

    latest = df.iloc[-1]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Clinical Facial Assessment Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Patient ID: {patient_id}", ln=True)
    pdf.cell(0, 8, f"Timestamp: {latest['timestamp']}", ln=True)
    pdf.ln(5)

    # Facial metrics
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Facial Symmetry Metrics", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"FSI: {latest['fsi']:.2f}", ln=True)
    pdf.cell(0, 8, f"Mouth Asymmetry: {latest['mouth_asym']:.2f}", ln=True)
    pdf.cell(0, 8, f"Eye Asymmetry: {latest['eye_asym']:.2f}", ln=True)
    pdf.cell(0, 8, f"Brow Asymmetry: {latest['brow_asym']:.2f}", ln=True)
    pdf.ln(5)

    # Speech metrics
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Speech Analysis", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Pitch Variation: {latest['pitch_var']:.2f}", ln=True)
    pdf.cell(0, 8, f"Jitter: {latest['jitter']:.2f}", ln=True)
    pdf.cell(0, 8, f"Shimmer: {latest['shimmer']:.2f}", ln=True)
    pdf.cell(0, 8, f"Clarity Score: {latest['clarity_score']:.2f}", ln=True)
    pdf.ln(5)

    # ML grade
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "House-Brackmann Grade", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Predicted Grade: {latest['house_brackmann_grade']}", ln=True)
    pdf.ln(10)

    # Charts
    radar_path = f"charts/{patient_id}_radar.png"
    weekly_path = f"charts/{patient_id}_weekly.png"

    if os.path.exists(radar_path):
        pdf.image(radar_path, x=30, w=150)
        pdf.ln(5)

    if os.path.exists(weekly_path):
        pdf.image(weekly_path, x=30, w=150)

    report_path = f"reports/{patient_id}_report.pdf"
    pdf.output(report_path)
    return report_path