# AI Plant Doctor
🌱 **Smart Plant Identification, Disease Detection & Farming Early Warning System**

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.13-blue.svg)](https://www.python.org/)
[![UI](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![Weather](https://img.shields.io/badge/Weather-Open--Meteo-green.svg)](https://open-meteo.com/)
[![Tests](https://img.shields.io/badge/pytest-17%20passed-brightgreen.svg)](https://pytest.org/)

---

## 1. Project Overview

**AI Plant Doctor** is an expanded, major-project agricultural decision-support system. It combines deep learning transfer learning (MobileNetV2), authentic 5-day weather forecasting from Open-Meteo, agricultural extension rules, a comprehensive plant and disease database, visual symptom diagnostics, and on-device scan history with downloadable reports.

### Primary Objectives:
- **Separation of Plant Identification and Disease Classification**: Clear distinction between identifying a plant species and diagnosing a crop illness.
- **Decision Support, Not Guesswork**: Adheres strictly to a **60% confidence threshold**. When uncertain, shows:
  `"Not sure, please consult your agriculture officer or KVK"` / `"உறுதியாகக் கூற இயலவில்லை, தயவுசெய்து உங்கள் வேளாண்மை அலுவலர் அல்லது வேளாண் அறிவியல் மையத்தை (KVK) அணுகவும்"`.
- **Honest AI & Transparent Registries**: Supported classes are mapped directly in `data/species_registry.json`. No fabricated weights or simulated inferences.
- **Genuine Open-Meteo Live Weather**: Real-time geocoding and 5-day forecasts with automated alerts for fungal disease risk, pesticide spray wash-off, and heat stress.
- **Bilingual Interface**: Full English and தமிழ் (Tamil) support loaded from `data/i18n.json`.
- **On-Device Scan History**: Private SQLite database tracking scan UUIDs, timestamps, predictions, and uncertainty with downloadable diagnostic `.txt` reports.

---

## 2. Main System Modules

1. **🌿 Plant Identifier (`identify_plant`)**:
   - Camera input / photo uploader.
   - Searchable directory of verified botanical profiles across Fruits, Vegetables, Cereals, Legumes, Medicinal Plants, Spices, Flowers, and Trees.
   - Distinct AI support labels: *Information Only*, *Supported by Disease Model*, or *Both*.
2. **🔬 Disease Detection (`check_crop`)**:
   - Screen leaves for **Tomato** diseases using MobileNetV2.
   - Strict crop-compatibility check preventing cross-crop diagnosis for **Paddy (rice)** and **Groundnut** until dedicated models are trained.
   - Automatic record saving to local SQLite history upon confident diagnosis.
3. **🪴 Plant Care Assistant (`plant_care`)**:
   - Personalized care profiles: Sunlight, watering intervals, soil pH, common pests, and verified ICAR/TNAU references.
4. **🐛 Pests & Symptoms Educational Directory (`pests_symptoms`)**:
   - Educational investigation of field symptoms: Yellowing leaves, brown/black spots, wilting, holes in leaves, leaf curling, and white powdery growth.
5. **🌦️ Weather Alerts (`weather`)**:
   - Live Open-Meteo integration with responsive 5-day forecast cards and agricultural risk advisories.
6. **📚 Agricultural Advice (`advice`)**:
   - Expandable disease profiles with symptoms, prevention, cultural management, monitoring, safe chemical treatment guidelines, and consultation thresholds.
7. **🏛️ Government Schemes (`schemes`)**:
   - Official information for PM-KISAN, PMFBY, Soil Health Card, and Tamil Nadu Kalaignar Scheme with direct portal links.
8. **📜 Scan History (`scan_history`)**:
   - On-device SQLite audit log with single-scan deletion, history clearing, and structured `.txt` report downloads.

---

## 3. Project Architecture

```
ai_early_warning_system_for_farmers/
├── app.py                     # Main Streamlit web application & navigation
├── train_model.py             # MobileNetV2 transfer learning training pipeline
├── weather.py                 # Open-Meteo geocoding, 5-day forecast & alert rules
├── utils.py                   # Image validation, preprocessing, i18n & prediction rules
├── scan_history.py            # SQLite scan persistence & report generator
├── requirements.txt           # Dependency specification
├── README.md                  # Comprehensive documentation & setup guide
├── model.h5                   # Created ONLY after executing train_model.py with dataset
├── class_names.json           # Output layer class mapping aligned with model.h5
├── data/
│   ├── plants.json            # Botanical profiles, care conditions, pests & safety
│   ├── species_registry.json  # Model class mappings, training & evaluation statuses
│   ├── symptoms.json          # Visual field symptoms & educational cause mapping
│   ├── diseases.json          # Structured agricultural disease & treatment knowledge
│   ├── schemes.json           # Government schemes & verified portal links
│   └── i18n.json              # Bilingual UI strings (English & Tamil)
├── tests/
│   ├── test_data.py           # Validates JSON schemas, registry, and scan history
│   ├── test_utils.py          # Validates image handling, crop checks & 60% rule
│   └── test_weather.py        # Validates geocoding, forecast parsing & weather rules
└── docs/                      # Screenshots and documentation artifacts
```

---

## 4. How to Add New Plant Species or Retrain Models

### 1. Adding a New Plant to the Knowledge Base
1. Open `data/plants.json`.
2. Add a new entry with `plant_id`, `common_name` (`en` and `ta`), `scientific_name`, `family`, `category`, `growing_conditions`, `common_pests`, and `prevention_care`.
3. Set `support_status` to `"info_only"` until an image model is trained.

### 2. Registering and Training a New Disease or Identification Model
1. In `data/species_registry.json`, add the planned classes under `supported_species`.
2. Place labelled images under `dataset/<Class_Name>/`.
3. Run:
   ```powershell
   python train_model.py --data_dir dataset --epochs 10 --batch_size 32
   ```
4. Update `class_names.json` and verify `model.h5`.

---

## 5. Running the Application

### 1. Run Automated Test Suite (17 Tests)
```powershell
cd "C:\Users\shahu\AI Early Warning\ai_early_warning_system_for_farmers"
python -m pytest tests -v
```

### 2. Launch Streamlit Application
```powershell
python -m streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 6. Disclaimers

> [!WARNING]
> **Agricultural Decision-Support Disclaimer**:
> AI Plant Doctor is an academic major-project prototype. Predictions are decision-support indicators, not guarantees. Consult certified Block Agricultural Officers (AAO) or Krishi Vigyan Kendra (KVK) specialists before applying chemicals.
