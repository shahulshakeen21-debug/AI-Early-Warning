"""
app.py  —  AI Plant Doctor  v3.0
Smart Plant Identification, Disease Detection & Farming Early Warning System
UI redesigned to match reference exactly: 11 screens, back-navigation, footer bar.
"""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from PIL import Image
import streamlit as st

import report
import scan_history
import utils
import weather

# ── page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Plant Doctor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── paths ──────────────────────────────────────────────────────────────────────
BASE_DIR         = Path(__file__).resolve().parent
DATA_DIR         = BASE_DIR / "data"
I18N_PATH        = DATA_DIR / "i18n.json"
DISEASES_PATH    = DATA_DIR / "diseases.json"
SCHEMES_PATH     = DATA_DIR / "schemes.json"
PLANTS_PATH      = DATA_DIR / "plants.json"
REGISTRY_PATH    = DATA_DIR / "species_registry.json"
SYMPTOMS_PATH    = DATA_DIR / "symptoms.json"
MODEL_PATH       = BASE_DIR / "model.h5"
CLASS_NAMES_PATH = BASE_DIR / "class_names.json"

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("app")

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS  —  matches reference image exactly
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Tamil:wght@400;500;600;700&display=swap');

/* ── base reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

:root {
  --g9: #14532d;
  --g8: #166534;
  --g7: #15803d;
  --g6: #16a34a;
  --g5: #22c55e;
  --g1: #dcfce7;
  --g0: #f0fdf4;
  --white: #ffffff;
  --bg: #f8fafc;
  --border: #e2e8f0;
  --t1: #0f172a;
  --t2: #334155;
  --t3: #64748b;
  --amber: #f59e0b;
  --amber-bg: #fffbeb;
  --red: #dc2626;
  --red-bg: #fef2f2;
  --blue: #2563eb;
  --blue-bg: #eff6ff;
  --r8: 8px;
  --r12: 12px;
  --r16: 16px;
  --sh1: 0 1px 3px rgba(0,0,0,.08);
  --sh2: 0 4px 12px rgba(0,0,0,.1);
}

.stApp {
  background: var(--bg) !important;
  font-family: 'Inter','Noto Sans Tamil',sans-serif !important;
  color: var(--t1) !important;
}

/* hide chrome */
#MainMenu,footer,header,[data-testid="collapsedControl"] { display:none !important; }
.stDeployButton { display:none !important; }

/* block container */
.main .block-container {
  padding: 0 0 80px 0 !important;
  max-width: 820px !important;
  margin: 0 auto !important;
}

