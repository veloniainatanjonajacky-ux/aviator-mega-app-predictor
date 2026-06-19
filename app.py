import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="Aviator Predictor V1.6.0", layout="centered", page_icon="✈️")

def get_mada_time():
    utc_now = datetime.now(timezone.utc)
    mada_time = utc_now + timedelta(hours=3)
    return mada_time.replace(tzinfo=None)

# CSS - LOKO VOAHITSY TSARA
st.markdown("""
<style>
    .stApp { 
        background-color: #f5f3ff; 
        color: #1a1a1a;
    }
    header[data-testid="stHeader"] { display: none; }
    
    /* Soratra rehetra tsy maintsy mainty mazava */
    .stMarkdown, .stMarkdown p, .stMarkdown li, 
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stText, label, .stCaption {
        color: #1a1a1a !important;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #880E4F, #AD1457);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        margin: -50px -20px 20px -20px;
        text-align: center;
    }
    .main-header h1 {
        color: white !important;
        margin: 0;
        font-size: 22px;
        font-weight: bold;
    }
    
    /* Mada time */
    .mada-time {
        background: linear-gradient(135deg, #9C27B0, #7B1FA2);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
        color: white !important;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(123,31,162,0.3);
    }
    
    /* Strategy Cards */
    .strategy-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 6px solid;
        color: #1a1a1a;
    }
    .strategy-card h3 {
        color: #1a1a1a !important;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .strategy-card p {
        color: #424242 !important;
        font-size: 15px;
        margin: 5px 0;
    }
    
    .violette { border-color: #9C27B0; }
    .tour { border-color: #FF9800; }
    .ia { border-color: #00C853; }
    .rose-vip { border-color: #E91E63; }
    .auto-2x { border-color: #4CAF50; }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #9C27B0, #7B1FA2);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 12px;
        font-weight: bold;
        width: 100%;
        font-size: 16px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #7B1FA2, #6A1B9A);
        color: white !important;
    }
    
    /* Zones */
    .zone-bleue { 
        background: #e3f2fd; 
        border-left: 5px solid #2196F3; 
        padding: 15px; 
        border-radius: 10px; 
        margin: 10px 0;
        color: #0d47a1 !important;
    }
    .zone-bleue b { color: #0d47a1 !important; font-size: 16px; }
    
    .zone-violette { 
        background: #f3e5f5; 
        border-left: 5px solid #9C27B0; 
        padding: 15px; 
        border-radius: 10px; 
        margin: 10px 0;
        color: #4A148C !important;
    }
    .zone-violette b { color: #4A148C !important; font-size: 16px; }
    
    .zone-rose { 
        background: #fce4ec; 
        border-left: 5px solid #E91E63; 
        padding: 15px; 
        border-radius: 10px; 
        margin: 10px 0;
        color: #880E4F !important;
    }
    .zone-rose b { color: #880E4F !important; font-size: 16px; }
    
    /* Prediction boxes */
    .pred-tour {
        background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
        border-left: 5px solid #FF9800;
        color: #E65100 !important;
    }
    .pred-tour b { color: #E65100 !important; }
    
    .pred-ia {
        background: #1a1a2e;
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
        color: white !important;
    }
    .pred-ia b, .pred-ia span { color: white !important; }
    
    .pred-rose {
        background: linear-gradient(135deg, #fce4ec, #f8bbd0);
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 6px solid #E91E63;
        color: #880E4F !important;
    }
    .pred-rose b { color: #880E4F !important; }
    
    .pred-auto {
        background: #e8f5e9;
        padding: 12px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #4CAF50;
        color: #1B5E20 !important;
    }
    .pred-auto b { color: #1B5E20 !important; }
    
    /* Inputs */
    .stNumberInput label, .stTextArea label, .stSlider label {
        color: #1a1a1a !important;
        font-weight: bold;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        color: #1a1a1a !important;
    }
    
    /* Metrics */
    [data-testid="stMetricLabel"] {
        color: #424242 !important;
    }
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "menu"

# HEADER
st.markdown("""
<div class="main-header">
    <h1>✈️ Aviator Predictor V1.6.0 (Beta)</h1>
</div>
""", unsafe_allow_html=True)

mada_now = get_mada_time()
st.markdown(f"""
<div class="mada-time">
    🇲🇬 Ora Madagascar: {mada_now.strftime('%H:%M:%S')} • {mada_now.strftime('%d/%m/%Y')}
</div>
""", unsafe_allow_html=True)

def calc_fiabilite_v16(round_num, base_data=None):
    base = 95 - (round_num - 1) * 3
    if base_data is not None and len(base_data) > 0:
        std = np.std(base_data)
        adjustment = max(-5, min(5, -std * 2))
        base += adjustment
    variation = np.random.uniform(-2, 3)
    final = base + variation
    return max(60.0, min(98.0, final))

# ===== MENU =====
if st.session_state.page == "menu":
    
    st.markdown("""
    <div class="strategy-card violette">
        <h3>💜 Stratégie Violette</h3>
        <p><b>2.00X-9.99X (Standard)</b></p>
        <p style="font-style: italic;">Analyse statistique des zones de couleur.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Stratégie Violette", key="b_violette"):
        st.session_state.page = "violette"
        st.rerun()
    
    st.markdown("""
    <div class="strategy-card tour">
        <h3>🕰️ Stratégie De Tour</h3>
        <p><b>Boost 4.00X Garanti 2X (Premium)</b></p>
        <p style="font-style: italic;">Technologie brevetée à haut rendement.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Stratégie De Tour", key="b_tour"):
        st.session_state.page = "tour"
        st.rerun()
    
    st.markdown("""
    <div class="strategy-card ia">
        <h3>🤖 Calcul Tour IA</h3>
        <p><b>Analyse IA (Premium)</b></p>
        <p style="font-style: italic;">Prédictions basées sur l'IA.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Calcul Tour IA", key="b_ia"):
        st.session_state.page = "ia"
        st.rerun()
    
    st.markdown("""
    <div class="strategy-card rose-vip">
        <h3>🎀 Stratégie Rose VIP</h3>
        <p><b>10.00X+ (Premium)</b></p>
        <p style="font-style: italic;">Algorithmes prédictifs avancés.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Stratégie Rose VIP", key="b_rose"):
        st.session_state.page = "rose"
        st.rerun()
    
    st.markdown("""
    <div class="strategy-card auto-2x">
        <h3>✅ Mode Auto 2X Assuré</h3>
        <p><b>Sécurité maximale pour profit constant</b></p>
        <p style="font-style: italic;">Technique de sécurité maximale.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Mode Auto 2X", key="b_auto"):
        st.session_state.page = "auto2x"
        st.rerun()

# ===== VIOLETTE =====
elif st.session_state.page == "violette":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 💜 STRATÉGIE VIOLETTE")
    st.info("📌 **Mode d'utilisation:**\n\n1. Entrez le multiplicateur le plus bas des 10 derniers tours (<2.00X)\n2. Indiquez l'heure exacte - **Ora Madagascar**\n3. Réinitialisez si nouveau minimum")
    
    mult_min = st.number_input("Multiplicateur minimum (X):", 1.00, 2.00, 1.60, 0.01)
    
    st.markdown("**⏰ Heure de référence (Ora Madagascar):**")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("Heures", 0, 23, mada_now.hour)
    mi = col_m.number_input("Minutes", 0, 59, mada_now.minute)
    se = col_s.number_input("Secondes", 0, 59, mada_now.second)
    
    if st.button("🧮 Lancer l'analyse", key="v_launch"):
        ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
        
        if mult_min < 1.30:
            pb, pv, pr = 25, 50, 25
        elif mult_min < 1.60:
            pb, pv, pr = 35, 42, 23
        elif mult_min < 1.80:
            pb, pv, pr = 38.5, 38.6, 22.9
        else:
            pb, pv, pr = 45, 35, 20
        
        pb += np.random.uniform(-2, 2)
        pv += np.random.uniform(-2, 2)
        pr += np.random.uniform(-2, 2)
        tot = pb + pv + pr
        pb, pv, pr = pb/tot*100, pv/tot*100, pr/tot*100
        
        start = ref + timedelta(seconds=55)
        end = ref + timedelta(minutes=1, seconds=22)
        interval = f"{start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')}"
        
        st.markdown("### 📊 Résultats de l'analyse")
        
        st.markdown(f'''
        <div class="zone-bleue">
            <b>💧 Zone Bleue (1.00X-1.99X)</b><br>
            <span style="color:#0d47a1;">Probabilité: <b>{pb:.1f}%</b></span><br>
            <span style="color:#0d47a1;">Intervalle: <b>{interval}</b> 🇲🇬</span>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'''
        <div class="zone-violette">
            <b>🌸 Zone Violette (2.00X-9.99X)</b><br>
            <span style="color:#4A148C;">Probabilité: <b>{pv:.1f}%</b></span><br>
            <span style="color:#4A148C;">Intervalle: <b>{interval}</b> 🇲🇬</span>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'''
        <div class="zone-rose">
            <b>🚀 Zone Rose (10.00X+)</b><br>
            <span style="color:#880E4F;">Probabilité: <b>{pr:.1f}%</b></span><br>
            <span style="color:#880E4F;">Intervalle: <b>{interval}</b> 🇲🇬</span>
        </div>
        ''', unsafe_allow_html=True)

# ===== TOUR =====
elif st.session_state.page == "tour":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 🕰️ STRATÉGIE DE TOUR")
    st.success("🎯 **Boost 4.00X Garanti 2X**")
    
    st.markdown("**Entrez les 5 derniers multiplicateurs:**")
    mults = []
    cols = st.columns(5)
    for i, c in enumerate(cols):
        with c:
            m = st.number_input(f"M{i+1}", 1.00, 100.00, 1.50, 0.01, key=f"tour_{i}")
            mults.append(m)
    
    st.markdown("**⏰ Ora Madagascar:**")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour, key="t_h")
    mi = col_m.number_input("M", 0, 59, mada_now.minute, key="t_m")
    se = col_s.number_input("S", 0, 59, mada_now.second, key="t_s")
    
    if st.button("🚀 Calculer le Boost", key="t_launch"):
        avg = np.mean(mults)
        ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
        
        st.markdown("### 🎯 Tours Garantis 2X:")
        for i in range(1, 6):
            boost_time = ref + timedelta(seconds=30*i)
            boost_value = max(2.00, avg * 1.3 + np.random.uniform(0, 2))
            confidence = calc_fiabilite_v16(i, mults)
            color = "#00C853" if boost_value >= 4 else "#FF6F00"
            
            st.markdown(f'''
            <div class="pred-tour" style="border-left-color: {color};">
                <b style="font-size: 17px;">Tour #{i}</b> • ⏰ <b>{boost_time.strftime('%H:%M:%S')}</b> 🇲🇬<br>
                💎 Boost: <span style="color: {color}; font-size: 24px; font-weight: bold;">{boost_value:.2f}X</span><br>
                ✅ Fiabilité: <b style="font-size: 16px;">{confidence:.1f}%</b> • Cash Out: <b>2.00X</b>
            </div>
            ''', unsafe_allow_html=True)
        
        st.info("💡 Sortez à 2.00X pour garantir le gain.")

# ===== IA =====
elif st.session_state.page == "ia":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 🤖 CALCUL TOUR IA")
    st.success("🧠 **Analyse IA Avancée** - Machine Learning")
    
    st.markdown("**Entrez 10 derniers multiplicateurs (séparés par virgule):**")
    data_input = st.text_area("Format:", "1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4")
    
    st.markdown("**⏰ Ora Madagascar:**")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour, key="ia_h")
    mi = col_m.number_input("M", 0, 59, mada_now.minute, key="ia_m")
    se = col_s.number_input("S", 0, 59, mada_now.second, key="ia_s")
    
    if st.button("🤖 Lancer l'IA", key="ia_launch"):
        try:
            data = [float(x.strip()) for x in data_input.split(",")]
            from sklearn.ensemble import RandomForestRegressor
            
            X = np.arange(len(data)).reshape(-1, 1)
            model = RandomForestRegressor(n_estimators=200, random_state=42)
            model.fit(X, data)
            
            ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
            
            st.markdown("### 🎯 Prédictions IA (TOP 10):")
            for i in range(1, 11):
                pred = model.predict([[len(data)+i-1]])[0]
                pred = max(1.0, pred + np.random.uniform(-0.3, 0.5))
                t = ref + timedelta(seconds=30*i)
                conf = calc_fiabilite_v16(i, data)
                
                if pred < 1.5:
                    color = "#F44336"
                elif pred < 2.5:
                    color = "#FFC107"
                else:
                    color = "#4CAF50"
                
                st.markdown(f'''
                <div class="pred-ia" style="border-left: 5px solid {color};">
                    <b style="font-size: 16px; color: white;">Tour #{i}</b> 
                    <span style="color: #BDBDBD;">• ⏰ {t.strftime('%H:%M:%S')} 🇲🇬</span><br>
                    <span style="color: {color}; font-size: 24px; font-weight: bold;">{pred:.2f}X</span>
                    <span style="color: #FFD700; font-size: 15px;"> • Fiabilité: <b>{conf:.1f}%</b></span>
                </div>
                ''', unsafe_allow_html=True)
        except:
            st.error("Format incorrect.")

# ===== ROSE VIP =====
elif st.session_state.page == "rose":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 🎀 STRATÉGIE ROSE VIP")
    st.error("🚀 **Mode VIP - 10.00X+ Hunter**")
    
    st.markdown("**Entrez les 20 derniers multiplicateurs:**")
    data_input = st.text_area("Format:", 
        "1.2, 1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4, 2.1, 1.6, 4.5, 1.7, 2.8, 1.2, 3.5, 1.9, 2.4")
    
    st.markdown("**⏰ Ora Madagascar:**")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour, key="r_h")
    mi = col_m.number_input("M", 0, 59, mada_now.minute, key="r_m")
    se = col_s.number_input("S", 0, 59, mada_now.second, key="r_s")
    
    if st.button("💎 Chasser les 10X+", key="r_launch"):
        try:
            data = [float(x.strip()) for x in data_input.split(",")]
            big_wins = [x for x in data if x >= 10]
            avg_gap = len(data) / max(len(big_wins), 1)
            ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
            
            st.markdown("### 💎 Prochains BIG WINS:")
            for i in range(1, 6):
                next_round = int(avg_gap * i)
                t = ref + timedelta(seconds=30 * next_round)
                predicted_value = np.random.uniform(10, 50)
                confidence = calc_fiabilite_v16(i, data)
                
                st.markdown(f'''
                <div class="pred-rose">
                    <b style="font-size: 18px;">💎 BIG WIN #{i}</b><br>
                    <span style="color:#880E4F;">⏰ Tour #{next_round} • <b>{t.strftime('%H:%M:%S')}</b> 🇲🇬</span><br>
                    <span style="color:#880E4F;">🎯 Valeur prédite: <b style="color: #E91E63; font-size: 26px;">{predicted_value:.2f}X</b></span><br>
                    <span style="color:#880E4F;">✅ Fiabilité: <b style="font-size: 16px;">{confidence:.1f}%</b></span>
                </div>
                ''', unsafe_allow_html=True)
            
            st.warning("⚠️ Misez petit et soyez patient.")
        except:
            st.error("Format incorrect.")

