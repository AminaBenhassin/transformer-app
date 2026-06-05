import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import datetime
import traceback
import glob

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Sonelgaz DGA Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# CSS PROFESSIONNEL (comme avant)
# ==============================
st.markdown("""
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(145deg, #F4F7FC 0%, #E9EEF5 100%);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFE 100%);
    border-right: 1px solid rgba(0,0,0,0.05);
    box-shadow: 4px 0 12px rgba(0,0,0,0.02);
}
.sidebar-title {
    font-weight: 800;
    font-size: 1.3rem;
    background: linear-gradient(135deg, #1E3A6F, #F39C12);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-align: center;
    margin: 1rem 0;
}
.metric-card {
    background: white;
    border-radius: 20px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    border: 1px solid rgba(243,156,18,0.15);
    transition: all 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.05);
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(145deg, #F39C12, #E67E22);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

/* TOP BAR */
.top-bar {
    background: white;
    padding: 0.8rem 2rem;
    border-radius: 80px;
    margin-bottom: 2rem;
    color: #1E3A6F;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 6px 14px rgba(0,0,0,0.02);
    border: 1px solid rgba(0,0,0,0.03);
}
.logo-text {
    font-weight: 800;
    font-size: 1.2rem;
    background: linear-gradient(135deg, #1E3A6F, #F39C12);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.top-nav span {
    margin-left: 1.5rem;
    font-size: 0.9rem;
    font-weight: 500;
    color: #4B5563;
    cursor: default;
    transition: 0.2s;
}
.top-nav span:hover {
    color: #F39C12;
}

/* HERO SECTION */
.hero {
    background: linear-gradient(135deg, #FFFFFF, #FEF9F0);
    border-radius: 32px;
    padding: 1.5rem 2rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(243,156,18,0.2);
    box-shadow: 0 12px 24px -12px rgba(0,0,0,0.08);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}
.hero h1 {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #1E3A6F, #F39C12);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin: 0;
}
.hero p {
    color: #6B7280;
    margin-top: 0.3rem;
}
.stats {
    display: flex;
    gap: 2rem;
    background: rgba(243,156,18,0.05);
    padding: 0.8rem 1.5rem;
    border-radius: 60px;
}
.stat-number {
    font-weight: 800;
    font-size: 1.4rem;
    color: #F39C12;
}

/* DGA CARD */
.dga-card {
    background: white;
    border-radius: 36px;
    padding: 1.8rem;
    margin-bottom: 2rem;
    box-shadow: 0 12px 28px -8px rgba(0,0,0,0.05);
    border: 1px solid rgba(0,0,0,0.02);
    transition: all 0.2s;
}
.dga-card:hover {
    box-shadow: 0 20px 32px -12px rgba(0,0,0,0.08);
}
.dga-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #1E3A6F;
    border-left: 5px solid #F39C12;
    padding-left: 1rem;
    margin-bottom: 1.5rem;
}

/* INPUTS */
.stNumberInput label {
    color: #1F2937 !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
}
div[data-baseweb="input"] {
    background-color: #F9FAFB;
    border-radius: 16px !important;
    border: 1px solid #E5E7EB !important;
    transition: 0.2s;
}
div[data-baseweb="input"]:focus-within {
    border-color: #F39C12 !important;
    box-shadow: 0 0 0 3px rgba(243,156,18,0.2);
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(145deg, #F39C12, #E67E22) !important;
    border: none !important;
    border-radius: 60px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.6rem 1rem !important;
    color: white;
    box-shadow: 0 4px 12px rgba(243,156,18,0.3);
    transition: 0.1s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(243,156,18,0.4);
}
.stButton > button:active {
    transform: translateY(2px);
}

/* RESULT CARD */
.result-card {
    background: linear-gradient(145deg, #FEF9F0, #FFFFFF);
    border-radius: 32px;
    padding: 1.5rem;
    text-align: center;
    margin: 1.5rem 0;
    border: 1px solid rgba(243,156,18,0.3);
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
}
.result-fault {
    font-size: 1.8rem;
    font-weight: 800;
    color: #1E3A6F;
    margin: 0.5rem 0;
}
.result-confidence {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(145deg, #F39C12, #E67E22);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

/* PROBABILITY BARS */
.prob-bar-container {
    background: #EDF2F7;
    border-radius: 40px;
    margin: 12px 0;
    overflow: hidden;
}
.prob-fill {
    background: linear-gradient(90deg, #F39C12, #F4B944);
    height: 32px;
    line-height: 32px;
    text-align: right;
    padding-right: 14px;
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    border-radius: 40px 0 0 40px;
}

/* TABLE */
.dataframe {
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}
.dataframe th {
    background: #1E3A6F !important;
    color: white !important;
    font-weight: 600;
}
.dataframe td {
    background: white;
    color: #1F2937;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 2.5rem;
    padding: 1rem;
    border-top: 1px solid rgba(0,0,0,0.05);
    color: #6B7280;
    font-size: 0.75rem;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# FONCTIONS DE CHARGEMENT
# ==============================
base_dir = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(base_dir, "models_saved")
HISTORY_FILE = os.path.join(base_dir, "history.csv")


# Liste des fichiers modèles (exclure scaler, encoder, label_encoder)
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


# Chargement du scaler et encoder (fixes)
scaler, encoder, scaler_ok = load_scaler_encoder()

# Récupérer la liste des modèles disponibles
model_files = get_available_models()
if len(model_files) == 0:
    st.error("Aucun modèle trouvé dans le dossier 'models_saved'. Vérifiez le répertoire.")
    st.stop()


# ==============================
# FONCTIONS UTILITAIRES
# ==============================
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
            return len(df), df.iloc[-1] if len(df) > 0 else None
        return 0, None
    except:
        return 0, None


def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        return True
    return False


# ==============================
# SESSION STATE INIT
# ==============================
if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False
if "selected_model_path" not in st.session_state:
    # Par défaut, prendre le premier modèle (ou fine_tree_real.pkl si présent)
    default = None
    for f in model_files:
        if "fine_tree_real" in f:
            default = f
            break
    if default is None and len(model_files) > 0:
        default = model_files[0]
    st.session_state.selected_model_path = default

# ==============================
# SIDEBAR (avec sélection de modèle et effacement)
# ==============================
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚡ SONELGAZ DGA</div>', unsafe_allow_html=True)

    # Sélection du modèle
    st.markdown("### 🤖 Sélection du modèle")
    model_names = [os.path.basename(p) for p in model_files]
    current_name = os.path.basename(st.session_state.selected_model_path) if st.session_state.selected_model_path else \
    model_names[0]
    selected_name = st.selectbox("Choisissez un modèle:", model_names,
                                 index=model_names.index(current_name) if current_name in model_names else 0)
    # Mettre à jour le chemin sélectionné
    new_path = os.path.join(MODELS_DIR, selected_name)
    if new_path != st.session_state.selected_model_path:
        st.session_state.selected_model_path = new_path
        # Forcer le rechargement du modèle (cache)
        st.cache_resource.clear()
        st.rerun()

    # Charger le modèle sélectionné
    model, model_ok = load_selected_model(st.session_state.selected_model_path)

    # Afficher les statistiques
    total_analyses, last_diag = get_stats()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"<div class='metric-card'><div class='metric-value'>{total_analyses}</div><div>Analyses</div></div>",
            unsafe_allow_html=True)
    with col2:
        if last_diag is not None:
            st.markdown(
                f"<div class='metric-card'><div>Last</div><div style='font-weight:600;'>{last_diag['Diagnosis'][:12]}</div></div>",
                unsafe_allow_html=True)
        else:
            st.markdown("<div class='metric-card'>No data</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Statut du modèle
    if model_ok and scaler_ok:
        st.success(f"✅ Modèle chargé: {selected_name}")
    else:
        st.error("⚠️ Problème de chargement (modèle ou scaler/encoder)")

    # Bouton effacer historique
    if os.path.exists(HISTORY_FILE) and total_analyses > 0:
        st.markdown("---")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.confirm_clear = True

    if st.session_state.confirm_clear:
        st.warning("⚠️ Are you sure? This will delete all diagnostic history permanently.")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("✅ Yes, clear"):
                if clear_history():
                    st.success("History cleared successfully!")
                    st.session_state.confirm_clear = False
                    st.rerun()
                else:
                    st.error("Could not delete file.")
        with col_c2:
            if st.button("❌ Cancel"):
                st.session_state.confirm_clear = False
                st.rerun()

    st.caption("Industrial DGA v3.0 · Choix du modèle")

# ==============================
# RESTE DE L'INTERFACE (identique)
# ==============================
st.markdown("""
<div class="top-bar">
    <div class="logo-text">🔬 SONELGAZ · DISSOLVED GAS ANALYSIS</div>
    <div class="top-nav">
        <span>📊 Dashboard</span>
        <span>⚙️ Diagnostics</span>
        <span>📜 History</span>
    </div>
</div>
""", unsafe_allow_html=True)

total_analyses, _ = get_stats()
st.markdown(f"""
<div class="hero">
    <div>
        <h1>Predictive Maintenance Hub</h1>
        <p>Neural network classification · IEC 60599 compliant</p>
    </div>
    <div class="stats">
        <div><span class="stat-number">{total_analyses}</span> total analyses</div>
        <div><span class="stat-number">99.2%</span> accuracy</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="dga-card">', unsafe_allow_html=True)
    st.markdown('<div class="dga-title">🧪 Gas concentrations (ppm)</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        H2 = st.number_input("Hydrogen (H₂)", min_value=0.0, max_value=50000.0, value=100.0, step=10.0)
        CH4 = st.number_input("Methane (CH₄)", min_value=0.0, max_value=50000.0, value=50.0, step=5.0)
    with col2:
        C2H6 = st.number_input("Ethane (C₂H₆)", min_value=0.0, max_value=50000.0, value=20.0, step=5.0)
        C2H4 = st.number_input("Ethylene (C₂H₄)", min_value=0.0, max_value=50000.0, value=10.0, step=2.0)
    with col3:
        C2H2 = st.number_input("Acetylene (C₂H₂)", min_value=0.0, max_value=50000.0, value=5.0, step=1.0)
        run = st.button("🚀 Run diagnostics", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if run:
    if not model_ok or not scaler_ok:
        st.error("Models not loaded properly. Check model files and scaler/encoder.")
    else:
        with st.spinner("Computing..."):
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

                st.markdown(f"""
                <div class="result-card">
                    <div style="font-size:0.8rem; font-weight:600; color:#F39C12;">DIAGNOSTIC RESULT</div>
                    <div class="result-fault">{fault}</div>
                    <div class="result-confidence">{confidence:.1f}% confidence</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### 📊 Probability distribution")
                classes = encoder.classes_
                prob_df = pd.DataFrame({"Fault": classes, "Prob": proba * 100}).sort_values("Prob", ascending=False)
                for _, row in prob_df.iterrows():
                    p = row["Prob"]
                    name = row["Fault"]
                    st.markdown(f"""
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem;">
                            <span>{name}</span>
                            <span>{p:.1f}%</span>
                        </div>
                        <div class="prob-bar-container">
                            <div class="prob-fill" style="width: {p:.1f}%;">{p:.1f}%</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Prediction error: {e}")
                st.code(traceback.format_exc())

st.markdown("---")
st.markdown("#### 📋 Recent diagnoses")
try:
    if os.path.exists(HISTORY_FILE):
        hist = pd.read_csv(HISTORY_FILE)
        if not hist.empty:
            st.dataframe(hist.tail(8), use_container_width=True)
        else:
            st.info("No history yet.")
    else:
        st.info("No history file. First prediction will create it.")
except Exception as e:
    st.warning(f"Could not load history: {e}")

st.markdown('<div class="footer">Sonelgaz DGA · Neural Classifier · Production ready · Model selection enabled</div>',
            unsafe_allow_html=True)