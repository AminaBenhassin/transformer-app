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
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Sonelgaz DGA | Professional Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==============================
# PREPARATION DU LOGO LOCAL
# ==============================
# هذه الدالة الذكية تقرأ اللوغو من حاسوبك مباشرة لتفادي مشاكل الإنترنت
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    except Exception:
        # رابط احتياطي في حال لم تضع صورة logo.png في المجلد
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Sonelgaz_logo.svg/512px-Sonelgaz_logo.svg.png"


base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, "logo.png")
LOGO_SRC = get_base64_image(logo_path)

# ==============================
# CSS LIGHT THEME – PROFESSIONNEL, 3D
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

/* FOND AVEC IMAGE ET OVERLAY CLAIR */
.stApp {
    background: linear-gradient(135deg, rgba(240, 244, 250, 0.92) 0%, rgba(226, 232, 240, 0.95) 100%), 
                url('https://images.unsplash.com/photo-1581092334651-ddf26d9a09d0?auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed !important;
    background-size: cover !important;
    color: #0F172A;
}

/* SIDEBAR CLAIRE */
section[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 75, 135, 0.1);
    box-shadow: 4px 0 20px rgba(0,0,0,0.02);
}
.sidebar-header {
    text-align: center;
    padding: 1.8rem 0 1rem;
}
.sidebar-logo {
    width: 140px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    transition: transform 0.3s ease;
}
.sidebar-logo:hover {
    transform: scale(1.03);
}
.sidebar-title {
    font-weight: 800;
    font-size: 1.1rem;
    color: #004B87;
    text-align: center;
    letter-spacing: 1px;
    margin-top: 10px;
}
.metric-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #E2E8F0;
    transition: all 0.25s ease;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
    margin-bottom: 10px;
}
.metric-card:hover {
    transform: translateY(-3px);
    border-color: #004B87;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #F39C12;
}

/* TOP BAR */
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
    font-weight: 800;
    font-size: 1rem;
    color: #004B87;
}

/* HERO CARD */
.hero {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin: 0 1.5rem 2rem 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.8);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
}
.hero h1 {
    font-size: 2rem;
    font-weight: 800;
    color: #004B87;
    margin: 0 0 10px 0;
}
.hero p {
    color: #475569;
    font-size: 1.05rem;
    margin: 0;
    line-height: 1.6;
}

/* DGA CARD & INPUTS */
.dga-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 2.5rem;
    margin: 0 1.5rem 2rem 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.8);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
}
.dga-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: #004B87;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
}

.stNumberInput label {
    color: #1E293B !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
}
div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
    border: 1px solid #CBD5E1 !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #004B87 !important;
    box-shadow: 0 0 0 3px rgba(0, 75, 135, 0.1) !important;
    transform: translateY(-2px);
}
input {
    color: #004B87 !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
}

