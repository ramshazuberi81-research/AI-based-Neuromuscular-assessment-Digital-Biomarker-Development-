# AI_Facial_Clinical

> **AI-driven clinical platform for objective, reproducible, and quantitative assessment of facial motor function**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-teal?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## Table of Contents

- [Overview](#overview)
- [Clinical Motivation](#clinical-motivation)
- [Target Conditions](#target-conditions)
- [System Architecture](#system-architecture)
- [Analytical Pipelines](#analytical-pipelines)
- [User Interfaces](#user-interfaces)
- [Core Technologies](#core-technologies)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)

---

## Overview

AI_Facial_Clinical is a hybrid patient-clinician platform that converts facial motion and speech patterns into measurable clinical indices. It provides:

- Real-time facial symmetry computation via 468-point 3D landmark extraction
- Quantitative motor scoring with side-specific asymmetry analysis
- Speech clarity assessment and motor-speech impairment indexing
- Session-to-session longitudinal progress tracking
- Automated PDF clinical report generation

> **Note:** This is a research prototype, not validated for clinical deployment.

---

## Clinical Motivation

Current facial motor assessment relies on subjective grading scales such as the **House–Brackmann system**, which suffer from:

| Challenge | Impact |
|-----------|--------|
| Subjective observer grading | High inter-rater variability |
| Ordinal scale granularity | Insensitive to subtle recovery |
| No longitudinal tracking | Missed trend detection |
| Absent AI support | No data-driven decision aid |

**AI_Facial_Clinical** addresses each of these by producing continuous, objective indices derived from computer vision and speech analysis — enabling data-driven clinical decisions with full audit trails.

---

## Target Conditions

| Condition | Status | Notes |
|-----------|--------|-------|
| Bell's Palsy | ✅ Primary target | Unilateral idiopathic facial nerve palsy |
| Post-stroke facial weakness | ✅ Supported | Central vs peripheral differentiation |
| Neuromuscular facial asymmetry | ✅ Supported | Myopathies, peripheral neuropathies |
| Parkinson's disease monitoring | 🔜 Roadmap | Tremor detection, micro-expression analysis |

---

## System Architecture

```
┌────────────────────────────────────────────────────────┐
│                     USER LAYER                         │
│                                                        │
│   ┌─────────────────┐       ┌─────────────────────┐   │
│   │    PATIENT       │       │     CLINICIAN        │   │
│   │  Self-assessment │       │  Neurologist dash.   │   │
│   └────────┬────────┘       └──────────┬──────────┘   │
└────────────┼────────────────────────────┼──────────────┘
             │                            │
             └──────────────┬─────────────┘
                            ▼
                    ┌───────────────┐
                    │    app.py     │  ← Entry point & router
                    └───────┬───────┘
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
┌─────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ facial_engine   │ │  speech_engine   │ │clinical_scoring  │
│     .py         │ │      .py         │ │      .py         │
│                 │ │                  │ │                  │
│ • Face detect   │ │ • Noise reduce   │ │ • Severity class │
│ • Landmark ext. │ │ • Feature ext.   │ │ • Asymmetry map  │
│ • Symmetry comp.│ │ • Clarity score  │ │ • HB equivalent  │
└────────┬────────┘ └────────┬─────────┘ └────────┬─────────┘
         └──────────────────┼──────────────────────┘
                            ▼
                   ┌─────────────────┐
                   │ Analytics Layer │
                   │ plots.py        │
                   │ progress_tracker│
                   └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼                           ▼
   ┌──────────────────┐       ┌──────────────────────┐
   │  SQLite Database │       │    PDF Reports        │
   │  Session storage │       │    ReportLab          │
   └──────────────────┘       └──────────────────────┘
```

---

## Analytical Pipelines

### Facial Analysis Pipeline

```
Camera Input
     │
     ▼  ── MediaPipe FaceDetector
Face Detection
     │
     ▼  ── 468 3D keypoints extracted per frame
Landmark Extraction
     │
     ▼  ── Per-region left/right ratio computation
Symmetry Computation
     │
     ▼  ── 0–100 continuous index, side-specific
Motor Score Generation
     │
     ▼
Clinical Grade Output  ──→  Severity class + asymmetry heatmap
```

### Speech Analysis Pipeline

```
Audio Capture  (microphone stream)
     │
     ▼  ── Bandpass filtering, noise floor removal
Noise Reduction
     │
     ▼  ── Articulation, prosody, formant features
Feature Extraction
     │
     ▼  ── 0–100 intelligibility index
Speech Clarity Score
     │
     ▼  ── Derived motor-speech impairment index
Dysarthria Index
     │
     ▼
Clinical Report  ──→  Auto-generated PDF summary
```

---

## User Interfaces

### Patient View

Designed for accessibility and self-monitoring:

- Emoji-based immediate feedback (no medical jargon)
- Weekly recovery progress graphs
- Improvement percentage tracking vs. baseline
- Speech clarity index in plain language

### Clinician (Neurologist) View

Designed for objective clinical assessment:

- Raw symmetry ratios per facial region (brow, eye, nasolabial, mouth)
- Affected side quantification with laterality scoring
- Severity classification (House–Brackmann equivalent)
- Historical session-to-session comparison
- Exportable PDF clinical reports

### Longitudinal Progress Tracking

```
Score
100 ┤
 75 ┤                                      ●  Facial symmetry
 50 ┤              ●          ●
 25 ┤    ●                         ○  Speech clarity index
  0 ┤────┬────────┬────────┬────────┬────────┬────
      W1       W2       W3       W4       W5
```

Session-by-session tracking enables:
- Detection of plateau or regression events
- Correlation between facial motor and speech recovery curves
- Evidence-based treatment adjustment decisions

---

## Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Runtime | Python 3.x | Core application |
| Vision | OpenCV ≥ 4.8 | Frame capture, preprocessing |
| Landmarks | MediaPipe ≥ 0.10 | 468-point 3D facial mesh |
| Numerics | NumPy, Pandas | Symmetry computation, data handling |
| Storage | SQLite | Session persistence |
| Reports | ReportLab | Auto-generated PDF output |
| Models | Pickle (.pkl) | Pretrained classification models |

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Webcam (for facial analysis)
- Microphone (for speech analysis)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/AI_Facial_Clinical.git
cd AI_Facial_Clinical

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the application
python app.py
```

### Key Dependencies (`requirements.txt`)

```
opencv-python>=4.8.0
mediapipe>=0.10.0
numpy>=1.24.0
pandas>=2.0.0
reportlab>=4.0.0
sqlalchemy>=2.0.0
```

---

## Project Structure

```
AI_Facial_Clinical/
│
├── app.py                      # Entry point & interface router
├── config.py                   # System configuration
├── requirements.txt            # Python dependencies
│
├── core/
│   ├── facial_engine.py        # Landmark extraction & symmetry computation
│   ├── speech_engine.py        # Audio capture & clarity scoring
│   ├── clinical_scoring.py     # Severity classification & grading
│   └── preprocessing.py        # Frame/audio normalization
│
├── analytics/
│   ├── plots.py                # Progress visualizations
│   └── progress_tracker.py     # Session comparison logic
│
├── reports/
│   └── pdf_report.py           # Clinical PDF generation (ReportLab)
│
├── database/
│   ├── db.py                   # SQLAlchemy session management
│   └── schema.sql              # Table definitions
│
├── models/
│   ├── face_model.pkl          # Pretrained facial classification model
│   └── speech_model.pkl        # Pretrained speech model
│
└── data/                       # Session data & exports
```

---

## Roadmap

| Priority | Feature | Description |
|----------|---------|-------------|
| 🟢 Soon | Parkinson's tremor detection | Temporal landmark delta analysis for resting tremor quantification |
| 🟢 Soon | Telemedicine integration | Remote monitoring with async session upload and clinician review queue |
| 🔵 Later | Cloud multi-clinic database | Federated session storage enabling cross-site longitudinal cohort analysis |
| 🔵 Later | Predictive recovery modeling | LSTM-based trajectory forecasting from early-session symmetry indices |
| 🟣 Future | Clinical validation | Prospective study design targeting FDA De Novo or CE Class IIa pathway |

---

## Vision

Transform facial motor assessment from:

> **Subjective observation** → **Objective, AI-driven, reproducible clinical measurement**

Enhancing patient outcomes, reducing inter-observer variability, and standardizing neurological assessment across clinical settings.

---

## Disclaimer

AI_Facial_Clinical is a **research prototype**. It has not undergone prospective clinical validation and is **not approved for diagnostic or therapeutic use**. All outputs should be interpreted by qualified clinicians in conjunction with standard clinical evaluation.

---

*Built with OpenCV · MediaPipe · Python*
