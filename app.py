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
    page_title="Sonelgaz DGA | Premium Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# ULTIMATE PREMIUM UI/UX CSS
# ==============================
st.markdown("""
<style>
/* استدعاء خط عصري جداً ومريح للعين */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ========== FOND GLOBAL ET TYPOGRAPHIE ========== */
.stApp {
    background-color: #F4F7F9; /* لون مريح جداً للعين للعمل لساعات */
    color: #1E293B;
}

/* ========== SIDEBAR PREMIUM ========== */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
    padding-top: 2rem;
}
.sidebar-logo-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-bottom: 2rem;
    border-bottom: 1px solid #F1F5F9;
    margin-bottom: 2rem;
}
.sidebar-logo {
    width: 120px;
    margin-bottom: 15px;
    transition: transform 0.3s ease;
}
.sidebar-logo:hover {
    transform: scale(1.05);
}
.sidebar-title {
    font-weight: 800;
    font-size: 1.2rem;
    color: #0F172A;
    letter-spacing: 0.5px;
}

/* ========== TOP BAR & HERO SECTION ========== */
.hero-container {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05);
    border: 1px solid #F1F5F9;
    transition: all 0.3s ease;
}
.hero-container:hover {
    box-shadow: 0 15px 50px -10px rgba(0,0,0,0.08);
    transform: translateY(-2px);
}
.hero-text h1 {
    font-size: 2rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0 0 8px 0;
}
.hero-text p {
    color: #64748B;
    font-size: 1rem;
    margin: 0;
    font-weight: 500;
}
.hero-stats {
    display: flex;
    gap: 20px;
}
.stat-pill {
    background: #F8FAFC;
    padding: 10px 20px;
    border-radius: 50px;
    border: 1px solid #E2E8F0;
    font-weight: 700;
    color: #3B82F6;
    display: flex;
    align-items: center;
    gap: 8px;
}
.stat-pill span {
    color: #64748B;
    font-weight: 500;
    font-size: 0.9rem;
}

/* ========== INPUT CARDS & FORMS ========== */
.input-section {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05);
    border: 1px solid #F1F5F9;
    margin-bottom: 2rem;
}
.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::before {
    content: '';
    display: inline-block;
    width: 6px;
    height: 24px;
    background: #F59E0B;
    border-radius: 4px;
}

/* Streamlit Native Inputs override */
.stNumberInput label {
    font-weight: 600 !important;
    color: #475569 !important;
    font-size: 0.9rem !important;
}
div[data-baseweb="input"] {
    background-color: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}
div[data-baseweb="input"]:focus-within {
    background-color: #FFFFFF !important;
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
}
input {
    font-weight: 700 !important;
    color: #0F172A !important;
    font-size: 1.1rem !important;
}

/* ========== PREMIUM ACTION BUTTON ========== */
.stButton > button {
    background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    padding: 1rem !important;
    border: none !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 20px -5px rgba(245, 158, 11, 0.4) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100% !important;
    margin-top: 1.5rem !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 25px -5px rgba(245, 158, 11, 0.5) !important;
}
.stButton > button:active {
    transform: translateY(1px) !important;
}

/* ========== DYNAMIC RESULT CARD ========== */
.result-card {
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin-top: 1rem;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    color: white;
    box-shadow: 0 15px 30px -10px rgba(0,0,0,0.1);
}
.result-normal { background: linear-gradient(135deg, #10B981 0%, #059669 100%); }
.result-warning { background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); }
.result-danger { background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); }

.result-title {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 700;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}
.result-fault {
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.result-confidence {
    font-size: 1.1rem;
    font-weight: 600;
    background: rgba(255,255,255,0.2);
    display: inline-block;
    padding: 6px 16px;
    border-radius: 50px;
    margin-top: 1rem;
    backdrop-filter: blur(5px);
}

/* ========== PROBABILITY BARS ========== */
.prob-container {
    margin-top: 2rem;
    padding: 2rem;
    background: #FFFFFF;
    border-radius: 20px;
    box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05);
}
.prob-item { margin-bottom: 1rem; }
.prob-header {
    display: flex;
    justify-content: space-between;
    font-weight: 600;
    color: #475569;
    font-size: 0.9rem;
    margin-bottom: 6px;
}
.prob-track {
    background: #F1F5F9;
    border-radius: 50px;
    height: 12px;
    overflow: hidden;
}
.prob-fill {
    height: 100%;
    border-radius: 50px;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ========== HISTORY TABLE ========== */
.dataframe {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}
.dataframe th {
    background: #F8FAFC !important;
    color: #475569 !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 12px 15px !important;
    border-bottom: 2px solid #E2E8F0 !important;
}
.dataframe td {
    padding: 12px 15px !important;
    border-bottom: 1px solid #F1F5F9 !important;
    color: #1E293B !important;
    font-weight: 500;
}
.dataframe tr:hover td {
    background: #F8FAFC !important;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# FONCTIONS DE CHARGEMENT
# ==============================
base_dir = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(base_dir, "models_saved")
HISTORY_FILE = os.path.join(base_dir, "history.csv")


def get_available_models():
    if not os.path.exists(MODELS_DIR): return []
    all_pkl = glob.glob(os.path.join(MODELS_DIR, "*.pkl"))
    exclude_keywords = ['scaler', 'encoder', 'label']
    return [f for f in all_pkl if not any(kw in os.path.basename(f).lower() for kw in exclude_keywords)]


@st.cache_resource
def load_scaler_encoder():
    try:
        return joblib.load(os.path.join(MODELS_DIR, "scaler.pkl")), joblib.load(
            os.path.join(MODELS_DIR, "encoder.pkl")), True
    except:
        return None, None, False


@st.cache_resource
def load_selected_model(model_path):
    try:
        return joblib.load(model_path), True
    except:
        return None, False


scaler, encoder, scaler_ok = load_scaler_encoder()
model_files = get_available_models()


def save_prediction(h2, ch4, c2h6, c2h4, c2h2, fault, conf):
    try:
        new_row = pd.DataFrame([{
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "H2": h2, "CH4": ch4, "C2H6": c2h6, "C2H4": c2h4, "C2H2": c2h2,
            "Diagnosis": fault, "Confidence_%": round(conf, 1)
        }])
        if os.path.exists(HISTORY_FILE):
            old = pd.read_csv(HISTORY_FILE)
            pd.concat([old, new_row], ignore_index=True).to_csv(HISTORY_FILE, index=False)
        else:
            new_row.to_csv(HISTORY_FILE, index=False)
    except:
        pass


def get_stats():
    try:
        if os.path.exists(HISTORY_FILE):
            df = pd.read_csv(HISTORY_FILE)
            return len(df), df.iloc[-1] if len(df) > 0 else None
    except:
        pass
    return 0, None


if "selected_model_path" not in st.session_state:
    st.session_state.selected_model_path = model_files[0] if model_files else None

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo-container">
        <img class="sidebar-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Sonelgaz_logo.svg/512px-Sonelgaz_logo.svg.png">
        <div class="sidebar-title">SONELGAZ AI LAB</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='color:#64748B; font-weight:600; font-size:0.8rem; text-transform:uppercase;'>Configuration</p>",
        unsafe_allow_html=True)
    if model_files:
        model_names = [os.path.basename(p) for p in model_files]
        current_name = os.path.basename(
            st.session_state.selected_model_path) if st.session_state.selected_model_path else model_names[0]
        selected_name = st.selectbox("Modèle IA Actif", model_names, index=model_names.index(current_name))
        new_path = os.path.join(MODELS_DIR, selected_name)
        if new_path != st.session_state.selected_model_path:
            st.session_state.selected_model_path = new_path
            st.cache_resource.clear()
            st.rerun()

    model, model_ok = load_selected_model(st.session_state.selected_model_path)

    if os.path.exists(HISTORY_FILE):
        st.markdown(
            "<br><p style='color:#64748B; font-weight:600; font-size:0.8rem; text-transform:uppercase;'>Maintenance</p>",
            unsafe_allow_html=True)
        if st.button("Effacer l'historique", use_container_width=True):
            os.remove(HISTORY_FILE)
            st.rerun()

# ==============================
# MAIN CONTENT
# ==============================
total_analyses, _ = get_stats()

# Hero Section
st.markdown(f"""
<div class="hero-container">
    <div class="hero-text">
        <h1>Analyse DGA Intelligente</h1>
        <p>Diagnostic de l'état de santé des transformateurs assisté par IA.</p>
    </div>
    <div class="hero-stats">
        <div class="stat-pill">{total_analyses} <span>Analyses</span></div>
        <div class="stat-pill">99.2% <span>Précision</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Saisie des gaz dissous (ppm)</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    H2 = st.number_input("Hydrogène (H₂)", min_value=0.0, value=100.0, step=10.0)
    CH4 = st.number_input("Méthane (CH₄)", min_value=0.0, value=50.0, step=5.0)
with col2:
    C2H6 = st.number_input("Éthane (C₂H₆)", min_value=0.0, value=20.0, step=5.0)
    C2H4 = st.number_input("Éthylène (C₂H₄)", min_value=0.0, value=10.0, step=2.0)
with col3:
    C2H2 = st.number_input("Acétylène (C₂H₂)", min_value=0.0, value=5.0, step=1.0)
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)  # spacer
    run = st.button("Générer le diagnostic IA")