/* BOUTON 3D (PRÉDIRE) */
.stButton > button {
    background: linear-gradient(180deg, #F39C12 0%, #D68910 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    box-shadow: 0 6px 0 #935116, 0 10px 20px rgba(0,0,0,0.15) !important;
    width: 100% !important;
    margin-top: 1.6rem !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    transition: all 0.1s ease !important;
}
.stButton > button:hover {
    transform: translateY(2px) !important;
    box-shadow: 0 4px 0 #935116, 0 6px 15px rgba(0,0,0,0.15) !important;
    background: linear-gradient(180deg, #F4D03F 0%, #F39C12 100%) !important;
}
.stButton > button:active {
    transform: translateY(6px) !important;
    box-shadow: 0 0 0 #935116, 0 2px 5px rgba(0,0,0,0.1) !important;
}

/* RÉSULTAT CARD */
.result-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 1.5rem;
    border-left: 8px solid #F39C12;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}
.result-fault {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0.5rem 0;
}
.result-confidence {
    font-size: 1.1rem;
    font-weight: 700;
    color: #475569;
    background: #F1F5F9;
    padding: 8px 20px;
    border-radius: 50px;
    display: inline-block;
    border: 1px solid #E2E8F0;
}

/* BARRES DE PROBABILITÉ */
.prob-container {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin: 1rem 1.5rem;
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
    background: linear-gradient(90deg, #004B87, #3B82F6);
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

/* Cacher éléments natifs Streamlit */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================
# FONCTIONS DE CHARGEMENT
# ==============================
MODELS_DIR = os.path.join(base_dir, "models_saved")
HISTORY_FILE = os.path.join(base_dir, "history.csv")


def get_available_models():
    if not os.path.exists(MODELS_DIR): return []
    all_pkl = glob.glob(os.path.join(MODELS_DIR, "*.pkl"))
    exclude_keywords = ['scaler', 'encoder', 'label']
    models = []
    for f in all_pkl:
        name = os.path.basename(f).lower()
        if not any(kw in name for kw in exclude_keywords):
            models.append(f)
    return models


@st.cache_resource
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


@st.cache_resource
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
                else:
                    return len(df), None
            return 0, None
        return 0, None
    except:
        return 0, None


def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        return True
    return False


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
        <div class="sidebar-title">SONELGAZ DGA</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:0.8rem; font-weight:700; color:#475569; text-transform:uppercase; margin-bottom:5px;'>Sélection du modèle</div>",
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
        "<br><div style='font-size:0.8rem; font-weight:700; color:#475569; text-transform:uppercase; margin-bottom:10px;'>Aperçu Rapide</div>",
        unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"<div class='metric-card'><div class='metric-value'>{total_analyses}</div><div style='font-size:0.75rem; font-weight:600; color:#64748B; text-transform:uppercase;'>Analyses</div></div>",
            unsafe_allow_html=True)
    with col2:
        if last_diag is not None and isinstance(last_diag, pd.Series):
            diag_value = last_diag.get('Diagnosis', 'Inconnu')
            diag_text = str(diag_value)[:12]
            st.markdown(
                f"<div class='metric-card'><div style='font-size:1.1rem; font-weight:800; color:#004B87; padding:10px 0;'>{diag_text}</div><div style='font-size:0.75rem; font-weight:600; color:#64748B; text-transform:uppercase;'>Dernier</div></div>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='metric-card'><div style='font-size:0.8rem; color:#64748B; padding:15px 0;'>Vide</div></div>",
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
        <img src="{LOGO_SRC}" width="30">
        <div class="logo-text">SONELGAZ · SYSTÈME EXPERT DGA</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>Plateforme de Maintenance Prédictive</h1>
    <p>
        Ce système expert analyse les concentrations de gaz dissous (DGA) dans l'huile des transformateurs de puissance. 
        En utilisant un modèle d'Intelligence Artificielle, il diagnostique l'état de l'équipement pour prévenir les défaillances critiques.
    </p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="dga-card">', unsafe_allow_html=True)
    st.markdown('<div class="dga-title">Saisie des Concentrations de Gaz (PPM)</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        H2 = st.number_input("Hydrogène (H₂)", min_value=0.0, max_value=50000.0, value=100.0, step=10.0)
        CH4 = st.number_input("Méthane (CH₄)", min_value=0.0, max_value=50000.0, value=50.0, step=5.0)
    with col2:
        C2H6 = st.number_input("Éthane (C₂H₆)", min_value=0.0, max_value=50000.0, value=20.0, step=5.0)
        C2H4 = st.number_input("Éthylène (C₂H₄)", min_value=0.0, max_value=50000.0, value=10.0, step=2.0)
    with col3:
        C2H2 = st.number_input("Acétylène (C₂H₂)", min_value=0.0, max_value=50000.0, value=5.0, step=1.0)
        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
        run = st.button("PRÉDIRE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if run:
    if not model_ok or not scaler_ok:
        st.markdown(
            "<div style='color:#DC2626; font-weight:bold; margin-left:1.5rem;'>Erreur: Modèle non disponible.</div>",
            unsafe_allow_html=True)
    else:
        with st.spinner("Analyse neuronale en cours..."):
            try:
                gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]
                input_df = pd.DataFrame([[H2, CH4, C2H6, C2H4, C2H2]], columns=gases)
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

                save_prediction(H2, CH4, C2H6, C2H4, C2H2, fault, confidence)

                # Résultat
                st.markdown(f"""
                <div class="result-card">
                    <div style="font-size:0.9rem; font-weight:700; color:#F39C12; text-transform:uppercase; letter-spacing:1px;">Résultat du Diagnostic</div>
                    <div class="result-fault">{fault}</div>
                    <div class="result-confidence">Certitude IA : {confidence:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

                # Barres de probabilité EXACTEMENT comme votre code d'origine (mais stylisées)
                st.markdown('<div class="prob-container">', unsafe_allow_html=True)
                st.markdown(
                    "<h4 style='color: #004B87; font-weight: 800; margin-bottom: 20px; font-size:1.1rem;'>Distribution des Probabilités</h4>",
                    unsafe_allow_html=True)

                classes = encoder.classes_
                prob_df = pd.DataFrame({"Fault": classes, "Prob": proba * 100}).sort_values("Prob", ascending=False)

                for _, row in prob_df.iterrows():
                    p = row["Prob"]
                    name = row["Fault"]
                    # Couleur distinctive pour le résultat choisi
                    fill_color = "linear-gradient(90deg, #F39C12, #D68910)" if name == fault else "linear-gradient(90deg, #004B87, #3B82F6)"

                    st.markdown(f"""
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.9rem; font-weight:600; color:#1E293B; margin-bottom:4px;">
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

# ==============================
# HISTORIQUE (st.dataframe exact de votre code)
# ==============================
st.markdown(
    "<h3 style='color: #004B87; font-weight: 800; margin: 3rem 1.5rem 1rem 1.5rem;'>Registre des Opérations</h3>",
    unsafe_allow_html=True)

st.markdown('<div style="margin: 0 1.5rem;">', unsafe_allow_html=True)
try:
    if os.path.exists(HISTORY_FILE):
        hist = pd.read_csv(HISTORY_FILE)
        if not hist.empty and isinstance(hist, pd.DataFrame):
            hist_display = hist.reset_index(drop=True)
            hist_display.index = hist_display.index + 1
            st.dataframe(hist_display, use_container_width=True, height=350)
        else:
            st.info("Le registre est vide.")
    else:
        st.info("Aucun journal existant. La première analyse le créera.")
except Exception as e:
    st.warning(f"Impossible de charger l'historique: {e}")
st.markdown('</div>', unsafe_allow_html=True)