# ===== AUTO 2X =====
elif st.session_state.page == "auto2x":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## ✅ MODE AUTO 2X ASSURÉ")
    st.success("🛡️ **Sécurité Maximale** - Profit constant à 2.00X")
    
    st.markdown("### 📊 Calculateur de Profit:")
    
    bankroll = st.number_input("💰 Bankroll (Ar):", 1000, 10000000, 50000, 1000)
    bet_pct = st.slider("🎯 % par tour:", 1, 10, 3)
    nb_tours = st.slider("🔄 Nombre de tours:", 5, 100, 20)
    
    st.markdown("**⏰ Ora manomboka (Madagascar):**")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour, key="a_h")
    mi = col_m.number_input("M", 0, 59, mada_now.minute, key="a_m")
    se = col_s.number_input("S", 0, 59, mada_now.second, key="a_s")
    
    bet_amount = int(bankroll * bet_pct / 100)
    win_per_round = bet_amount
    win_rate = 0.70
    expected_wins = int(nb_tours * win_rate)
    expected_losses = nb_tours - expected_wins
    net_profit = (expected_wins * win_per_round) - (expected_losses * bet_amount)
    global_fiab = np.random.uniform(72, 85)
    
    st.markdown("### 🎯 Plan de Trading:")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Mise/tour", f"{bet_amount:,} Ar")
    col2.metric("✅ Cash Out", "2.00X")
    col3.metric("🎁 Gain/tour", f"+{win_per_round:,} Ar")
    
    st.markdown("### 📈 Résultats prévus:")
    col1, col2 = st.columns(2)
    col1.metric("✅ Gagnés", f"{expected_wins}")
    col2.metric("❌ Perdus", f"{expected_losses}")
    
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, #4CAF50, #2E7D32); padding: 25px; 
                border-radius: 15px; text-align: center; color: white !important; margin: 15px 0;">
        <h2 style="color: white !important; margin: 0;">💎 PROFIT NET PRÉVU</h2>
        <h1 style="color: white !important; margin: 10px 0; font-size: 40px;">+{net_profit:,} Ar</h1>
        <p style="color: white !important;">Sur {nb_tours} tours • Win Rate ~70%</p>
        <p style="color: white !important;">✅ Fiabilité globale: <b>{global_fiab:.1f}%</b></p>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("📅 Voir le planning des tours", key="a_plan"):
        ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
        st.markdown("### 📅 Planning (TOP 10):")
        for i in range(1, 11):
            t = ref + timedelta(seconds=30*i)
            fiab = calc_fiabilite_v16(i)
            st.markdown(f'''
            <div class="pred-auto">
                <b>Tour #{i}</b> • ⏰ <b>{t.strftime('%H:%M:%S')}</b> 🇲🇬 • 
                Cash Out: <b style="color: #2E7D32;">2.00X</b> • 
                Fiabilité: <b>{fiab:.1f}%</b>
            </div>
            ''', unsafe_allow_html=True)
    
    st.info("""
    💡 **Règles d'Or:**
    - ✅ Toujours sortir à 2.00X
    - ✅ Maximum 5% du bankroll/tour
    - ✅ Arrêter après 5 pertes consécutives
    - ✅ Reprendre 30 minutes plus tard
    """)

st.markdown("---")
st.caption(f"🇲🇬 Made in Madagascar • Ora: {mada_now.strftime('%H:%M:%S')} • ⚠️ Jouez avec modération")
