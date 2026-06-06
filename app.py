import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import datetime
import traceback
import glob
import base64

# ==============================
# CONFIGURATION DE LA PAGE
# ==============================
st.set_page_config(
    page_title="PowerGuard AI | DGA Expert System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# PREPARATION DU LOGO LOCAL
# ==============================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    except Exception:
        # صورة درع احتياطية في حال لم يتم العثور على شعارك
        return "https://cdn-icons-png.flaticon.com/512/2092/2092663.png"

base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, "logo.png") # تأكد أن اسم اللوغو الجديد هو logo.png
LOGO_SRC = get_base64_image(logo_path)

# ==============================
# CSS LIGHT THEME – POWERGUARD AI BRANDING
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* ========== FOND AVEC IMAGE ET OVERLAY CLAIR ========== */
.stApp {
    background: linear-gradient(135deg, rgba(240, 244, 250, 0.92) 0%, rgba(226, 232, 240, 0.95) 100%), 
                url('https://images.unsplash.com/photo-1581092334651-ddf26d9a09d0?auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed !important;
    background-size: cover !important;
    color: #0F172A;
}

/* ========== SIDEBAR CLAIRE AVEC OMBRE ========== */
section[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(15, 44, 89, 0.1);
    box-shadow: 4px 0 20px rgba(0,0,0,0.02);
}
.sidebar-header {
    text-align: center;
    padding: 1.8rem 0 1rem;
}
.sidebar-logo {
    width: 160px;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.15));
    transition: transform 0.3s ease;
}
.sidebar-logo:hover {
    transform: scale(1.05);
}
.sidebar-title {
    font-weight: 900;
    font-size: 1.2rem;
    color: #0F2C59;
    text-align: center;
    letter-spacing: 1px;
    margin-top: 15px;
}

/* ========== NOUVEAU DESIGN DU MENU (POWERGUARD TABS) ========== */
div.row-widget.stRadio > div {
    gap: 12px;
    display: flex;
    flex-direction: column;
    padding: 10px 0;
}
div.row-widget.stRadio > div > label {
    background-color: transparent;
    padding: 14px 20px;
    border-radius: 8px;
    border: 1px solid rgba(15, 44, 89, 0.05);
    border-left: 4px solid transparent;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    cursor: pointer;
    font-weight: 700;
    color: #475569 !important;
}
div.row-widget.stRadio > div > label:hover {
    background-color: #F8FAFC;
    transform: translateX(5px);
    color: #0F2C59 !important;
    border-left: 4px solid #00A8E8; /* Cyan Highlight */
}
div.row-widget.stRadio > div > label[data-checked="true"] {
    background-color: #0F2C59 !important;
    color: #FFFFFF !important;
    box-shadow: 0 8px 20px rgba(15, 44, 89, 0.25);
    border-color: #0F2C59;
    border-left: 4px solid #FF7A00; /* Lightning Orange Highlight */
    transform: scale(1.02);
}
div.row-widget.stRadio > div > label > div:first-child { display: none; } 

/* ========== CARTES STATISTIQUES (Sidebar) ========== */
.metric-card-side {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #E2E8F0;
    transition: all 0.25s ease;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
    margin-bottom: 10px;
}
.metric-value-side {
    font-size: 1.5rem;
    font-weight: 800;
    color: #FF7A00; /* Orange */
}

/* ========== TOP BAR ========== */
.top-bar {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 0.8rem 2rem;
    border-radius: 12px;
    margin: 1rem 1.5rem 2rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(255,255,255,0.8);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}
.logo-area {
    display: flex;
    align-items: center;
    gap: 12px;
}
.logo-text {
    font-weight: 900;
    font-size: 1.1rem;
    color: #0F2C59;
    letter-spacing: 1px;
}

/* ========== DGA CARD (GLASSMORPHISM) ========== */
.dga-card {
    background: rgba(255, 255, 255, 0.90);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 16px;
    padding: 2.5rem;
    margin: 0 1.5rem 2rem 1.5rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);
    transition: transform 0.3s ease;
}
.dga-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: #0F2C59;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
}

