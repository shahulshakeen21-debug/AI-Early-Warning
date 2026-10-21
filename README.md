# AI Plant Doctor — Smart Plant Identification & Farming Early Warning System
**விவசாயிகளுக்கான AI முன் எச்சரிக்கை அமைப்பு**  
*Better Plants. Healthier Crops. Brighter Future*

An intelligent agro-meteorological advisory and crop health diagnostics web application built for farmers, agricultural students, and researchers.

---

## 🌟 Project Architecture

This repository contains two complete implementations:
1. **`ai-plant-doctor-web/`**: Full-scale, responsive modern web application built with **React 19, TypeScript, Vite, Tailwind CSS, Zustand, i18next (English & Tamil), and Node/Express proxy**.
2. **`ai_early_warning_system_for_farmers/`**: Python & Streamlit application featuring Open-Meteo weather integrations, automated agricultural risk rules, plant database, and automated pytest test suites.

---

## 🚀 Quick Start Guide

### 1. Modern Web Application (React + Vite)
```bash
cd ai-plant-doctor-web
npm install

# Start the Node.js API proxy (keeps keys secure)
node server.js

# In a separate terminal, launch the web app
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

### 2. Streamlit Application (Python)
```bash
cd ai_early_warning_system_for_farmers
pip install -r requirements.txt
python -m streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📋 Features
- **Botanical Identification & Disease Detection**: Instant classification of leaf samples with clinical symptom breakdowns and recommended treatment schedules.
- **Bilingual Interface**: Seamless instant toggle between English and Tamil (தமிழ்).
- **Live Agro-Meteorology (Open-Meteo API)**: 5-day weather forecasts with automated fungal disease risk, heat stress, and spray window advisories.
- **Botanical Species Catalog**: Searchable plant database with scientific names and disease vulnerability profiles.
- **Agricultural Welfare Schemes**: Curated details and direct links for PM-KISAN, PMFBY, Soil Health Card, and Kisan Credit Card (KCC).
- **On-Device Diagnostic History & PDF Reports**: Store diagnostic history in IndexedDB and download official PDF reports via `jsPDF`.
