import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import datetime
import traceback
import base64

# ==============================
# CONFIGURATION
# ==============================
st.set_page_config(page_title="PowerGuard | Système Expert DGA", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* اخفاء Deploy و GitHub */
[data-testid="stToolbar"] {display: none;}
[data-testid="stDecoration"] {display: none;}
[data-testid="stStatusWidget"] {display: none;}
[data-testid="stHeader"] {display: none;}

/* اخفاء كلمة Streamlit */
.css-18e3th9 {padding-top: 0rem;}

</style>
""", unsafe_allow_html=True)
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    except:
        return ""


base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, "logo.png")
LOGO_SRC = get_base64_image(logo_path)

# ==============================
# CSS PROFESSIONNEL
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }

.stApp { 
    background: linear-gradient(135deg, rgba(241, 245, 249, 0.9), rgba(241, 245, 249, 0.9)), 
                url('https://images.unsplash.com/photo-1581092334651-ddf26d9a09d0?auto=format&fit=crop&w=1920&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
section[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E2E8F0; }
.sidebar-logo { width: 160px; margin-bottom: 20px; transition: transform 0.3s; }
.sidebar-logo:hover { transform: scale(1.05); }

/* MENU AMÉLIORÉ */
div.row-widget.stRadio > div { gap: 10px; padding: 10px; }
div.row-widget.stRadio > div > label {
    background-color: #F8FAFC;
    padding: 14px 18px;
    border-radius: 10px;
    border: 1px solid #E2E8F0;
    cursor: pointer;
    font-weight: 600;
    color: #475569 !important;
    transition: all 0.2s ease;
}
div.row-widget.stRadio > div > label:hover {
    background-color: #F1F5F9;
    border-color: #00A8E8;
}
div.row-widget.stRadio > div > label[data-checked="true"] {
    background-color: #0F2C59 !important;
    color: white !important;
    border-color: #0F2C59;
    border-left: 6px solid #FF7A00 !important;
}
div.row-widget.stRadio > div > label > div:first-child { display: none; } 

.dga-card { background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 2rem; }

/* =========================================
   UI/UX DES CHAMPS DE SAISIE (FORCÉ)
   ========================================= */
div[data-testid="stNumberInput"] label p {
    color: #1E293B !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
}
/* استهداف الصندوق نفسه بقوة */
div[data-testid="stNumberInput"] > div > div > div {
    background-color: #F1F5F9 !important; 
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
}
/* التأثير عند الضغط (Focus) */
div[data-testid="stNumberInput"] > div > div > div:focus-within {
    border-color: #FF7A00 !important;
    box-shadow: 0 0 0 1.5px #FF7A00 !important;
    background-color: #FFFFFF !important;
}
div[data-testid="stNumberInput"] input {
    color: #1E293B !important;
    font-weight: 600 !important;
}

/* ANIMATION DES GAZ (3D EFFECT) */
.sensors-container { 
    display: flex; justify-content: space-around; align-items: center; 
    margin: 1.5rem 0 3rem 0; padding: 2.5rem 1rem; 
    background: rgba(255,255,255,0.6); border-radius: 16px; 
    border: 1px solid rgba(255,255,255,0.8); box-shadow: inset 0 4px 15px rgba(0,0,0,0.02); 
}
.gas-orb-wrapper { display: flex; flex-direction: column; align-items: center; width: 100px; }
.gas-orb { 
    position: relative; width: 85px; height: 85px; border-radius: 50%; 
    background: radial-gradient(circle at 30% 30%, #ffffff, #cbd5e1);
    display: flex; align-items: center; justify-content: center; 
    box-shadow: 0 10px 20px rgba(0,0,0,0.15), inset -5px -5px 10px rgba(0,0,0,0.1); 
    animation: floatOrb 4s ease-in-out infinite; 
}
.gas-orb-wrapper:nth-child(2) .gas-orb { animation-delay: 0.5s; }
.gas-orb-wrapper:nth-child(3) .gas-orb { animation-delay: 1s; }
.gas-orb-wrapper:nth-child(4) .gas-orb { animation-delay: 1.5s; }
.gas-orb-wrapper:nth-child(5) .gas-orb { animation-delay: 2s; }

.gas-ring {
    position: absolute; top: -6px; left: -6px; right: -6px; bottom: -6px;
    border-radius: 50%; border: 3px dashed #00A8E8;
    border-top-color: transparent !important; opacity: 0.8;
    animation: spinRing 6s linear infinite;
}
.gas-name { font-size: 1.5rem; font-weight: 800; color: #0F2C59; margin: 0; }

@keyframes spinRing { 100% { transform: rotate(360deg); } }
@keyframes floatOrb { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }

/* BOUTON PRÉDIRE */
.stButton > button { 
    background: linear-gradient(180deg, #FF914D 0%, #FF7A00 100%) !important; 
    color: white !important; font-weight: 800 !important; width: 100%; 
    padding: 12px !important; border-radius: 8px !important; border: none !important;
    box-shadow: 0 4px 0 #CC6200, 0 8px 15px rgba(255, 122, 0, 0.2) !important;
    text-transform: uppercase; letter-spacing: 1px;
}
.stButton > button:hover { transform: translateY(2px) !important; box-shadow: 0 2px 0 #CC6200, 0 4px 10px rgba(255, 122, 0, 0.2) !important; }
.stButton > button:active { transform: translateY(4px) !important; box-shadow: 0 0 0 #CC6200 !important; }

/* HISTORIQUE UNLIMITED */
.table-wrapper { max-height: 450px; overflow-y: auto; background: white; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 2rem; }
.custom-table { width: 100%; border-collapse: collapse; text-align: left; }
.custom-table th { background: #0F2C59; color: white; padding: 15px 20px; position: sticky; top:0; z-index: 10; text-transform: uppercase; font-size: 12px; }
.custom-table td { padding: 15px 20px; border-bottom: 1px solid #F1F5F9; color: #1E293B; font-weight: 500; font-size: 14px; }
.custom-table tr:hover td { background-color: #F8FAFC; }

/* METRICS */
.metric-container { display: flex; gap: 20px; margin-bottom: 2rem; }
.metric-card { background: white; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; flex: 1; border-top: 4px solid #0F2C59; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
.metric-value { font-size: 2rem; font-weight: 900; color: #0F2C59; }
.metric-label { font-size: 0.85rem; color: #64748B; font-weight: 700; text-transform: uppercase; margin-top: 5px; }

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
[data-testid="stHeader"] { background-color: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# LOGIQUE & CHARGEMENT
# ==============================
MODELS_DIR = os.path.join(base_dir, "models_saved")
HISTORY_FILE = os.path.join(base_dir, "history.csv")


@st.cache_resource(show_spinner=False)
def load_ai():
    m = joblib.load(os.path.join(MODELS_DIR, "fine_tree_real.pkl"))
    s = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    e = joblib.load(os.path.join(MODELS_DIR, "encoder.pkl"))
    return m, s, e


model, scaler, encoder = load_ai()


def save_prediction(h2, ch4, c2h6, c2h4, c2h2, fault, conf):
    new_row = pd.DataFrame([{
        "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "H2": h2, "CH4": ch4, "C2H6": c2h6, "C2H4": c2h4, "C2H2": c2h2,
        "Diagnosis": fault, "Confidence_%": round(conf, 1)
    }])
    if os.path.exists(HISTORY_FILE):
        pd.concat([pd.read_csv(HISTORY_FILE), new_row], ignore_index=True).to_csv(HISTORY_FILE, index=False)
    else:
        new_row.to_csv(HISTORY_FILE, index=False)


def get_stats():
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        if not df.empty:
            return len(df), df.iloc[-1]['Diagnosis']
    return 0, "Aucun"


total_analyses, last_diag = get_stats()

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.markdown(f'<div style="text-align:center;"><img src="{LOGO_SRC}" class="sidebar-logo"></div>',
                unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.85rem; font-weight:800; color:#0F2C59; text-transform:uppercase; margin-bottom:10px;'>Menu Principal</div>",
        unsafe_allow_html=True)
    menu = st.radio("", ["Analyse DGA", "Supervision & Données"], label_visibility="collapsed")

    st.markdown("<hr style='border-color: #E2E8F0; margin: 30px 0;'>", unsafe_allow_html=True)

    if st.button("Effacer l'historique"):
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            st.rerun()

    st.markdown(f"""
    <div style="background:white; border:1px solid #E2E8F0; border-radius:12px; padding:15px; text-align:center; margin-bottom:15px;">
        <div style="font-size:1.8rem; font-weight:900; color:#FF7A00;">{total_analyses}</div>
        <div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase;">Analyses Effectuées</div>
    </div>
    <div style="background:white; border:1px solid #E2E8F0; border-radius:12px; padding:15px; text-align:center;">
        <div style="font-size:1rem; font-weight:900; color:#0F2C59;">{str(last_diag)[:12]}</div>
        <div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase; margin-top:5px;">Dernier État</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# PAGE 1 : ANALYSE DGA
# ==============================
if menu == "Analyse DGA":
    st.markdown("""
    <div style="background:white; padding:1.5rem 2rem; border-radius:12px; border:1px solid #E2E8F0; display:flex; align-items:center; gap:15px; margin-bottom:2rem;">
        <img src="https://cdn-icons-png.flaticon.com/512/2092/2092663.png" width="30" style="filter: grayscale(100%) brightness(40%) sepia(100%) hue-rotate(200deg) saturate(300%);">
        <h2 style="margin:0; color:#0F2C59; font-weight:900; font-size:1.4rem;">POWERGUARD · SYSTÈME EXPERT</h2>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="dga-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #0F2C59; font-weight: 800; margin-bottom: 0.5rem;'>SAISIE DES GAZ (PPM)</h4>",
                    unsafe_allow_html=True)

        gases_list = ["H₂", "CH₄", "C₂H₆", "C₂H₄", "C₂H₂"]
        sensors_html = ""
        for name in gases_list:
            sensors_html += f'''
            <div class="gas-orb-wrapper">
                <div class="gas-orb">
                    <div class="gas-ring"></div>
                    <div class="gas-name">{name}</div>
                </div>
            </div>'''
        st.markdown(f'<div class="sensors-container">{sensors_html}</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            H2 = st.number_input("Hydrogène (H₂)", value=100.0, step=10.0)
            CH4 = st.number_input("Méthane (CH₄)", value=50.0, step=5.0)
        with col2:
            C2H6 = st.number_input("Éthane (C₂H₆)", value=20.0, step=5.0)
            C2H4 = st.number_input("Éthylène (C₂H₄)", value=10.0, step=2.0)
        with col3:
            C2H2 = st.number_input("Acétylène (C₂H₂)", value=5.0, step=1.0)
            st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
            run = st.button("PREDIRE")
        st.markdown('</div>', unsafe_allow_html=True)

    if run:
        with st.spinner("Analyse de l'échantillon..."):
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

                if "Arc" in fault or "High" in fault:
                    status_text, label_color = "ÉTAT CRITIQUE", "#DC2626"
                elif "Spark" in fault or "Middle" in fault:
                    status_text, label_color = "ANOMALIE DÉTECTÉE", "#FF7A00"
                else:
                    status_text, label_color = "ÉTAT NORMAL", "#0F2C59"

                st.markdown(f"""
                <div style="background:white; padding:2rem; border-radius:12px; text-align:center; border-left:8px solid {label_color}; box-shadow:0 10px 30px rgba(0,0,0,0.05); margin-bottom:2rem;">
                    <div style="font-size:1rem; font-weight:800; color:{label_color}; letter-spacing:1px; margin-bottom:10px;">{status_text}</div>
                    <div style="font-size:2.5rem; font-weight:900; color:#0F2C59; margin-bottom:10px;">{fault}</div>
                    <div style="display:inline-block; padding:8px 20px; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:50px; font-weight:700; color:#475569;">Fiabilité du modèle : {confidence:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(
                    "<h4 style='color: #0F2C59; font-weight: 800; margin-bottom: 1rem;'>PROBABILITÉS DES DÉFAUTS</h4>",
                    unsafe_allow_html=True)

                prob_df = pd.DataFrame({"Fault": encoder.classes_, "Prob": proba * 100}).sort_values("Prob",
                                                                                                     ascending=False)

                html_bars = '<div style="background:white; padding:1.5rem 2rem; border-radius:12px; border:1px solid #E2E8F0; box-shadow:0 4px 15px rgba(0,0,0,0.05);">'
                for _, row in prob_df.iterrows():
                    p = row["Prob"]
                    name = row["Fault"]
                    bg_color = "#FF7A00" if name == fault else "#0F2C59"
                    html_bars += f"""
                    <div style="margin-bottom: 15px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.95rem; font-weight:700; color:#0F2C59; margin-bottom:6px;">
                            <span>{name}</span><span>{p:.1f}%</span>
                        </div>
                        <div style="background:#E2E8F0; border-radius:30px; height:20px; overflow:hidden; border: 1px solid #CBD5E1;">
                            <div style="width:{p:.1f}%; background:{bg_color}; height:100%; border-radius:30px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);"></div>
                        </div>
                    </div>"""
                html_bars += '</div>'
                st.markdown(html_bars, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erreur d'inférence: {e}")

    # HISTORIQUE UNLIMITED SUR LA PAGE D'ACCUEIL
    st.markdown(
        "<h3 style='color: #0F2C59; font-weight: 800; margin-bottom: 1rem;'>REGISTRE DES OPÉRATIONS (ILLIMITÉ)</h3>",
        unsafe_allow_html=True)
    if os.path.exists(HISTORY_FILE):
        hist = pd.read_csv(HISTORY_FILE)
        if not hist.empty:
            hist_display = hist.iloc[::-1].reset_index(drop=True)
            hist_display.index = hist_display.index + 1
            st.markdown(f'<div class="table-wrapper">{hist_display.to_html(classes="custom-table", border=0)}</div>',
                        unsafe_allow_html=True)
        else:
            st.info("Le registre est actuellement vide.")
    else:
        st.info("Aucun journal existant. La première analyse le créera automatiquement.")

# ==============================
# PAGE 2 : SUPERVISION & DONNÉES
# ==============================
elif menu == "Supervision & Données":
    st.markdown("""
    <div style="background:white; padding:1.5rem 2rem; border-radius:12px; border:1px solid #E2E8F0; margin-bottom:2rem;">
        <h1 style="margin:0; color:#0F2C59; font-weight:900; font-size:1.8rem;">Supervision des Données</h1>
        <p style="margin:5px 0 0 0; color:#475569;">Registre centralisé de toutes les analyses DGA effectuées par PowerGuard.</p>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists(HISTORY_FILE):
        hist = pd.read_csv(HISTORY_FILE)
        if not hist.empty:
            total_tests = len(hist)
            last_fault = hist.iloc[-1]["Diagnosis"]
            critical_count = hist['Diagnosis'].str.contains('Arc|High', case=False).sum()

            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-card">
                    <div class="metric-value">{total_tests}</div>
                    <div class="metric-label">Analyses Effectuées</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#00A8E8;">{last_fault}</div>
                    <div class="metric-label">Dernier Constat</div>
                </div>
                <div class="metric-card" style="border-top-color:#DC2626;">
                    <div class="metric-value" style="color:#DC2626;">{critical_count}</div>
                    <div class="metric-label">Alertes Critiques Historiques</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                "<h3 style='color: #0F2C59; font-weight: 800; margin-bottom: 1rem;'>JOURNAL COMPLET (ILLIMITÉ)</h3>",
                unsafe_allow_html=True)

            recent_hist = hist.iloc[::-1].reset_index(drop=True)
            recent_hist.index = recent_hist.index + 1
            html_table = recent_hist.to_html(classes='custom-table', border=0)

            st.markdown(f"""
            <div class="table-wrapper">
                {html_table}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("La base de données est vierge. Aucune analyse enregistrée.")
    else:
        st.info("Aucun journal existant. Veuillez effectuer une analyse dans l'onglet 'Analyse DGA'.")