/* ========== ANIMATION INTERACTIVE DES GAZ ========== */
.sensors-container {
    display: flex;
    justify-content: space-around;
    align-items: flex-start;
    margin: 1.5rem 0 3rem 0;
    padding: 2rem 1rem;
    background: rgba(255,255,255,0.6);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.8);
    box-shadow: inset 0 4px 15px rgba(0,0,0,0.02);
}
.gas-orb-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 110px;
}
.gas-orb {
    position: relative;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: #FFFFFF;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    animation: floatOrb 4s ease-in-out infinite;
    margin-bottom: 15px;
}
.gas-orb-wrapper:nth-child(2) .gas-orb { animation-delay: 0.5s; }
.gas-orb-wrapper:nth-child(3) .gas-orb { animation-delay: 1s; }
.gas-orb-wrapper:nth-child(4) .gas-orb { animation-delay: 1.5s; }
.gas-orb-wrapper:nth-child(5) .gas-orb { animation-delay: 2s; }

.gas-ring {
    position: absolute;
    top: -6px; left: -6px; right: -6px; bottom: -6px;
    border-radius: 50%;
    border: 3px dashed;
    border-top-color: transparent !important;
    opacity: 0.8;
    animation: spinRing linear infinite;
}

.gas-name {
    font-size: 1.4rem;
    font-weight: 800;
}
.gas-val {
    font-size: 1.1rem;
    font-weight: 800;
    text-align: center;
}
.gas-status {
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 12px;
    border-radius: 20px;
    margin-top: 5px;
}

@keyframes spinRing { 100% { transform: rotate(360deg); } }
@keyframes floatOrb { 
    0%, 100% { transform: translateY(0); } 
    50% { transform: translateY(-8px); } 
}

/* ========== INPUTS MODERNES ========== */
.stNumberInput label {
    color: #1E293B !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
    border: 1px solid #CBD5E1 !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.01) !important;
    transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #0F2C59 !important;
    box-shadow: 0 0 0 3px rgba(15, 44, 89, 0.1) !important;
    transform: translateY(-2px);
}
input {
    color: #0F2C59 !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
}

