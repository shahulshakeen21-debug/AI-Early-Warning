# AI Plant Doctor — Smart Plant Identification, Disease Detection & Farming Early Warning System
**விவசாயிகளுக்கான AI முன் எச்சரிக்கை அமைப்பு**  
*Better Plants. Healthier Crops. Brighter Future*

---

## 🌟 Overview
**AI Plant Doctor** is a production-ready, mobile-first responsive web application built with **React 19, Vite, TypeScript, Tailwind CSS, Zustand, and React Router**. It matches the UI design showcase pixel-closely across all 12 functional screens, featuring bilingual English/Tamil support, live Open-Meteo weather forecasts, automated crop risk alerts, IndexedDB scan history, and PDF report downloads.

---

## 📱 Implemented Showcase Screens

| # | Screen | Route | Description |
|---|---|---|---|
| **1** | **Home Dashboard** | `/` | Hero banner with farmland photography, welcome text, 2×2 feature cards (*Scan a Plant, Weather Alerts, Plant Care & Advice, Government Schemes*), and agricultural decision-support disclaimer. |
| **2** | **Plant Scan** | `/scan` | 3 tabs (*Take Photo via camera, Upload Image with 5MB client-side compression, Gallery presets*), category selector, drag-and-drop zone, and `Analyze Image` CTA. |
| **3** | **Plant Identification Result** | `/result/identify` | High-res photo view with 3 side thumbnails, green *Plant Identified* card (species name, scientific name, confidence badge), *About this plant*, and *Check for Diseases* button. |
| **4** | **Disease Detection Result** | `/result/disease` | Leaf image banner, red *Disease Detected* card with severity/confidence (or green *Healthy Plant* variant), symptoms list, actionable guidance, and *View Detailed Advice*. |
| **5** | **Weather Alerts** | `/weather` | Place search + GPS geolocation + lat/long inputs, 5-day daily forecast cards (day, weather icon, max/min temp, rain mm, humidity %), and colored *Fungal Disease Risk* advisory cards. |
| **6** | **Plant Database** | `/plants` | Search bar, category filters, and species cards with real leaf photos, scientific names, and status badges (*Disease Model, Identification Model, Supported, Verified*). |
| **7** | **Plant Care & Advice** | `/care` | Dual dropdowns (Plant + Disease) with 8 expandable accordions (*About the Disease, Symptoms, Prevention Methods, Cultural Management, Monitoring Tips, Treatment Guidance, When to Consult Expert, References*). |
| **8** | **Government Schemes** | `/schemes` | Cards for PM-KISAN, PMFBY (Crop Insurance), Soil Health Card, PMKSY, and KCC with benefits, eligibility, application steps, and direct official `.gov.in` portal buttons. |
| **9** | **Tamil Language Interface** | Global | Full English / தமிழ் toggle persisted in `localStorage`. Instantly switches all headings, alerts, advice, and button labels. |
| **10** | **Mobile-First Responsive Shell** | Global | Centered 430px mobile frame on desktop with camera grill and sticky bottom navigation; responsive viewport on mobile devices. |
| **11** | **Scan History** | `/history` | On-device IndexedDB storage of previous scans with leaf thumbnails, dates, confidence scores, individual PDF export buttons, and deletion. |
| **12** | **Scan Report Download** | `/report/:id` | Formal diagnosis report card with botanical details, symptoms, actions, weather snapshot, and instant single-click PDF generation via `jsPDF` & `html2canvas`. |

---

## 🚀 Running the Project Locally

### 1. Prerequisites
- **Node.js**: v18+ (verified on Node v24.18.0)
- **npm**: v9+

### 2. Setup & Installation
```bash
cd "c:\Users\shahu\AI Early Warning\ai-plant-doctor-web"
npm install
```

### 3. Start the Backend API Proxy
Keeps API keys secure and proxies plant identification and botanical summary requests:
```bash
node server.js
# Runs on http://localhost:3001
```

### 4. Start the Frontend Vite Server
In a new terminal window:
```bash
npm run dev
# Opens at http://localhost:5173
```

---

## 🔑 Environment Configuration (.env)
Create a `.env` file in the `ai-plant-doctor-web` root directory (see `.env.example`):
```env
PORT=3001
PLANT_ID_API_KEY=your_plant_id_api_key_here
PLANTNET_API_KEY=your_plantnet_api_key_here
```
*Note: If no API key is specified, the server gracefully activates its built-in smart agricultural rule engine.*

---

## 🛠️ Verification & Build
The application compiles cleanly with zero TypeScript or Vite errors:
```bash
npm run build
```
Output:
```
dist/index.html                        0.96 kB
dist/assets/index.css                 33.47 kB
dist/assets/index.js                 1,097.62 kB
✓ built successfully
```