/* ── TOP HERO HEADER (home only) ── */
.hero-header {
  background: linear-gradient(120deg,#14532d 0%,#166534 45%,#15803d 100%);
  padding: 1.1rem 1.4rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}
.hero-header::after {
  content: "";
  position: absolute;
  right: 0; top: 0; bottom: 0;
  width: 200px;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 80"><rect width="200" height="80" fill="%23166534" opacity=".4"/></svg>') center/cover;
  opacity: .3;
}
.hero-brand { display:flex; align-items:center; gap:.7rem; }
.hero-leaf { font-size:2rem; filter:drop-shadow(0 2px 4px rgba(0,0,0,.3)); }
.hero-title { font-size:1.55rem; font-weight:800; color:#fff; letter-spacing:-.025em; line-height:1.1; }
.hero-sub   { font-size:.78rem; color:rgba(255,255,255,.82); font-weight:400; margin-top:.15rem; }
.hero-slogan {
  text-align:right; color:#fff; font-size:.85rem; font-weight:700; line-height:1.4;
  position:relative; z-index:1;
}
.hero-slogan small { display:block; font-size:.72rem; font-weight:400; opacity:.85; }

/* ── PAGE HEADER (inner pages) ── */
.page-header {
  background: linear-gradient(120deg,#14532d,#15803d);
  padding: .75rem 1.1rem .65rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.ph-brand { display:flex; align-items:center; gap:.5rem; }
.ph-leaf  { font-size:1.3rem; }
.ph-title { font-size:1rem; font-weight:800; color:#fff; }
.ph-sub   { font-size:.68rem; color:rgba(255,255,255,.8); }
.ph-right { display:flex; align-items:center; gap:.6rem; }
.loc-pill {
  background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.3);
  border-radius:20px; padding:.22rem .65rem;
  font-size:.72rem; color:#fff; font-weight:500;
}
.lang-pill {
  background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.3);
  border-radius:20px; padding:.22rem .65rem;
  font-size:.75rem; color:#fff; font-weight:700; cursor:pointer;
}

/* ── BACK BAR ── */
.back-bar {
  background:#fff; border-bottom:1px solid var(--border);
  padding:.55rem 1.1rem;
  display:flex; align-items:center; gap:.5rem;
  font-size:.85rem; font-weight:600; color:var(--g8);
  cursor:pointer;
}
.back-bar span { font-size:1rem; }

/* ── WELCOME CARD (home screen) ── */
.welcome-card {
  background: linear-gradient(135deg,#166534 0%,#15803d 100%);
  margin: .75rem .75rem .6rem;
  border-radius: var(--r16);
  padding: 1.2rem 1.3rem 1rem;
  color:#fff; position:relative; overflow:hidden;
}
.welcome-card::before {
  content:"🌾";
  position:absolute; right:.8rem; bottom:-.2rem;
  font-size:3.5rem; opacity:.15;
}
.welcome-card h2 { font-size:1.25rem; font-weight:800; margin-bottom:.3rem; }
.welcome-card p  { font-size:.84rem; color:rgba(255,255,255,.9); line-height:1.5; }

/* ── FEATURE CARDS GRID ── */
.feat-grid {
  display:grid; grid-template-columns:1fr 1fr;
  gap:.65rem; padding:0 .75rem .75rem;
}
.feat-card {
  background:#fff; border:1px solid var(--border); border-radius:var(--r12);
  padding:1rem .95rem .9rem; box-shadow:var(--sh1);
  transition:box-shadow .18s,transform .15s;
}
.feat-card:hover { box-shadow:var(--sh2); transform:translateY(-1px); }
.fc-icon {
  width:40px; height:40px; border-radius:10px;
  background:var(--g0); display:flex; align-items:center; justify-content:center;
  font-size:1.3rem; margin-bottom:.5rem;
}
.fc-title { font-size:.97rem; font-weight:700; color:var(--t1); margin-bottom:.25rem; }
.fc-desc  { font-size:.8rem; color:var(--t3); line-height:1.45; margin-bottom:.7rem; }

/* ── SECTION WRAPPER ── */
.section-wrap { padding:.75rem .75rem 0; }
.section-title {
  font-size:1.05rem; font-weight:700; color:var(--t1); margin-bottom:.15rem;
}
.section-sub { font-size:.82rem; color:var(--t3); margin-bottom:.8rem; }

/* ── UNIVERSAL CARD ── */
.ucard {
  background:#fff; border:1px solid var(--border); border-radius:var(--r12);
  padding:1rem 1.1rem; box-shadow:var(--sh1); margin-bottom:.7rem;
}
.ucard-title { font-size:.95rem; font-weight:700; color:var(--t1); margin-bottom:.3rem; }

/* ── RESULT BANNER ── */
.res-banner {
  border-radius:var(--r12); padding:.95rem 1.1rem;
  display:flex; align-items:flex-start; gap:.8rem; margin-bottom:.75rem;
}
.res-disease  { background:var(--red-bg);  border-left:5px solid var(--red);   }
.res-healthy  { background:var(--g0);      border-left:5px solid var(--g6);    }
.res-uncertain{ background:var(--amber-bg);border-left:5px solid var(--amber); }
.res-info     { background:var(--blue-bg); border-left:5px solid var(--blue);  }
.res-icon { font-size:1.9rem; line-height:1; flex-shrink:0; }
.res-label {
  font-size:.7rem; font-weight:800; text-transform:uppercase; letter-spacing:.07em;
  margin-bottom:.18rem;
}
.red-label   { color:var(--red); }
.green-label { color:var(--g7); }
.amber-label { color:#92400e; }
.blue-label  { color:var(--blue); }
.res-name { font-size:1.15rem; font-weight:800; color:var(--t1); margin-bottom:.1rem; }
.res-sci  { font-size:.8rem; color:var(--t2); font-style:italic; }
.conf-chip {
  display:inline-block; border-radius:20px;
  padding:.18rem .65rem; font-size:.78rem; font-weight:700; margin-top:.35rem;
}
.chip-green { background:var(--g7); color:#fff; }
.chip-red   { background:var(--red); color:#fff; }
.chip-amber { background:var(--amber); color:#fff; }
.chip-blue  { background:var(--blue); color:#fff; }

/* ── INFO ROWS (plant result) ── */
.info-row {
  display:flex; gap:.5rem; align-items:baseline;
  font-size:.84rem; padding:.32rem 0; border-bottom:1px solid var(--border);
}
.info-row:last-child { border-bottom:none; }
.ir-label { color:var(--t3); font-weight:600; min-width:120px; font-size:.8rem; }
.ir-val   { color:var(--t1); }
.check-green { color:var(--g7); font-weight:700; }

/* ── BULLET LIST ── */
.blist { list-style:none; padding:0; }
.blist li {
  padding:.38rem 0 .38rem 1.3rem; position:relative;
  font-size:.86rem; color:var(--t2); border-bottom:1px solid var(--border);
}
.blist li:last-child { border-bottom:none; }
.blist li::before {
  content:"•"; position:absolute; left:.35rem;
  color:var(--g6); font-weight:900;
}

/* ── WEATHER FORECAST CARD ── */
.wday {
  background:#fff; border:1px solid var(--border); border-radius:var(--r12);
  padding:.75rem .5rem; text-align:center; box-shadow:var(--sh1);
}
.wday .wd-day  { font-size:.72rem; font-weight:800; color:var(--t3); text-transform:uppercase; letter-spacing:.05em; }
.wday .wd-date { font-size:.75rem; color:var(--g7); font-weight:600; margin:.1rem 0 .3rem; }
.wday .wd-icon { font-size:1.5rem; margin:.1rem 0; }
.wday .wd-temp { font-size:1rem; font-weight:800; color:var(--t1); }
.wday .wd-rain { font-size:.7rem; color:var(--blue); margin-top:.15rem; }
.wday .wd-hum  { font-size:.68rem; color:var(--t3); }

/* weather alert boxes */
.walert {
  border-radius:var(--r8); padding:.8rem 1rem; margin-bottom:.6rem;
  display:flex; gap:.65rem; align-items:flex-start;
}
.walert.fungal { background:var(--amber-bg); border-left:4px solid var(--amber); }
.walert.heat   { background:var(--red-bg);   border-left:4px solid var(--red);   }
.walert.spray  { background:var(--blue-bg);  border-left:4px solid var(--blue);  }
.walert.ok     { background:var(--g0);       border-left:4px solid var(--g6);    }
.wa-head { font-weight:700; font-size:.88rem; margin-bottom:.18rem; color:var(--t1); }
.wa-text { font-size:.8rem; color:var(--t2); line-height:1.45; }

/* ── PLANT DATABASE CARD ── */
.pdb-card {
  background:#fff; border:1px solid var(--border); border-radius:var(--r12);
  padding:.85rem 1rem; margin-bottom:.6rem; box-shadow:var(--sh1);
  display:flex; gap:.85rem; align-items:flex-start;
}
.pdb-thumb {
  width:54px; height:54px; border-radius:var(--r8);
  background:var(--g0); display:flex; align-items:center;
  justify-content:center; font-size:1.7rem; flex-shrink:0;
}
.pdb-name { font-size:.97rem; font-weight:700; color:var(--t1); }
.pdb-sci  { font-size:.78rem; color:var(--t3); font-style:italic; }
.pdb-cat  { font-size:.76rem; color:var(--g7); font-weight:600; margin:.15rem 0; }
.pill {
  display:inline-block; border-radius:20px; font-size:.67rem; font-weight:700;
  padding:.16rem .52rem; margin-right:.3rem; margin-top:.2rem;
}
.pill-green  { background:#dcfce7; color:#166534; }
.pill-yellow { background:#fef9c3; color:#854d0e; }
.pill-blue   { background:#dbeafe; color:#1e40af; }
.pill-gray   { background:#f1f5f9; color:#475569; }

/* ── SCHEME CARD ── */
.sc-card {
  background:#fff; border:1px solid var(--border); border-radius:var(--r12);
  padding:1rem 1.1rem; margin-bottom:.85rem; box-shadow:var(--sh1);
}
.sc-title { font-size:.98rem; font-weight:800; color:var(--t1); margin-bottom:.25rem; }
.sc-badge {
  display:inline-block; background:var(--g0); color:var(--g8);
  font-size:.68rem; font-weight:700; border-radius:20px;
  padding:.16rem .58rem; margin-bottom:.55rem;
}
.sc-row { display:flex; gap:.4rem; margin-bottom:.22rem; font-size:.83rem; }
.sc-lbl { color:var(--t3); font-weight:600; min-width:90px; font-size:.78rem; flex-shrink:0; }
.sc-val { color:var(--t2); line-height:1.4; }
.sc-link a {
  display:inline-flex; align-items:center; gap:.3rem;
  background:var(--g7); color:#fff; border-radius:var(--r8);
  padding:.4rem .9rem; font-size:.82rem; font-weight:700;
  text-decoration:none; margin-top:.55rem;
}
.sc-link a:hover { background:var(--g8); }

/* ── HISTORY ITEM ── */
.hist-item {
  background:#fff; border:1px solid var(--border); border-radius:var(--r12);
  padding:.85rem 1rem; margin-bottom:.6rem; box-shadow:var(--sh1);
  display:flex; align-items:flex-start; gap:.8rem;
}
.hist-dot {
  width:40px; height:40px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:1.2rem; flex-shrink:0;
}
.hd-disease { background:var(--red-bg); }
.hd-healthy { background:var(--g0); }
.hd-info    { background:var(--blue-bg); }
.hist-plant  { font-size:.93rem; font-weight:700; color:var(--t1); }
.hist-result { font-size:.81rem; color:var(--t2); margin:.1rem 0; }
.hist-conf   { font-size:.76rem; color:var(--t3); }
.hist-ts     { font-size:.7rem;  color:var(--t3); margin-top:.15rem; }

/* ── DISCLAIMER ── */
.disc-box {
  background:var(--blue-bg); border-left:4px solid var(--blue);
  border-radius:var(--r8); padding:.8rem 1rem;
  font-size:.81rem; color:var(--t2); line-height:1.5; margin:.75rem 0;
}
.disc-box strong { color:var(--t1); }

/* ── UPLOAD AREA ── */
.upload-drop {
  border:2px dashed var(--border); border-radius:var(--r12);
  background:#fff; padding:1.8rem 1rem; text-align:center;
  color:var(--t3); margin-bottom:.8rem; cursor:pointer;
}
.upload-drop:hover { border-color:var(--g6); background:var(--g0); }
.upload-drop .ud-icon { font-size:2rem; margin-bottom:.4rem; }
.upload-drop .ud-text { font-size:.85rem; font-weight:500; }
.upload-drop .ud-hint { font-size:.75rem; color:var(--t3); margin-top:.2rem; }

/* ── BUTTONS ── */
div.stButton > button {
  background:var(--g8) !important; color:#fff !important;
  border:none !important; border-radius:var(--r8) !important;
  font-weight:700 !important; font-size:.9rem !important;
  padding:.52rem 1rem !important; min-height:42px !important;
  width:100% !important; transition:background .18s,box-shadow .18s !important;
  box-shadow:0 2px 6px rgba(22,101,52,.28) !important;
}
div.stButton > button:hover {
  background:var(--g9) !important;
  box-shadow:0 4px 12px rgba(22,101,52,.38) !important;
}
div.stButton > button[kind="secondary"] {
  background:var(--white) !important; color:var(--g8) !important;
  border:1.5px solid var(--g7) !important;
  box-shadow:none !important;
}
div.stDownloadButton > button {
  background:var(--g8) !important; color:#fff !important;
  border-radius:var(--r8) !important; font-weight:700 !important;
  width:100% !important;
}

/* file uploader */
[data-testid="stFileUploader"] section {
  border:2px dashed var(--border) !important;
  border-radius:var(--r12) !important;
  background:#fff !important;
}

/* expanders */
.streamlit-expanderHeader {
  background:#fff !important; border-radius:var(--r8) !important;
  font-weight:600 !important; font-size:.9rem !important;
}
details[open] .streamlit-expanderHeader {
  border-radius:var(--r8) var(--r8) 0 0 !important;
}

/* select / text */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] input {
  border-radius:var(--r8) !important; border-color:var(--border) !important;
  font-size:.88rem !important;
}

/* tabs */
button[data-baseweb="tab"] { font-weight:600 !important; font-size:.86rem !important; }
button[data-baseweb="tab"][aria-selected="true"] {
  color:var(--g8) !important; border-bottom-color:var(--g8) !important;
}

/* ── FOOTER BAR ── */
.footer-bar {
  background:#fff; border-top:1px solid var(--border);
  padding:.65rem 1.1rem; display:flex; flex-wrap:wrap;
  align-items:center; justify-content:space-around; gap:.5rem;
  margin-top:1.2rem;
}
.fb-item {
  display:flex; align-items:center; gap:.3rem;
  font-size:.74rem; color:var(--t3); font-weight:500;
}
.fb-icon { font-size:1rem; }

/* ── BOTTOM NAV ── */
.bnav {
  position:fixed; bottom:0; left:0; right:0;
  background:#fff; border-top:1px solid var(--border);
  display:flex; justify-content:space-around; padding:.45rem 0 .55rem;
  z-index:999; box-shadow:0 -2px 10px rgba(0,0,0,.07);
}
.bn-item {
  display:flex; flex-direction:column; align-items:center; gap:2px;
  font-size:.62rem; color:var(--t3); font-weight:500; min-width:52px;
}
.bn-item.active { color:var(--g8) !important; font-weight:700; }
.bn-icon { font-size:1.25rem; line-height:1; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
_DEFAULTS = dict(
    lang="en", page="home",
    scan_image=None, scan_source=None,
    last_result=None, last_plant=None, last_disease=None,
    weather_data=None, weather_loc=None, weather_coords=None,
    care_plant=None, care_disease=None,
    db_plant=None,
)
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

scan_history.init_db()

# ══════════════════════════════════════════════════════════════════════════════
# CACHED DATA
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def _load_all():
    return (
        utils.load_json_file(I18N_PATH),
        utils.load_json_file(DISEASES_PATH),
        utils.load_json_file(SCHEMES_PATH),
        utils.load_json_file(PLANTS_PATH),
        utils.load_json_file(REGISTRY_PATH),
        utils.load_json_file(SYMPTOMS_PATH),
    )

i18n_db, diseases_db, schemes_db, plants_db, registry_db, symptoms_db = _load_all()

@st.cache_resource(show_spinner=False)
def _load_model():
    if not MODEL_PATH.exists():
        return None, None, "model.h5 not found — run train_model.py first."
    try:
        import tensorflow as tf
        m = tf.keras.models.load_model(str(MODEL_PATH))
        with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
            cls = json.load(f)
        return m, cls, None
    except ImportError:
        return None, None, "TensorFlow not installed."
    except Exception as e:
        return None, None, str(e)

model, class_names, model_error = _load_model()
MODEL_OK = model is not None

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def t(key: str) -> str:
    return utils.get_text(i18n_db, key, st.session_state.lang)

def go(page: str, **kw):
    st.session_state.page = page
    for k, v in kw.items():
        st.session_state[k] = v
    st.rerun()

def _en(lang): return lang == "en"

def _plant_emoji(cat: str) -> str:
    return {"vegetables":"🍅","fruits":"🍋","cereals":"🌾","pulses":"🫘",
            "spices":"🌶️","flowers":"🌸","trees":"🌳","herbs":"🌿"}.get(
            (cat or "").lower(), "🌱")

def _wicon(temp, rain_p) -> str:
    rp = rain_p or 0
    if rp > 65: return "🌧️"
    if rp > 35: return "⛅"
    if (temp or 0) > 35: return "☀️"
    return "🌤️"

def _pill(label, cls): return f'<span class="pill {cls}">{label}</span>'

def _lang_toggle():
    st.session_state.lang = "ta" if st.session_state.lang == "en" else "en"
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# HEADER COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════
def _home_header():
    lang = st.session_state.lang
    loc = st.session_state.weather_loc or ""
    loc_html = f'<span class="loc-pill">📍 {loc}</span>' if loc else ""
    lbl = "தமிழ்" if _en(lang) else "English"

    col_h, col_l = st.columns([5, 1])
    with col_h:
        st.markdown(f"""
        <div class="hero-header">
          <div class="hero-brand">
            <span class="hero-leaf">🌿</span>
            <div>
              <div class="hero-title">AI Plant Doctor</div>
              <div class="hero-sub">Smart Plant Identification, Disease Detection & Farming Early Warning System</div>
              {loc_html}
            </div>
          </div>
          <div class="hero-slogan">
            Healthy Plants<br>Better Harvests<br>Brighter Future
            <small>விவசாயிகளுக்கான AI</small>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_l:
        st.markdown("<div style='margin-top:.4rem'></div>", unsafe_allow_html=True)
        if st.button(lbl, key="lang_btn_home"):
            _lang_toggle()

def _page_header(title: str, show_back: bool = True):
    lang = st.session_state.lang
    lbl  = "தமிழ்" if _en(lang) else "English"
    loc  = st.session_state.weather_loc or ""
    loc_html = f'<span class="loc-pill">📍 {loc}</span>' if loc else ""

    col_h, col_l = st.columns([5, 1])
    with col_h:
        st.markdown(f"""
        <div class="page-header">
          <div class="ph-brand">
            <span class="ph-leaf">🌿</span>
            <div>
              <div class="ph-title">AI Plant Doctor</div>
              <div class="ph-sub">English / தமிழ்</div>
            </div>
          </div>
          <div class="ph-right">{loc_html}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_l:
        st.markdown("<div style='margin-top:.3rem'></div>", unsafe_allow_html=True)
        if st.button(lbl, key=f"lang_btn_{title[:6]}"):
            _lang_toggle()

    if show_back:
        if st.button("← Back", key=f"back_{title[:8]}_{st.session_state.page}"):
            go("home")
    st.markdown(f"<div class='section-wrap'><p class='section-title'>{title}</p></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM NAV
# ══════════════════════════════════════════════════════════════════════════════
_NAV = [
    ("home",     "🏠", "Home",     "முகப்பு"),
    ("scan",     "🔬", "Scan",     "ஸ்கேன்"),
    ("weather",  "🌦️", "Weather",  "வானிலை"),
    ("database", "🌿", "Database", "தரவு"),
    ("history",  "📜", "History",  "வரலாறு"),
    ("more",     "⋯",  "More",     "மேலும்"),
]

def _bottom_nav():
    lang = st.session_state.lang
    cols = st.columns(len(_NAV))
    for col, (pg, icon, en_lbl, ta_lbl) in zip(cols, _NAV):
        active = "active" if st.session_state.page == pg else ""
        label  = en_lbl if _en(lang) else ta_lbl
        with col:
            if st.button(f"{icon}\n{label}", key=f"bn_{pg}"):
                go(pg)

# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 1 — HOME DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def screen_home():
    lang = st.session_state.lang
    _home_header()

    # Welcome card
    if _en(lang):
        wt = "Welcome, Farmer! 👋"
        wd = "Get instant plant identification, disease detection, weather alerts and expert guidance."
    else:
        wt = "வரவேற்கிறோம், விவசாயி! 👋"
        wd = "உடனடி தாவர அடையாளம், நோய் கண்டறிதல், வானிலை எச்சரிக்கை மற்றும் நிபுணர் வழிகாட்டல் பெறுங்கள்."

    st.markdown(f"""
    <div class="welcome-card">
      <h2>{wt}</h2>
      <p>{wd}</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards 2×2
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="feat-card">
          <div class="fc-icon">🌿</div>
          <div class="fc-title">{'Scan a Plant' if _en(lang) else 'தாவர ஸ்கேன்'}</div>
          <div class="fc-desc">{'Identify plants and detect diseases using AI.' if _en(lang) else 'AI மூலம் தாவர அடையாளம் மற்றும் நோய் கண்டறிதல்.'}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔬  Scan Now" if _en(lang) else "🔬  இப்போது ஸ்கேன்", key="h_scan"):
            go("scan")
    with c2:
        st.markdown(f"""
        <div class="feat-card">
          <div class="fc-icon">🌦️</div>
          <div class="fc-title">{'Weather Alerts' if _en(lang) else 'வானிலை எச்சரிக்கை'}</div>
          <div class="fc-desc">{'Get local weather and crop risk alerts.' if _en(lang) else 'உள்ளூர் வானிலை மற்றும் பயிர் இடர் எச்சரிக்கைகள்.'}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌦️  View Weather" if _en(lang) else "🌦️  வானிலை பார்க்க", key="h_wx"):
            go("weather")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
        <div class="feat-card">
          <div class="fc-icon">🌱</div>
          <div class="fc-title">{'Plant Care & Advice' if _en(lang) else 'தாவர பராமரிப்பு'}</div>
          <div class="fc-desc">{'Learn about plant care, pests and diseases.' if _en(lang) else 'தாவர பராமரிப்பு, பூச்சிகள் பற்றி அறிக.'}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌱  Get Advice" if _en(lang) else "🌱  ஆலோசனை பெற", key="h_care"):
            go("care")
    with c4:
        st.markdown(f"""
        <div class="feat-card">
          <div class="fc-icon">🏛️</div>
          <div class="fc-title">{'Government Schemes' if _en(lang) else 'அரசு திட்டங்கள்'}</div>
          <div class="fc-desc">{'Explore schemes and official links.' if _en(lang) else 'திட்டங்கள் மற்றும் அதிகாரப்பூர்வ இணைப்புகள்.'}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏛️  View Schemes" if _en(lang) else "🏛️  திட்டங்கள்", key="h_sch"):
            go("schemes")

    # Disclaimer
    st.markdown(f"""
    <div class="disc-box" style="margin:.6rem .75rem 0">
      ℹ️ <strong>{'Decision Support' if _en(lang) else 'முடிவு ஆதரவு'}:</strong>
      {'Predictions may be less accurate on real field photos. This is decision support, not a replacement for experts.' if _en(lang)
       else 'உண்மையான வயல் புகைப்படங்களில் கணிப்புகள் குறைவான துல்லியமாக இருக்கலாம். இது நிபுணர்களுக்கு மாற்றாக அல்ல.'}
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 2 — PLANT SCAN
# ══════════════════════════════════════════════════════════════════════════════
def screen_scan():
    lang = st.session_state.lang
    _page_header("Scan a Plant" if _en(lang) else "தாவர ஸ்கேன்")

    st.markdown(f"<div class='section-wrap'><p class='section-sub'>{'Upload a photo or take a picture to identify the plant and check for diseases.' if _en(lang) else 'தாவரத்தை அடையாளம் காண புகைப்படத்தை பதிவேற்றவும் அல்லது எடுக்கவும்.'}</p></div>",
                unsafe_allow_html=True)

    # Three-button row matching reference image
    tab_up, tab_cam = st.tabs([
        "📤  Upload Image" if _en(lang) else "📤  படம் பதிவேற்று",
        "📷  Take Photo"   if _en(lang) else "📷  படம் எடு",
    ])

    with tab_up:
        up = st.file_uploader(
            "Click to upload or drag and drop (JPG, PNG, JPEG)" if _en(lang)
            else "கிளிக் செய்து பதிவேற்றவும் (JPG, PNG, JPEG)",
            type=["jpg","jpeg","png"], key="fu_main"
        )
        if up:
            ok, err, img = utils.validate_image_file(up.getvalue())
            if ok:
                st.session_state.scan_image  = img
                st.session_state.scan_source = "upload"
            else:
                st.error(f"❌ {err}")

    with tab_cam:
        cam = st.camera_input("Take a photo" if _en(lang) else "படம் எடுங்கள்", key="cam_main")
        if cam:
            ok, err, img = utils.validate_image_file(cam.getvalue())
            if ok:
                st.session_state.scan_image  = img
                st.session_state.scan_source = "camera"
            else:
                st.error(f"❌ {err}")

    # Preview
    if st.session_state.scan_image:
        pr, cl = st.columns([4,1])
        with pr:
            st.image(st.session_state.scan_image, use_container_width=True,
                     caption="Selected image")
        with cl:
            st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)
            if st.button("🗑️" if _en(lang) else "நீக்கு", key="rm_img"):
                st.session_state.scan_image = None
                st.rerun()

    # Plant category
    keys   = list(plants_db.keys())
    labels = [plants_db[k]["common_name"].get(lang, plants_db[k]["common_name"].get("en",k)) for k in keys]
    lmap   = dict(zip(labels, keys))

    st.markdown(f"<div class='section-wrap'><p style='font-weight:600;font-size:.88rem;margin-bottom:.35rem'>{'Select Plant Category (optional)' if _en(lang) else 'தாவர வகை (விரும்பினால்)'}</p></div>",
                unsafe_allow_html=True)
    choice = st.selectbox("", ["-- Auto Detect --" if _en(lang) else "-- தானாக கண்டறி --"] + labels,
                           key="cat_sel", label_visibility="collapsed")

    st.markdown("<div style='padding:0 .75rem'>", unsafe_allow_html=True)
    if st.button("🔍  Analyze Image" if _en(lang) else "🔍  பகுப்பாய்வு செய்", key="analyse"):
        if not st.session_state.scan_image:
            st.warning("⚠️ Please upload or capture an image first." if _en(lang)
                       else "⚠️ முதலில் படம் பதிவேற்றவும் அல்லது எடுக்கவும்.")
        else:
            pid = None
            if choice and "Auto" not in choice and "தானாக" not in choice:
                pid = lmap.get(choice)
            _do_analysis(pid, lang)
    st.markdown("</div>", unsafe_allow_html=True)

    # Model notice
    if not MODEL_OK:
        st.markdown(f"""
        <div class="disc-box" style="margin:.7rem .75rem 0">
          ℹ️ <strong>{'AI Model Not Installed' if _en(lang) else 'AI மாடல் நிறுவப்படவில்லை'}:</strong>
          {model_error}
          {'Knowledge-base plant information will still be shown.' if _en(lang)
           else 'அறிவுத்தளத்திலிருந்து தகவல் காட்டப்படும்.'}
        </div>
        """, unsafe_allow_html=True)

    # Last result quick preview
    if st.session_state.last_result:
        st.markdown("---")
        _render_result(st.session_state.last_result, lang)


# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS LOGIC
# ══════════════════════════════════════════════════════════════════════════════
def _do_analysis(plant_id: Optional[str], lang: str):
    img = st.session_state.scan_image
    if not img: return

    with st.spinner("Analysing image…" if _en(lang) else "பகுப்பாய்வு செய்கிறது…"):
        if MODEL_OK:
            arr   = utils.preprocess_image_for_model(img)
            probs = model.predict(arr, verbose=0)[0]
            if plant_id:
                pinfo   = plants_db.get(plant_id, {})
                cname   = pinfo.get("common_name", {}).get("en", plant_id)
                ev      = utils.evaluate_prediction_result(probs, class_names, cname)
                result  = {"mode":"disease","plant_id":plant_id,"eval":ev}
            else:
                ev     = utils.evaluate_plant_identification_result(probs, class_names)
                result = {"mode":"identify","eval":ev}
        else:
            result = {"mode":"no_model","plant_id":plant_id}

        scan_ev = result.get("eval", {})
        sid = str(uuid.uuid4())[:8].upper()
        scan_history.save_scan(
            scan_uuid=sid,
            selected_plant=plant_id,
            scan_type=result["mode"],
            predicted_class=scan_ev.get("predicted_class") if scan_ev else None,
            confidence=scan_ev.get("confidence") if scan_ev else None,
            model_version="MobileNetV2-v2" if MODEL_OK else "KnowledgeBase",
            is_uncertain=not MODEL_OK or (scan_ev.get("status")=="low_confidence" if scan_ev else True),
        )
        result["scan_uuid"] = sid
        st.session_state.last_result  = result
        st.session_state.last_plant   = plant_id
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 3 — PLANT IDENTIFICATION RESULT
# ══════════════════════════════════════════════════════════════════════════════
def _render_result(result: Dict, lang: str):
    mode = result.get("mode","no_model")
    pid  = result.get("plant_id")
    pi   = plants_db.get(pid) if pid else None
    ev   = result.get("eval", {}) or {}
    st_v = ev.get("status","")

    if mode == "no_model":
        # Knowledge-base only
        st.markdown(f"<div class='section-wrap'><p class='section-title'>{'Plant Identification Result' if _en(lang) else 'தாவர அடையாள முடிவு'}</p></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="padding:0 .75rem">
        <div class="res-banner res-info">
          <div class="res-icon">ℹ️</div>
          <div>
            <div class="res-label blue-label">{'Information Only' if _en(lang) else 'தகவல் மட்டும்'}</div>
            <div class="res-name">{pi['common_name'].get(lang, pi['common_name']['en']) if pi else 'Unknown'}</div>
            <div class="res-sci">{pi.get('scientific_name','') if pi else ''}</div>
            <span class="conf-chip chip-blue">{'Knowledge Base' if _en(lang) else 'அறிவுத்தளம்'}</span>
          </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        if pi:
            _plant_info_block(pi, lang)
        if st.button("✅  Check for Diseases" if _en(lang) else "✅  நோய்களை சரிபார்க்கவும்", key="chk_dis_nb"):
            go("care", care_plant=pid)
        return

    if mode == "identify":
        st.markdown(f"<div class='section-wrap'><p class='section-title'>{'Plant Identification Result' if _en(lang) else 'தாவர அடையாள முடிவு'}</p></div>", unsafe_allow_html=True)
        if st_v == "identified":
            sp   = ev.get("predicted_species","Unknown")
            conf = ev.get("confidence", 0.0)
            mp   = plants_db.get(sp.lower().replace(" ","_"))
            nm   = mp["common_name"].get(lang, sp) if mp else sp
            sci  = mp.get("scientific_name","") if mp else ""
            st.markdown(f"""
            <div style="padding:0 .75rem">
            <div class="res-banner res-healthy">
              <div class="res-icon">🌿</div>
              <div>
                <div class="res-label green-label">{'Plant Identified' if _en(lang) else 'தாவரம் அடையாளம் காணப்பட்டது'}</div>
                <div class="res-name">{nm}</div>
                <div class="res-sci">{sci}</div>
                <span class="conf-chip chip-green">Confidence: {conf*100:.0f}%</span>
              </div>
            </div>
            </div>
            """, unsafe_allow_html=True)
            if mp:
                _plant_info_block(mp, lang)
                st.markdown("<div style='padding:0 .75rem'>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="disc-box">
                  ℹ️ {'This plant is supported by our identification model. You can now check for possible diseases.' if _en(lang) else 'இந்த தாவரம் எங்கள் அடையாள மாடல் ஆதரிக்கிறது. நோய்களை இப்போது சரிபார்க்கலாம்.'}
                </div>
                """, unsafe_allow_html=True)
                if st.button("✅  Check for Diseases" if _en(lang) else "✅  நோய்களை சரிபார்க்கவும்", key="chk_dis_id"):
                    go("care", care_plant=mp.get("plant_id"))
                st.markdown("</div>", unsafe_allow_html=True)
        elif st_v == "low_confidence":
            conf = ev.get("confidence",0.0)
            st.markdown(f"""
            <div style="padding:0 .75rem">
            <div class="res-banner res-uncertain">
              <div class="res-icon">⚠️</div>
              <div>
                <div class="res-label amber-label">{'Uncertain' if _en(lang) else 'நிச்சயமற்றது'}</div>
                <div class="res-name">{'Could not identify with certainty' if _en(lang) else 'நிச்சயமாக அடையாளம் காண முடியவில்லை'}</div>
                <span class="conf-chip chip-amber">{conf*100:.0f}% — Below threshold</span>
              </div>
            </div>
            <div class="disc-box">
              ℹ️ {'Please provide a clearer close-up photograph. Consult a botanical expert or KVK.' if _en(lang) else 'தெளிவான நெருக்கமான புகைப்படம் வழங்கவும். KVK நிபுணரை அணுகவும்.'}
            </div>
            </div>
            """, unsafe_allow_html=True)
        return

    if mode == "disease":
        st.markdown(f"<div class='section-wrap'><p class='section-title'>{'Disease Detection Result' if _en(lang) else 'நோய் கண்டறிதல் முடிவு'}</p></div>", unsafe_allow_html=True)
        if st_v == "confident_diagnosis":
            did      = ev.get("disease_id","")
            conf     = ev.get("confidence", 0.0)
            healthy  = ev.get("is_healthy", False)
            di       = diseases_db.get(did, {})
            dname    = di.get("name",{}).get(lang, di.get("name",{}).get("en", did))
            pathogen = di.get("pathogen","")
            if healthy:
                st.markdown(f"""
                <div style="padding:0 .75rem">
                <div class="res-banner res-healthy">
                  <div class="res-icon">✅</div>
                  <div>
                    <div class="res-label green-label">{'Plant Healthy' if _en(lang) else 'தாவரம் ஆரோக்கியமாக உள்ளது'}</div>
                    <div class="res-name">{dname or ('Healthy' if _en(lang) else 'ஆரோக்கியமானது')}</div>
                    <span class="conf-chip chip-green">Confidence: {conf*100:.0f}%</span>
                  </div>
                </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="padding:0 .75rem">
                <div class="res-banner res-disease">
                  <div class="res-icon">🔴</div>
                  <div>
                    <div class="res-label red-label">{'Disease Detected' if _en(lang) else 'நோய் கண்டறியப்பட்டது'}</div>
                    <div class="res-name">{dname}</div>
                    <div class="res-sci">{pathogen}</div>
                    <span class="conf-chip chip-red">Confidence: {conf*100:.0f}%</span>
                  </div>
                </div>
                </div>
                """, unsafe_allow_html=True)
                if di:
                    _disease_block(di, lang)
                _download_block(result, pid, did, lang)

        elif st_v == "low_confidence":
            conf = ev.get("confidence",0.0)
            st.markdown(f"""
            <div style="padding:0 .75rem">
            <div class="res-banner res-uncertain">
              <div class="res-icon">⚠️</div>
              <div>
                <div class="res-label amber-label">{'Low Confidence' if _en(lang) else 'குறைந்த நம்பகத்தன்மை'}</div>
                <div class="res-name">{'Please consult your agriculture officer or KVK' if _en(lang) else 'விவசாய அதிகாரியை அணுகவும்'}</div>
                <span class="conf-chip chip-amber">{conf*100:.0f}%</span>
              </div>
            </div>
            <div class="disc-box">
              ℹ️ {'Confidence is below 100%. Please also consult an agriculture officer or KVK for expert advice.' if _en(lang)
                  else 'நம்பகத்தன்மை குறைவாக உள்ளது. நிபுணர் ஆலோசனைக்கு KVK அணுகவும்.'}
            </div>
            </div>
            """, unsafe_allow_html=True)
        elif st_v == "crop_mismatch":
            st.warning(ev.get("message","Crop mismatch."))
        else:
            st.error(ev.get("message","Error."))


def _plant_info_block(pi: Dict, lang: str):
    name  = pi.get("common_name",{}).get(lang, pi.get("common_name",{}).get("en",""))
    sci   = pi.get("scientific_name","")
    cat   = pi.get("category","")
    desc  = pi.get("description",{}).get(lang, pi.get("description",{}).get("en",""))
    gc    = pi.get("growing_conditions",{})
    sup   = pi.get("support_status","info_only")

    if sup == "both_models":
        pills = _pill("Identification ✓","pill-green") + _pill("Disease ✓","pill-green")
    elif sup == "disease_model":
        pills = _pill("Disease ✓","pill-yellow")
    else:
        pills = _pill("Information Only","pill-blue")

    st.markdown(f"""
    <div style="padding:0 .75rem">
    <div class="ucard">
      <div class="ucard-title">{'Plant Identification Result' if False else ''}</div>
      <div class="info-row"><span class="ir-label">Plant Category</span><span class="ir-val">{cat}</span></div>
      <div class="info-row"><span class="ir-label">Model Support</span><span class="ir-val">{pills}</span></div>
    </div>
    <div class="ucard">
      <div class="ucard-title">{'About this plant' if lang=='en' else 'இந்த தாவரத்தைப் பற்றி'}</div>
      <p style="font-size:.84rem;color:var(--t2);line-height:1.55;margin:.35rem 0">{desc}</p>
      <div class="info-row"><span class="ir-label">☀️ Sunlight</span><span class="ir-val">{gc.get('sunlight','—')}</span></div>
      <div class="info-row"><span class="ir-label">💧 Watering</span><span class="ir-val">{gc.get('watering','—')}</span></div>
      <div class="info-row"><span class="ir-label">🌱 Soil</span><span class="ir-val">{gc.get('soil','—')}</span></div>
      <div class="info-row"><span class="ir-label">🌡️ Temp</span><span class="ir-val">{gc.get('temperature_c','—')}</span></div>
    </div>
    </div>
    """, unsafe_allow_html=True)


def _disease_block(di: Dict, lang: str):
    syms  = di.get("symptoms",{}).get(lang, di.get("symptoms",{}).get("en",[]))
    prev  = di.get("prevention",{}).get(lang, di.get("prevention",{}).get("en",[]))
    treat = di.get("treatment",{}).get(lang, di.get("treatment",{}).get("en",[]))

    def _lst(items): return "".join(f"<li>{i}</li>" for i in items)

    st.markdown("<div style='padding:0 .75rem'>", unsafe_allow_html=True)
    if syms:
        with st.expander("🩺  Symptoms" if _en(lang) else "🩺  அறிகுறிகள்", expanded=True):
            st.markdown(f'<ul class="blist">{_lst(syms)}</ul>', unsafe_allow_html=True)
    if prev:
        with st.expander("🛡️  Recommended Action" if _en(lang) else "🛡️  பரிந்துரைக்கப்பட்ட நடவடிக்கை"):
            st.markdown(f'<ul class="blist">{_lst(prev)}</ul>', unsafe_allow_html=True)
    if treat:
        with st.expander("💊  Treatment Guidance" if _en(lang) else "💊  சிகிச்சை வழிகாட்டுதல்"):
            st.markdown(f'<ul class="blist">{_lst(treat)}</ul>', unsafe_allow_html=True)
    with st.expander("👨‍⚕️  When to Consult Expert" if _en(lang) else "👨‍⚕️  நிபுணரை எப்போது அணுக"):
        st.markdown("""
        - Disease spreads despite treatment
        - More than 30% of crop affected
        - Contact local KVK or Block Agricultural Officer
        """ if _en(lang) else """
        - சிகிச்சையின் பின்னும் நோய் பரவினால்
        - 30%க்கும் அதிகமான பயிர் பாதிக்கப்பட்டால்
        - உள்ளூர் KVK அல்லது வட்டார விவசாய அலுவலரை அணுகவும்
        """)
    st.markdown("</div>", unsafe_allow_html=True)


def _download_block(result: Dict, pid, did, lang):
    pi = plants_db.get(pid) if pid else None
    di = diseases_db.get(did) if did else None
    ev = result.get("eval",{}) or {}
    sr = {
        "scan_uuid":     result.get("scan_uuid","N/A"),
        "timestamp":     datetime.now().strftime("%Y-%m-%d %H:%M"),
        "scan_type":     result.get("mode","unknown"),
        "selected_plant":pid,
        "predicted_class":ev.get("predicted_class"),
        "confidence":    ev.get("confidence"),
        "is_uncertain":  ev.get("status")=="low_confidence",
    }
    txt = report.generate_text_report(sr, pi, di)
    st.markdown("<div style='padding:0 .75rem;margin-top:.5rem'>", unsafe_allow_html=True)
    st.download_button(
        "⬇️  View Detailed Advice / Download Report" if _en(lang) else "⬇️  விரிவான ஆலோசனை / அறிக்கை பதிவிறக்கம்",
        data=txt, file_name=f"scan_{sr['scan_uuid']}.txt", mime="text/plain",
        key=f"dl_{result.get('scan_uuid','x')}"
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 4 — WEATHER ALERTS
# ══════════════════════════════════════════════════════════════════════════════
def screen_weather():
    lang = st.session_state.lang
    _page_header("Weather Alerts" if _en(lang) else "வானிலை எச்சரிக்கைகள்")

    st.markdown(f"<div class='section-wrap'><p class='section-sub'>{'Get live data from Open-Meteo. 5-day forecast and crop risk alerts.' if _en(lang) else 'Open-Meteo இலிருந்து நேரடி தரவு. 5 நாள் முன்னறிவிப்பு மற்றும் பயிர் இடர் எச்சரிக்கைகள்.'}</p></div>", unsafe_allow_html=True)

    # Search form
    with st.form("wx_form"):
        col_p, col_s = st.columns([5, 1])
        with col_p:
            place = st.text_input("", placeholder="Coimbatore, Tamil Nadu" if _en(lang) else "ஊரின் பெயர் உள்ளிடவும்",
                                   key="wx_place", label_visibility="collapsed")
        with col_s:
            submitted = st.form_submit_button("🔍" if _en(lang) else "தேடு")
        col_la, col_lo = st.columns(2)
        with col_la:
            lat_s = st.text_input("Lat (optional)" if _en(lang) else "அட்சரேகை", key="wx_lat", label_visibility="visible")
        with col_lo:
            lon_s = st.text_input("Long (optional)" if _en(lang) else "தீர்க்கரேகை", key="wx_lon", label_visibility="visible")
        st.form_submit_button("🌍  Refresh Weather" if _en(lang) else "🌍  வானிலை புதுப்பி",
                               use_container_width=True)

    if submitted or (lat_s and lon_s):
        with st.spinner("Fetching weather data…" if _en(lang) else "வானிலை தரவு பெறுகிறது…"):
            try:
                if lat_s.strip() and lon_s.strip():
                    lat, lon = float(lat_s), float(lon_s)
                    ok, err = weather.validate_coordinates(lat, lon)
                    if not ok: st.error(err); return
                    loc_name = f"{lat:.4f}°N, {lon:.4f}°E"
                elif place.strip():
                    geo = weather.geocode_place_name(place.strip())
                    lat, lon = geo["latitude"], geo["longitude"]
                    loc_name = f"{geo.get('name','')}, {geo.get('admin1','')}"
                else:
                    st.warning("Please enter a place name or coordinates." if _en(lang)
                               else "இடப்பெயர் அல்லது ஆயத்தொலைவுகளை உள்ளிடவும்.")
                    return
                fc = weather.fetch_weather_forecast(lat, lon)
                st.session_state.weather_data   = fc
                st.session_state.weather_loc    = loc_name
                st.session_state.weather_coords = (lat, lon)
                st.rerun()
            except weather.WeatherServiceError as e:
                st.error(f"⚠️ {e}")
            except Exception as e:
                st.error(f"Error: {e}")

    wdata = st.session_state.weather_data
    if not wdata:
        return

    loc_name = st.session_state.weather_loc or ""
    now_str  = datetime.now().strftime("%d %b %Y, %H:%M")
    tz       = wdata.get("timezone","—")

    st.markdown(f"""
    <div style="padding:0 .75rem">
    <div class="ucard" style="margin-bottom:.65rem">
      <p style="font-size:.82rem;color:var(--t2);margin:0">
        📍 <strong>{loc_name}</strong><br>
        <span style="color:var(--t3);font-size:.75rem">
          📡 {'Live data from Open-Meteo' if _en(lang) else 'Open-Meteo இலிருந்து நேரடி தரவு'} &nbsp;|&nbsp;
          🕐 Last updated: {now_str} &nbsp;|&nbsp;
          🌐 Timezone: {tz} &nbsp;|&nbsp;
          📅 Forecast: 5 days
        </span>
      </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # 5-day forecast
    daily   = wdata.get("daily", {})
    times   = daily.get("time", [])
    t_max   = daily.get("temperature_2m_max", [])
    t_min   = daily.get("temperature_2m_min", [])
    r_sum   = daily.get("precipitation_sum", [])
    r_prob  = daily.get("precipitation_probability_max", [])
    hourly  = wdata.get("hourly", {})

    st.markdown(f"<div style='padding:0 .75rem'><p class='section-title'>{'5-Day Forecast' if _en(lang) else '5 நாள் முன்னறிவிப்பு'}</p></div>", unsafe_allow_html=True)
    cols = st.columns(min(5, len(times)))
    for i, col in enumerate(cols):
        if i >= len(times): break
        try:
            dt      = datetime.strptime(times[i], "%Y-%m-%d")
            day_nm  = dt.strftime("%a")
            day_dt  = dt.strftime("%d %b")
        except Exception:
            day_nm = times[i]; day_dt = ""
        tx  = t_max[i]  if i < len(t_max)  else None
        tn  = t_min[i]  if i < len(t_min)  else None
        rs  = r_sum[i]  if i < len(r_sum)  else None
        rp  = r_prob[i] if i < len(r_prob) else None
        ico = _wicon(tx, rp)
        tmp = f"{tx:.0f}°/{tn:.0f}°" if tx and tn else "—"
        with col:
            st.markdown(f"""
            <div class="wday">
              <div class="wd-day">{day_nm}</div>
              <div class="wd-date">{day_dt}</div>
              <div class="wd-icon">{ico}</div>
              <div class="wd-temp">{tmp}</div>
              <div class="wd-rain">💧 {f"{rs:.0f}mm" if rs is not None else "—"} &nbsp; {f"{rp:.0f}%" if rp is not None else ""}</div>
            </div>
            """, unsafe_allow_html=True)

    # Agricultural alerts
    try:
        alerts = weather.generate_agricultural_weather_alerts(wdata)
        if alerts:
            st.markdown(f"<div style='padding:.7rem .75rem 0'><p class='section-title'>⚠️ {'Weather Alerts' if _en(lang) else 'வானிலை எச்சரிக்கைகள்'}</p></div>", unsafe_allow_html=True)
            seen = set()
            for al in alerts:
                rid = al.get("rule_id","")
                if rid in seen: continue
                seen.add(rid)
                sev = al.get("severity","caution")
                cls = {"warning":"fungal","danger":"heat","caution":"spray"}.get(sev,"ok")
                ico = {"warning":"🟡","danger":"🔴","caution":"🔵"}.get(sev,"✅")
                desc_o  = al.get("description",{})
                desc_t  = desc_o.get(lang, desc_o.get("en","")) if isinstance(desc_o,dict) else str(desc_o)
                adv_o   = al.get("action_advice",{})
                adv_t   = adv_o.get(lang, adv_o.get("en","")) if isinstance(adv_o,dict) else ""
                head    = rid.replace("_"," ").title()
                date_l  = al.get("date","")
                st.markdown(f"""
                <div style="padding:0 .75rem">
                <div class="walert {cls}">
                  <span style="font-size:1.3rem">{ico}</span>
                  <div>
                    <div class="wa-head">{head} <span style="font-size:.7rem;color:var(--t3)">{date_l}</span></div>
                    <div class="wa-text">{desc_t}</div>
                    {'<div class="wa-text" style="margin-top:.25rem"><strong>Recommendation:</strong> ' + adv_t + '</div>' if adv_t else ''}
                  </div>
                </div>
                </div>
                """, unsafe_allow_html=True)
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 5 — PLANT DATABASE
# ══════════════════════════════════════════════════════════════════════════════
def screen_database():
    lang = st.session_state.lang
    _page_header("Plant Database" if _en(lang) else "தாவர தரவுத்தளம்")
    st.markdown(f"<div class='section-wrap'><p class='section-sub'>{'Explore detailed information about various plants.' if _en(lang) else 'பல்வேறு தாவரங்களைப் பற்றிய விரிவான தகவல்கள்.'}</p></div>", unsafe_allow_html=True)

    with st.container():
        search = st.text_input("🔍  Search plants…" if _en(lang) else "🔍  தாவரங்களை தேடுங்கள்…", key="db_search")
        c1, c2 = st.columns(2)
        cats   = ["All Categories"] + sorted(set(p.get("category","") for p in plants_db.values()))
        stats  = ["All Status","Disease Model Supported","Information Only"]
        with c1:
            sel_cat  = st.selectbox("Category" if _en(lang) else "வகை", cats,  key="db_cat")
        with c2:
            sel_stat = st.selectbox("Status" if _en(lang) else "நிலை",   stats, key="db_stat")

    for pid, plant in plants_db.items():
        n_en = plant.get("common_name",{}).get("en","")
        n_ta = plant.get("common_name",{}).get("ta","")
        sci  = plant.get("scientific_name","")
        cat  = plant.get("category","")
        sup  = plant.get("support_status","info_only")

        if search and search.lower() not in (n_en+n_ta+sci+cat).lower():
            continue
        if sel_cat != "All Categories" and cat != sel_cat:
            continue
        if sel_stat == "Disease Model Supported" and sup not in ("both_models","disease_model"):
            continue
        if sel_stat == "Information Only" and sup != "info_only":
            continue

        nm = plant.get("common_name",{}).get(lang, n_en)
        em = _plant_emoji(cat)

        if sup == "both_models":
            pills_html = _pill("Disease Model","pill-green") + _pill("Supported","pill-green")
        elif sup == "disease_model":
            pills_html = _pill("Disease Model","pill-yellow")
        else:
            pills_html = _pill("Information Only","pill-blue") + _pill("Verified","pill-gray")

        st.markdown(f"""
        <div style="padding:0 .75rem">
        <div class="pdb-card">
          <div class="pdb-thumb">{em}</div>
          <div style="flex:1">
            <div class="pdb-name">{nm}</div>
            <div class="pdb-sci">{sci}</div>
            <div class="pdb-cat">{cat}</div>
            <div style="margin-top:.2rem">{pills_html}</div>
          </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"📋 View" if _en(lang) else "📋 பார்க்க", key=f"db_v_{pid}"):
            go("care", care_plant=pid, care_disease=None)


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 6 — PLANT CARE & ADVICE
# ══════════════════════════════════════════════════════════════════════════════
def screen_care():
    lang = st.session_state.lang
    _page_header("Plant Care & Advice" if _en(lang) else "தாவர பராமரிப்பு & ஆலோசனை")

    keys   = list(plants_db.keys())
    labels = [plants_db[k]["common_name"].get(lang, plants_db[k]["common_name"].get("en",k)) for k in keys]
    lmap   = dict(zip(labels, keys))

    def_idx = 0
    if st.session_state.care_plant and st.session_state.care_plant in keys:
        def_idx = keys.index(st.session_state.care_plant)

    col_p, col_d = st.columns(2)
    with col_p:
        sel_pl = st.selectbox("Plant" if _en(lang) else "தாவரம்", labels, index=def_idx, key="cp_sel")
    sel_pid = lmap.get(sel_pl)
    pi = plants_db.get(sel_pid, {})

    # Disease selector
    known   = pi.get("known_diseases", [])
    d_opts  = ["Select condition…" if _en(lang) else "நிலை தேர்வு…"]
    d_map   = {}
    for did in known:
        di = diseases_db.get(did, {})
        dl = di.get("name",{}).get(lang, di.get("name",{}).get("en",did))
        d_opts.append(dl); d_map[dl] = did

    with col_d:
        sel_dc = st.selectbox("Condition" if _en(lang) else "நிலை", d_opts, key="cd_sel")
    sel_did = d_map.get(sel_dc)
    di = diseases_db.get(sel_did) if sel_did else None

    # Show plant thumb info
    if pi:
        name_disp = pi.get("common_name",{}).get(lang, pi.get("common_name",{}).get("en",""))
        sci_disp  = pi.get("scientific_name","")
        st.markdown(f"""
        <div style="padding:0 .75rem">
        <div class="ucard" style="display:flex;gap:.8rem;align-items:center">
          <div style="font-size:2rem">{_plant_emoji(pi.get('category',''))}</div>
          <div>
            <div class="ucard-title">{name_disp}</div>
            <div style="font-size:.8rem;color:var(--t3);font-style:italic">{sci_disp}</div>
          </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    def _lst(items): return "".join(f"<li>{i}</li>" for i in items)

    st.markdown("<div style='padding:0 .75rem'>", unsafe_allow_html=True)

    if pi:
        with st.expander("🌿  About the Plant" if _en(lang) else "🌿  தாவரத்தைப் பற்றி", expanded=True):
            desc = pi.get("description",{}).get(lang, pi.get("description",{}).get("en",""))
            gc   = pi.get("growing_conditions",{})
            st.markdown(f"<p style='font-size:.85rem;color:var(--t2);line-height:1.55;margin-bottom:.7rem'>{desc}</p>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("☀️ Sun",   gc.get("sunlight","—")[:14])
            c2.metric("💧 Water", gc.get("watering","—")[:14])
            c3.metric("🌱 Soil",  gc.get("soil","—")[:14])
            c4.metric("🌡️ Temp",  gc.get("temperature_c","—"))

    if di:
        syms  = di.get("symptoms",{}).get(lang, di.get("symptoms",{}).get("en",[]))
        prev  = di.get("prevention",{}).get(lang, di.get("prevention",{}).get("en",[]))
        treat = di.get("treatment",{}).get(lang, di.get("treatment",{}).get("en",[]))
        cdesc = di.get("description",{}).get(lang, di.get("description",{}).get("en",""))

        if syms:
            with st.expander("🩺  Symptoms" if _en(lang) else "🩺  அறிகுறிகள்"):
                st.markdown(f'<ul class="blist">{_lst(syms)}</ul>', unsafe_allow_html=True)
        if prev:
            with st.expander("🛡️  Prevention Methods" if _en(lang) else "🛡️  தடுப்பு முறைகள்"):
                st.markdown(f'<ul class="blist">{_lst(prev)}</ul>', unsafe_allow_html=True)
        with st.expander("🌾  Cultural Management" if _en(lang) else "🌾  பண்பாட்டு மேலாண்மை"):
            st.markdown("- Rotate crops to reduce soilborne pathogen buildup\n- Remove and destroy infected plant material\n- Use certified disease-free seeds\n- Maintain proper plant spacing for air circulation" if _en(lang)
                        else "- மண்ணில் உள்ள நோயெதிர்ப்பு கிருமிகளை குறைக்க பயிர் சுழற்சி செய்யவும்\n- பாதிக்கப்பட்ட தாவர பொருட்களை அகற்றி அழிக்கவும்\n- நோய் இல்லாத சான்றிதழ் பெற்ற விதைகளை பயன்படுத்தவும்")
        with st.expander("🔍  Monitoring Tips" if _en(lang) else "🔍  கண்காணிப்பு குறிப்புகள்"):
            st.markdown("- Inspect crops twice weekly for early symptoms\n- Monitor weather for high humidity (>80%) and rain\n- Keep records of disease occurrence dates\n- Report unusual outbreaks to local KVK" if _en(lang)
                        else "- வாரத்தில் இரண்டு முறை பயிர்களை சோதிக்கவும்\n- அதிக ஈரப்பதம் (>80%) மற்றும் மழைக்காக வானிலையை கண்காணிக்கவும்\n- நோய் ஏற்படும் தேதிகளை பதிவு வைக்கவும்")
        if treat:
            with st.expander("💊  Treatment Guidance" if _en(lang) else "💊  சிகிச்சை வழிகாட்டுதல்"):
                st.markdown(f'<ul class="blist">{_lst(treat)}</ul>', unsafe_allow_html=True)

    pests = pi.get("common_pests",[]) if pi else []
    if pests:
        with st.expander("🐛  Common Pests" if _en(lang) else "🐛  பொதுவான பூச்சிகள்"):
            st.markdown(f'<ul class="blist">{"".join(f"<li>{p}</li>" for p in pests)}</ul>', unsafe_allow_html=True)

    with st.expander("👨‍⚕️  When to Consult Expert" if _en(lang) else "👨‍⚕️  நிபுணரை எப்போது அணுக"):
        st.markdown("- Disease spreads rapidly despite preventive measures\n- More than 30% of the crop is affected\n- Unusual or unidentified symptoms appear\n- Before purchasing any pesticide or fungicide\n- Contact local KVK (Krishi Vigyan Kendra) or Block Agricultural Officer" if _en(lang)
                    else "- தடுப்பு நடவடிக்கைகளுக்கு பிறகும் நோய் வேகமாக பரவினால்\n- 30%க்கும் அதிகமான பயிர் பாதிக்கப்பட்டால்\n- அசாதாரண அறிகுறிகள் தோன்றினால்\n- எந்தவொரு பூச்சிக்கொல்லி வாங்குவதற்கு முன்பும்")

    refs = pi.get("references",[]) if pi else []
    if refs:
        with st.expander("📚  References" if _en(lang) else "📚  குறிப்புகள்"):
            for r in refs:
                st.markdown(f"- {r}")

    st.markdown(f"""
    <div class="disc-box">
      ℹ️ {'This information is general guidance. Please consult your local agriculture officer or KVK for expert advice.' if _en(lang)
           else 'இந்த தகவல் பொதுவான வழிகாட்டுதல். நிபுணர் ஆலோசனைக்கு உங்கள் உள்ளூர் விவசாய அலுவலகத்தை அணுகவும்.'}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 7 — GOVERNMENT SCHEMES
# ══════════════════════════════════════════════════════════════════════════════
def screen_schemes():
    lang = st.session_state.lang
    _page_header("Government Schemes" if _en(lang) else "அரசு திட்டங்கள்")
    st.markdown(f"<div class='section-wrap'><p class='section-sub'>{'Explore agricultural schemes and official application links.' if _en(lang) else 'வேளாண் திட்டங்கள் மற்றும் அதிகாரப்பூர்வ விண்ணப்ப இணைப்புகள்.'}</p></div>", unsafe_allow_html=True)

    sl = schemes_db if isinstance(schemes_db, list) else list(schemes_db.values())
    for sc in sl:
        name  = sc.get("name",{}).get(lang, sc.get("name",{}).get("en","—"))
        summ  = sc.get("summary",{})
        summ  = summ.get(lang, summ.get("en","")) if isinstance(summ,dict) else str(summ)

        ben_o = sc.get("benefits",{})
        ben_r = ben_o.get(lang, ben_o.get("en",[])) if isinstance(ben_o,dict) else ben_o
        ben   = "; ".join(str(b) for b in ben_r[:2]) if isinstance(ben_r,list) else str(ben_r)

        el_o  = sc.get("eligibility",{})
        el_r  = el_o.get(lang, el_o.get("en",[])) if isinstance(el_o,dict) else el_o
        el    = el_r[0] if isinstance(el_r,list) and el_r else str(el_r)

        ap_o  = sc.get("application_procedure", sc.get("how_to_apply",{}))
        ap    = ap_o.get(lang, ap_o.get("en","")) if isinstance(ap_o,dict) else str(ap_o)
        if len(ap) > 160: ap = ap[:160] + "…"

        portal = sc.get("official_url", sc.get("official_portal_url",""))
        badge  = sc.get("scheme_type","Central Government")

        st.markdown(f"""
        <div style="padding:0 .75rem">
        <div class="sc-card">
          <div class="sc-title">{name}</div>
          <span class="sc-badge">{badge}</span>
          <p style="font-size:.84rem;color:var(--t2);margin-bottom:.55rem">{summ}</p>
          <div class="sc-row"><span class="sc-lbl">{'Benefits' if _en(lang) else 'நன்மைகள்'}:</span><span class="sc-val">{ben}</span></div>
          <div class="sc-row"><span class="sc-lbl">{'Eligibility' if _en(lang) else 'தகுதி'}:</span><span class="sc-val">{el}</span></div>
          <div class="sc-row"><span class="sc-lbl">{'How to apply' if _en(lang) else 'விண்ணப்பிக்க'}:</span><span class="sc-val">{ap}</span></div>
          {f'<div class="sc-link"><a href="{portal}" target="_blank">🔗 Visit Official Website ↗</a></div>' if portal else ''}
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:0 .75rem">
    <div class="disc-box">
      ⚠️ {'Verify all details at the official website. Government rules may change over time.' if _en(lang)
           else 'அதிகாரப்பூர்வ இணையதளத்தில் அனைத்து விவரங்களையும் சரிபார்க்கவும். அரசு விதிகள் மாறலாம்.'}
    </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 8 — SCAN HISTORY
# ══════════════════════════════════════════════════════════════════════════════
def screen_history():
    lang = st.session_state.lang
    _page_header("Scan History" if _en(lang) else "ஸ்கேன் வரலாறு")

    col_t, col_c = st.columns([4,1])
    with col_t:
        st.markdown(f"<div style='padding:0 .75rem'><p class='section-sub'>{'Previous plant scans and disease detection results.' if _en(lang) else 'முந்தைய தாவர ஸ்கேன் மற்றும் நோய் கண்டறிதல் முடிவுகள்.'}</p></div>", unsafe_allow_html=True)
    with col_c:
        if st.button("Clear All" if _en(lang) else "அனைத்தும் நீக்கு", key="hist_clear"):
            scan_history.clear_all_scans()
            st.success("Cleared." if _en(lang) else "நீக்கப்பட்டது.")
            st.rerun()

    records = scan_history.get_all_scans(limit=30)
    if not records:
        st.markdown(f"""
        <div style="padding:0 .75rem">
        <div class="disc-box">
          ℹ️ {'No scan history yet. Use Scan to analyse plants.' if _en(lang) else 'ஸ்கேன் வரலாறு இல்லை. தாவரங்களை பகுப்பாய்வு செய்ய Scan பயன்படுத்தவும்.'}
        </div>
        </div>
        """, unsafe_allow_html=True)
        return

    for rec in records:
        plant   = (rec.get("selected_plant") or "Unknown").replace("_"," ").title()
        pred    = (rec.get("predicted_class") or "—").replace("_"," ")
        conf    = rec.get("confidence")
        conf_s  = f"{conf*100:.0f}%" if conf is not None else "—"
        ts      = rec.get("timestamp","")
        unc     = bool(rec.get("is_uncertain",0))
        sid     = rec.get("id")
        scan_id = rec.get("scan_uuid","")
        healthy = "healthy" in pred.lower()
        dot_cls = "hd-healthy" if healthy else ("hd-info" if unc else "hd-disease")
        icon    = "✅" if healthy else ("⚠️" if unc else "🔴")

        col_i, col_dl, col_rm = st.columns([5,1,1])
        with col_i:
            st.markdown(f"""
            <div style="padding:0 .75rem">
            <div class="hist-item">
              <div class="hist-dot {dot_cls}">{icon}</div>
              <div>
                <div class="hist-plant">{plant} — {pred}</div>
                <div class="hist-conf">{'Confidence' if _en(lang) else 'நம்பகத்தன்மை'}: {conf_s}</div>
                <div class="hist-ts">🕐 {ts}</div>
              </div>
            </div>
            </div>
            """, unsafe_allow_html=True)
        with col_dl:
            pi_d  = plants_db.get(rec.get("selected_plant",""))
            sr_d  = {
                "scan_uuid":rec.get("scan_uuid","N/A"),
                "timestamp":ts,"scan_type":rec.get("scan_type","unknown"),
                "selected_plant":plant,"predicted_class":pred,
                "confidence":conf,"is_uncertain":unc,
            }
            txt = report.generate_text_report(sr_d, pi_d)
            st.download_button("⬇️", data=txt, file_name=f"rpt_{scan_id}.txt",
                               mime="text/plain", key=f"dl_{sid}")
        with col_rm:
            if st.button("🗑️", key=f"rm_{sid}"):
                scan_history.delete_scan(sid)
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 9 — MORE (About)
# ══════════════════════════════════════════════════════════════════════════════
def screen_more():
    lang = st.session_state.lang
    _page_header("More" if _en(lang) else "மேலும்")

    st.markdown("""
    <div style="padding:0 .75rem">
    <div class="ucard">
      <div class="ucard-title">🌿 AI Plant Doctor v3.0</div>
      <p style="font-size:.84rem;color:var(--t2);margin:.3rem 0">Smart Plant Identification, Disease Detection & Farming Early Warning System</p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding:0 .75rem'>", unsafe_allow_html=True)
    with st.expander("⚙️  Technology Stack"):
        st.markdown("""
        - **Streamlit** — Web framework
        - **TensorFlow/Keras** — AI model inference (when installed)
        - **Open-Meteo API** — Real-time weather (free, no key required)
        - **TNAU Knowledge Base** — Plant & disease data
        - **SQLite** — Local scan history
        - **MobileNetV2** — Transfer learning backbone
        """)
    with st.expander("🧠  Train the AI Model"):
        st.code("python train_model.py --data_dir /path/to/PlantVillage", language="bash")
        st.markdown("Download PlantVillage dataset from Kaggle, place in a folder, and run the command above.")
    with st.expander("📞  Expert Resources"):
        st.markdown("""
        - **TNAU Agritech Portal**: agritech.tnau.ac.in
        - **ICAR**: icar.org.in
        - **PM-KISAN**: pmkisan.gov.in
        - **PMFBY**: pmfby.gov.in
        - **Soil Health Card**: soilhealth.dac.gov.in
        """)
    with st.expander("⚠️  Disclaimer"):
        st.markdown("""
        1. This system provides decision support only — not a scientific diagnosis.
        2. Always consult a certified agricultural officer before applying treatments.
        3. Never mix or spray pesticides without reading official product labels.
        4. Verify government scheme details at official portals.
        """)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER BAR
# ══════════════════════════════════════════════════════════════════════════════
def _footer():
    st.markdown("""
    <div class="footer-bar">
      <div class="fb-item"><span class="fb-icon">🤖</span> AI Powered</div>
      <div class="fb-item"><span class="fb-icon">🌦️</span> Live Weather (Open-Meteo)</div>
      <div class="fb-item"><span class="fb-icon">🌿</span> Extensive Plant Database</div>
      <div class="fb-item"><span class="fb-icon">✅</span> Safe & Reliable Advice</div>
      <div class="fb-item"><span class="fb-icon">🏛️</span> Official Schemes</div>
      <div class="fb-item"><span class="fb-icon">📱</span> Mobile Friendly</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def main():
    page = st.session_state.page

    if page == "home":
        screen_home()
    elif page == "scan":
        screen_scan()
        if st.session_state.last_result:
            pass  # already rendered inside screen_scan
    elif page == "weather":
        screen_weather()
    elif page == "database":
        screen_database()
    elif page == "care":
        screen_care()
    elif page == "schemes":
        screen_schemes()
    elif page == "history":
        screen_history()
    elif page == "more":
        screen_more()
    else:
        screen_home()

    _footer()
    st.markdown("---")
    _bottom_nav()


if __name__ == "__main__":
    main()