st.markdown('</div>', unsafe_allow_html=True)

# Prediction Logic
if run:
    if not model_ok or not scaler_ok:
        st.error("Le modèle IA n'est pas prêt.")
    else:
        with st.spinner("Analyse des schémas neuronaux en cours..."):
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

                # تحديد اللون بناءً على نوع العطل
                theme_class = "result-normal"
                bar_color = "#10B981"
                if "Arc" in fault or "High" in fault:
                    theme_class = "result-danger"
                    bar_color = "#EF4444"
                elif "Spark" in fault or "Middle" in fault:
                    theme_class = "result-warning"
                    bar_color = "#F59E0B"

                # Display Result
                st.markdown(f"""
                <div class="result-card {theme_class}">
                    <div class="result-title">Verdict de l'Intelligence Artificielle</div>
                    <h2 class="result-fault">{fault}</h2>
                    <div class="result-confidence">Taux de confiance : {confidence:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

                # Probability Distribution
                st.markdown('<div class="prob-container">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Distribution des probabilités</div>', unsafe_allow_html=True)

                prob_df = pd.DataFrame({"Fault": encoder.classes_, "Prob": proba * 100}).sort_values("Prob",
                                                                                                     ascending=False)
                for _, row in prob_df.iterrows():
                    p = row["Prob"]
                    name = row["Fault"]
                    color = bar_color if name == fault else "#CBD5E1"  # Highlight winning prob
                    st.markdown(f"""
                    <div class="prob-item">
                        <div class="prob-header">
                            <span>{name}</span>
                            <span>{p:.1f}%</span>
                        </div>
                        <div class="prob-track">
                            <div class="prob-fill" style="width: {p}%; background-color: {color};"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erreur d'analyse: {e}")

# History Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Historique des opérations</div>', unsafe_allow_html=True)
if os.path.exists(HISTORY_FILE):
    hist = pd.read_csv(HISTORY_FILE)
    if not hist.empty:
        # ترتيب عكسي لظهور الأحدث أولاً
        st.dataframe(hist.iloc[::-1].reset_index(drop=True), use_container_width=True, height=300)
    else:
        st.info("La base de données est vide.")
else:
    st.info("Effectuez votre premier diagnostic pour initialiser l'historique.")
st.markdown('</div>', unsafe_allow_html=True)