/* ========== BOUTON 3D (PRÉDIRE) ========== */
.stButton > button {
    background: linear-gradient(180deg, #FF914D 0%, #FF7A00 100%) !important; /* Lightning Orange */
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    box-shadow: 0 6px 0 #CC6200, 0 10px 20px rgba(255, 122, 0, 0.2) !important;
    transition: all 0.1s ease !important;
    width: 100% !important;
    margin-top: 1.6rem !important;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.stButton > button:hover {
    transform: translateY(2px) !important;
    box-shadow: 0 4px 0 #CC6200, 0 6px 15px rgba(255, 122, 0, 0.2) !important;
    background: linear-gradient(180deg, #FFA770 0%, #FF914D 100%) !important;
}
.stButton > button:active {
    transform: translateY(6px) !important;
    box-shadow: 0 0 0 #CC6200, 0 2px 5px rgba(0,0,0,0.1) !important;
}

/* ========== CARTE RÉSULTAT ========== */
.result-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 2.5rem;
    text-align: center;
    border-left: 8px solid #FF7A00;
    box-shadow: 0 15px 35px rgba(0,0,0,0.06);
    margin-top: 1.5rem;
    animation: slideUp 0.5s ease-out;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.result-card.critical { border-left-color: #DC2626; }
.result-card.warning { border-left-color: #FF7A00; }
.result-card.normal { border-left-color: #10B981; }

.result-fault {
    font-size: 2.4rem;
    font-weight: 900;
    color: #0F2C59;
    margin: 10px 0;
}
.result-confidence {
    font-size: 1rem;
    font-weight: 700;
    color: #475569;
    background: #F8FAFC;
    padding: 8px 20px;
    border-radius: 50px;
    display: inline-block;
    border: 1px solid #E2E8F0;
}

/* ========== BARRES DE PROBABILITÉ ========== */
.prob-container {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    border: 1px solid #E2E8F0;
}
.prob-bar-container {
    background: #EDF2F7;
    border-radius: 30px;
    margin: 8px 0 16px 0;
    overflow: hidden;
    height: 28px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
}
.prob-fill {
    height: 100%;
    line-height: 28px;
    text-align: right;
    padding-right: 12px;
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    border-radius: 30px;
    transition: width 1s ease-in-out;
}

/* ========== TABLEAU HISTORIQUE (SCROLLABLE & UNLIMITED) ========== */
.table-wrapper {
    max-height: 450px;
    overflow-y: auto;
    border-radius: 10px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    background: #FFFFFF;
    margin: 0 1.5rem;
}
.custom-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}
.custom-table th {
    background-color: #0F2C59;
    color: #FFFFFF;
    padding: 16px 20px;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 0.5px;
    position: sticky;
    top: 0;
    z-index: 10;
}
.custom-table td {
    padding: 14px 20px;
    border-bottom: 1px solid #F1F5F9;
    color: #1E293B;
    font-size: 14px;
    font-weight: 500;
}
.custom-table tr:hover td { background-color: #F8FAFC; }
.custom-table tr:last-child td { border-bottom: none; }

/* CARTES DU DASHBOARD PRINCIPAL */
.metric-container {
    display: flex;
    gap: 20px;
    margin-bottom: 2rem;
    margin-left: 1.5rem;
    margin-right: 1.5rem;
}
.metric-card {
    background: #FFFFFF;
    padding: 24px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    flex: 1;
    box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    border-top: 4px solid #0F2C59;
    transition: transform 0.3s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-value { font-size: 2rem; font-weight: 800; color: #0F2C59; }
.metric-label { font-size: 0.85rem; color: #64748B; text-transform: uppercase; font-weight: 700; margin-top: 5px;}

/* Cacher éléments natifs Streamlit */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# FONCTIONS DE CHARGEMENT
# ==============================
MODELS_DIR = os.path.join(base_dir, "models_saved")
HISTORY_FILE = os.path.join(base_dir, "history.csv")

def get_available_models():
    if not os.path.exists(MODELS_DIR):
        return []
    all_pkl = glob.glob(os.path.join(MODELS_DIR, "*.pkl"))
    exclude_keywords = ['scaler', 'encoder', 'label']
    models = []
    for f in all_pkl:
        name = os.path.basename(f).lower()
        if not any(kw in name for kw in exclude_keywords):
            models.append(f)
    return models

@st.cache_resource(show_spinner=False)
def load_scaler_encoder():
    scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
    encoder_path = os.path.join(MODELS_DIR, "encoder.pkl")
    if not os.path.exists(scaler_path) or not os.path.exists(encoder_path):
        return None, None, False
    try:
        scaler = joblib.load(scaler_path)
        encoder = joblib.load(encoder_path)
        return scaler, encoder, True
    except:
        return None, None, False

@st.cache_resource(show_spinner=False)
def load_selected_model(model_path):
    try:
        model = joblib.load(model_path)
        return model, True
    except:
        return None, False

scaler, encoder, scaler_ok = load_scaler_encoder()
model_files = get_available_models()

def save_prediction(h2, ch4, c2h6, c2h4, c2h2, fault, conf):
    try:
        new_row = pd.DataFrame([{
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "H2": h2, "CH4": ch4, "C2H6": c2h6, "C2H4": c2h4, "C2H2": c2h2,
            "Diagnosis": fault,
            "Confidence_%": round(conf, 2)
        }])
        if os.path.exists(HISTORY_FILE):
            old = pd.read_csv(HISTORY_FILE)
            if list(old.columns) == list(new_row.columns):
                pd.concat([old, new_row], ignore_index=True).to_csv(HISTORY_FILE, index=False)
            else:
                new_row.to_csv(HISTORY_FILE, index=False)
        else:
            new_row.to_csv(HISTORY_FILE, index=False)
    except:
        pass

def get_stats():
    try:
        if os.path.exists(HISTORY_FILE):
            df = pd.read_csv(HISTORY_FILE)
            if len(df) > 0:
                last_row = df.iloc[-1]
                if isinstance(last_row, pd.Series) and 'Diagnosis' in last_row:
                    return len(df), last_row
            return 0, None
        return 0, None
    except:
        return 0, None

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        return True
    return False

# Fonction pour évaluer l'état d'un gaz
def evaluate_gas(gas_name, val):
    limits = {
        "H2": {"warn": 150, "crit": 1000},
        "CH4": {"warn": 120, "crit": 400},
        "C2H6": {"warn": 65, "crit": 150},
        "C2H4": {"warn": 50, "crit": 200},
        "C2H2": {"warn": 15, "crit": 50}
    }
    limit = limits.get(gas_name)
    if val >= limit["crit"]:
        return "#DC2626", "CRITIQUE", "rgba(220, 38, 38, 0.1)", "1s"
    elif val >= limit["warn"]:
        return "#FF7A00", "ATTENTION", "rgba(255, 122, 0, 0.1)", "2.5s"
    else:
        return "#10B981", "NORMAL", "rgba(16, 185, 129, 0.1)", "6s"

if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False
if "selected_model_path" not in st.session_state:
    default = None
    for f in model_files:
        if "fine_tree_real" in f:
            default = f
            break
    if default is None and len(model_files) > 0:
        default = model_files[0]
    st.session_state.selected_model_path = default

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-header">
        <img class="sidebar-logo" src="{LOGO_SRC}">
        <div class="sidebar-title">POWERGUARD AI</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:0.85rem; font-weight:800; color:#0F2C59; text-transform:uppercase; margin-bottom:5px;'>Navigation Principale</div>",
        unsafe_allow_html=True)
    menu = st.radio("", ["Analyse DGA", "Supervision & Données"], label_visibility="collapsed")

    st.markdown("<hr style='border-color: rgba(15, 44, 89, 0.1); margin: 20px 0;'>", unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:0.85rem; font-weight:800; color:#0F2C59; text-transform:uppercase; margin-bottom:5px;'>Sélection du Modèle</div>",
        unsafe_allow_html=True)

    if model_files:
        model_names = [os.path.basename(p) for p in model_files]
        current_name = os.path.basename(
            st.session_state.selected_model_path) if st.session_state.selected_model_path else model_names[0]
        selected_name = st.selectbox("", model_names,
                                     index=model_names.index(current_name) if current_name in model_names else 0,
                                     label_visibility="collapsed")
        new_path = os.path.join(MODELS_DIR, selected_name)
        if new_path != st.session_state.selected_model_path:
            st.session_state.selected_model_path = new_path
            st.cache_resource.clear()
            st.rerun()

    model, model_ok = load_selected_model(st.session_state.selected_model_path)
    total_analyses, last_diag = get_stats()

    st.markdown(
        "<br><div style='font-size:0.85rem; font-weight:800; color:#0F2C59; text-transform:uppercase; margin-bottom:10px;'>Aperçu Rapide</div>",
        unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"<div class='metric-card-side'><div class='metric-value-side'>{total_analyses}</div><div style='font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase;'>Analyses</div></div>",
            unsafe_allow_html=True)
    with col2:
        if last_diag is not None and isinstance(last_diag, pd.Series):
            diag_value = last_diag.get('Diagnosis', 'Inconnu')
            diag_text = str(diag_value)[:10]
            st.markdown(
                f"<div class='metric-card-side'><div style='font-size:1.1rem; font-weight:900; color:#0F2C59; padding:10px 0;'>{diag_text}</div><div style='font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase;'>Dernier</div></div>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='metric-card-side'><div style='font-size:0.8rem; color:#64748B; padding:15px 0;'>Vide</div></div>",
                unsafe_allow_html=True)

    st.markdown("---")

    if os.path.exists(HISTORY_FILE) and total_analyses > 0:
        if st.button("Purger l'Historique", use_container_width=True):
            st.session_state.confirm_clear = True

    if st.session_state.confirm_clear:
        st.warning("Confirmer la suppression ?")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("Oui"):
                if clear_history():
                    st.session_state.confirm_clear = False
                    st.rerun()
        with col_c2:
            if st.button("Non"):
                st.session_state.confirm_clear = False
                st.rerun()

# ==============================
# CONTENU PRINCIPAL
# ==============================
st.markdown(f"""
<div class="top-bar">
    <div class="logo-area">
        <img src="{LOGO_SRC}" width="35">
        <div class="logo-text">POWERGUARD AI · SYSTÈME EXPERT DGA</div>
    </div>
</div>
""", unsafe_allow_html=True)

if menu == "Analyse DGA":
    with st.container():
        st.markdown('<div class="dga-card">', unsafe_allow_html=True)
        st.markdown(
            "<h4 style='color: #0F2C59; font-weight: 800; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;'>Surveillance Dynamique des Gaz</h4>",
            unsafe_allow_html=True)

        # State management for animation
        if 'h2_val' not in st.session_state: st.session_state.h2_val = 100.0
        if 'ch4_val' not in st.session_state: st.session_state.ch4_val = 50.0
        if 'c2h6_val' not in st.session_state: st.session_state.c2h6_val = 20.0
        if 'c2h4_val' not in st.session_state: st.session_state.c2h4_val = 10.0
        if 'c2h2_val' not in st.session_state: st.session_state.c2h2_val = 5.0

        gases_data = [
            ("H₂", st.session_state.h2_val, evaluate_gas("H2", st.session_state.h2_val)),
            ("CH₄", st.session_state.ch4_val, evaluate_gas("CH4", st.session_state.ch4_val)),
            ("C₂H₆", st.session_state.c2h6_val, evaluate_gas("C2H6", st.session_state.c2h6_val)),
            ("C₂H₄", st.session_state.c2h4_val, evaluate_gas("C2H4", st.session_state.c2h4_val)),
            ("C₂H₂", st.session_state.c2h2_val, evaluate_gas("C2H2", st.session_state.c2h2_val))
        ]

        sensors_html = ""
        for name, val, (color, status, bg_color, speed) in gases_data:
            sensors_html += f'<div class="gas-orb-wrapper"><div class="gas-orb"><div class="gas-ring" style="border-color: {color}; animation-duration: {speed};"></div><div class="gas-name" style="color: {color};">{name}</div></div><div class="gas-val" style="color: {color};">{val}</div><div class="gas-status" style="background: {bg_color}; color: {color};">{status}</div></div>'

        st.markdown(f'<div class="sensors-container">{sensors_html}</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.h2_val = st.number_input("Hydrogène (H₂)", min_value=0.0, max_value=50000.0,
                                                      value=st.session_state.h2_val, step=10.0)
            st.session_state.ch4_val = st.number_input("Méthane (CH₄)", min_value=0.0, max_value=50000.0,
                                                       value=st.session_state.ch4_val, step=5.0)
        with col2:
            st.session_state.c2h6_val = st.number_input("Éthane (C₂H₆)", min_value=0.0, max_value=50000.0,
                                                        value=st.session_state.c2h6_val, step=5.0)
            st.session_state.c2h4_val = st.number_input("Éthylène (C₂H₄)", min_value=0.0, max_value=50000.0,
                                                        value=st.session_state.c2h4_val, step=2.0)
        with col3:
            st.session_state.c2h2_val = st.number_input("Acétylène (C₂H₂)", min_value=0.0, max_value=50000.0,
                                                        value=st.session_state.c2h2_val, step=1.0)
            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
            run = st.button("PRÉDIRE", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    if run:
        if not model_ok or not scaler_ok:
            st.markdown(
                "<div style='color:#DC2626; font-weight:bold; margin-left:1.5rem;'>Erreur: Modèle non disponible. Vérifiez les fichiers.</div>",
                unsafe_allow_html=True)
        else:
            with st.spinner("Analyse neuronale en cours..."):
                try:
                    gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]
                    input_df = pd.DataFrame([[st.session_state.h2_val, st.session_state.ch4_val, st.session_state.c2h6_val,
                                              st.session_state.c2h4_val, st.session_state.c2h2_val]], columns=gases)

                    input_df[gases] = np.log1p(input_df[gases])
                    input_df["R1"] = input_df["C2H2"] / (input_df["C2H4"] + 1e-6)
                    input_df["R2"] = input_df["CH4"] / (input_df["H2"] + 1e-6)
                    input_df["R3"] = input_df["C2H4"] / (input_df["CH4"] + 1e-6)
                    input_df["R4"] = input_df["C2H6"] / (input_df["CH4"] + 1e-6)
                    input_df["TOTAL"] = input_df[gases].sum(axis=1)

                    X = scaler.transform(input_df)
                    pred_class = model.predict(X)[0]
                    proba = model.predict_proba(X)[0]
                    fault = encoder.inverse_transform([pred_class])[0]
                    confidence = float(np.max(proba) * 100)

                    save_prediction(st.session_state.h2_val, st.session_state.ch4_val, st.session_state.c2h6_val,
                                    st.session_state.c2h4_val, st.session_state.c2h2_val, fault, confidence)

                    if "Arc" in fault or "High" in fault:
                        css_class, status_text, label_color = "critical", "État Critique Détecté", "#DC2626"
                    elif "Spark" in fault or "Middle" in fault:
                        css_class, status_text, label_color = "warning", "Anomalie Modérée", "#FF7A00"
                    else:
                        css_class, status_text, label_color = "normal", "Condition Optimale", "#10B981"

                    st.markdown(f"""
                    <div class="result-card {css_class}" style="margin: 0 1.5rem 2rem 1.5rem;">
                        <div style="font-size: 0.95rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; color: {label_color}; margin-bottom:10px;">{status_text}</div>
                        <div class="result-fault">{fault}</div>
                        <div class="result-confidence">Certitude IA : {confidence:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<div class="prob-container" style="margin: 0 1.5rem 2rem 1.5rem;">', unsafe_allow_html=True)
                    st.markdown(
                        "<h4 style='color: #0F2C59; font-weight: 800; margin-bottom: 20px; font-size:1.1rem;'>Distribution des Probabilités</h4>",
                        unsafe_allow_html=True)

                    classes = encoder.classes_
                    prob_df = pd.DataFrame({"Fault": classes, "Prob": proba * 100}).sort_values("Prob", ascending=False)

                    for _, row in prob_df.iterrows():
                        p = row["Prob"]
                        name = row["Fault"]
                        # PowerGuard Orange for winner, PowerGuard Blue for rest
                        fill_color = "linear-gradient(90deg, #FF914D, #FF7A00)" if name == fault else "linear-gradient(90deg, #0F2C59, #00A8E8)"

                        st.markdown(f"""
                        <div style="margin-bottom: 12px;">
                            <div style="display:flex; justify-content:space-between; font-size:0.9rem; font-weight:700; color:#1E293B; margin-bottom:4px;">
                                <span>{name}</span>
                                <span style="color:#64748B;">{p:.1f}%</span>
                            </div>
                            <div class="prob-bar-container">
                                <div class="prob-fill" style="width: {p:.1f}%; background: {fill_color};">{p:.1f}%</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Erreur: {e}")
                    st.code(traceback.format_exc())

    st.markdown(
        "<h3 style='color: #0F2C59; font-weight: 800; margin: 3rem 1.5rem 1rem 1.5rem; text-transform: uppercase; font-size:1.2rem;'>Registre des Opérations (Illimité)</h3>",
        unsafe_allow_html=True)

    try:
        if os.path.exists(HISTORY_FILE):
            hist = pd.read_csv(HISTORY_FILE)
            if not hist.empty and isinstance(hist, pd.DataFrame):
                # AFFICHAGE ILLIMITÉ
                hist_display = hist.iloc[::-1].reset_index(drop=True)
                hist_display.index = hist_display.index + 1

                html_table = hist_display.to_html(classes='custom-table', border=0)

                st.markdown(f"""
                <div class="table-wrapper">
                    <div class="custom-table-container">
                        {html_table}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(
                    "<div style='background:white; padding:20px; border-radius:8px; border:1px solid #E2E8F0; color:#64748B; font-weight:600; margin: 0 1.5rem;'>Le registre est actuellement vide.</div>",
                    unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='background:white; padding:20px; border-radius:8px; border:1px solid #E2E8F0; color:#64748B; font-weight:600; margin: 0 1.5rem;'>Aucun journal existant. La première analyse le créera automatiquement.</div>",
                unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Impossible de charger l'historique: {e}")


elif menu == "Supervision & Données":
    st.markdown("""
    <div class="dga-card" style="margin-top: 1rem;">
        <h1 class="hero-title">Supervision des Données</h1>
        <p class="hero-desc">Registre centralisé et statistiques des analyses prédictives effectuées sur l'ensemble du parc de transformateurs.</p>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists(HISTORY_FILE):
        hist = pd.read_csv(HISTORY_FILE)

        if not hist.empty:
            total_tests = len(hist)
            last_fault = hist.iloc[-1]["Diagnosis"]
            avg_conf = hist["Confidence_%"].mean()

            st.markdown(f"""
            <div class="metric-container" style="margin: 0 1.5rem 2rem 1.5rem; display: flex; gap: 20px;">
                <div class="metric-card">
                    <div class="metric-value">{total_tests}</div>
                    <div class="metric-label">Analyses Effectuées</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#0F2C59;">{last_fault}</div>
                    <div class="metric-label">Dernier Constat</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#10B981;">{avg_conf:.1f}%</div>
                    <div class="metric-label">Précision Moyenne</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                "<h3 style='color: #0F2C59; font-weight: 800; margin: 2rem 1.5rem 1rem 1.5rem; text-transform: uppercase; font-size:1.2rem;'>Journal Complet (Illimité)</h3>",
                unsafe_allow_html=True)

            recent_hist = hist.iloc[::-1].reset_index(drop=True)
            recent_hist.index = recent_hist.index + 1
            html_table = recent_hist.to_html(classes='custom-table', border=0)

            st.markdown(f"""
            <div class="table-wrapper">
                <div class="custom-table-container">
                    {html_table}
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(
                "<div style='background:white; padding:20px; border-radius:8px; border:1px solid #E2E8F0; color:#64748B; font-weight:600; margin: 0 1.5rem;'>La base de données est vierge.</div>",
                unsafe_allow_html=True)
    else:
        st.markdown(
            "<div style='background:white; padding:20px; border-radius:8px; border:1px solid #E2E8F0; color:#64748B; font-weight:600; margin: 0 1.5rem;'>Aucun journal existant. Veuillez effectuer une analyse.</div>",
            unsafe_allow_html=True)