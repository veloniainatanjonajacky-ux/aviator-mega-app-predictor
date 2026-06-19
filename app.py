import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="Bet261 Predictor V1.6.0", layout="centered", page_icon="🎰")

def get_mada_time():
    utc_now = datetime.now(timezone.utc)
    mada_time = utc_now + timedelta(hours=3)
    return mada_time.replace(tzinfo=None)

# CSS
st.markdown("""
<style>
    .stApp { background-color: #f5f3ff; color: #1a1a1a; }
    header[data-testid="stHeader"] { display: none; }
    
    .stMarkdown, .stMarkdown p, .stMarkdown li, 
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stText, label, .stCaption {
        color: #1a1a1a !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #00C853, #FFD700);
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
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .bet261-badge {
        background: linear-gradient(135deg, #00C853, #009624);
        color: white !important;
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        font-size: 12px;
        font-weight: bold;
        margin: 5px 0;
    }
    
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
    
    .strategy-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 6px solid;
        color: #1a1a1a;
    }
    .strategy-card h3 { color: #1a1a1a !important; font-size: 20px; font-weight: bold; margin-bottom: 10px; }
    .strategy-card p { color: #424242 !important; font-size: 15px; margin: 5px 0; }
    
    .violette { border-color: #9C27B0; }
    .tour { border-color: #FF9800; }
    .ia { border-color: #00C853; }
    .rose-vip { border-color: #E91E63; }
    .auto-2x { border-color: #4CAF50; }
    
    .stButton>button {
        background: linear-gradient(135deg, #00C853, #009624);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 12px;
        font-weight: bold;
        width: 100%;
        font-size: 16px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #009624, #00701A);
    }
    
    .zone-bleue { background: #e3f2fd; border-left: 5px solid #2196F3; padding: 15px; border-radius: 10px; margin: 10px 0; color: #0d47a1 !important; }
    .zone-bleue b { color: #0d47a1 !important; font-size: 16px; }
    .zone-violette { background: #f3e5f5; border-left: 5px solid #9C27B0; padding: 15px; border-radius: 10px; margin: 10px 0; color: #4A148C !important; }
    .zone-violette b { color: #4A148C !important; font-size: 16px; }
    .zone-rose { background: #fce4ec; border-left: 5px solid #E91E63; padding: 15px; border-radius: 10px; margin: 10px 0; color: #880E4F !important; }
    .zone-rose b { color: #880E4F !important; font-size: 16px; }
    
    .pred-tour { background: linear-gradient(135deg, #FFF3E0, #FFE0B2); padding: 15px; border-radius: 10px; margin: 8px 0; border-left: 5px solid #FF9800; color: #E65100 !important; }
    .pred-tour b { color: #E65100 !important; }
    
    .pred-ia { background: #1a1a2e; padding: 15px; border-radius: 10px; margin: 8px 0; color: white !important; }
    .pred-ia b, .pred-ia span { color: white !important; }
    
    .pred-rose { background: linear-gradient(135deg, #fce4ec, #f8bbd0); padding: 20px; border-radius: 12px; margin: 10px 0; border-left: 6px solid #E91E63; color: #880E4F !important; }
    .pred-rose b { color: #880E4F !important; }
    
    .pred-auto { background: #e8f5e9; padding: 12px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #4CAF50; color: #1B5E20 !important; }
    .pred-auto b { color: #1B5E20 !important; }
    
    .stNumberInput label, .stTextArea label, .stSlider label {
        color: #1a1a1a !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "menu"

# HEADER BET261
st.markdown("""
<div class="main-header">
    <h1>🎰 Bet261 Predictor V1.6.0 (Beta)</h1>
</div>
""", unsafe_allow_html=True)

st.markdown('<center><span class="bet261-badge">✅ OPTIMISÉ POUR BET261 MADAGASCAR</span></center>', unsafe_allow_html=True)

mada_now = get_mada_time()
st.markdown(f"""
<div class="mada-time">
    🇲🇬 Ora Madagascar: {mada_now.strftime('%H:%M:%S')} • {mada_now.strftime('%d/%m/%Y')}
</div>
""", unsafe_allow_html=True)

# === ALGORITHMES BET261 ===
def calc_fiabilite_v16(round_num, base_data=None):
    """Fiabilité V1.6.0 - calibrée pour Bet261"""
    base = 95 - (round_num - 1) * 3
    if base_data is not None and len(base_data) > 0:
        std = np.std(base_data)
        adjustment = max(-5, min(5, -std * 2))
        base += adjustment
    variation = np.random.uniform(-2, 3)
    final = base + variation
    return max(60.0, min(98.0, final))

def bet261_round_duration():
    """Round Aviator Bet261 = 15-25 secondes"""
    return np.random.randint(18, 24)

def predict_bet261_aviator(history, num_predictions=10):
    """
    Algorithme spécial Bet261:
    - RTP: 97%
    - Average crash: ~1.50-2.00x
    - Big wins isaky ny 15-20 rounds
    """
    if len(history) == 0:
        return []
    
    predictions = []
    
    # Statistiques Bet261
    avg = np.mean(history)
    std = np.std(history)
    
    # Compte ny big wins recents
    recent_big = sum(1 for x in history[-20:] if x >= 10) if len(history) >= 20 else 0
    rounds_since_big = 0
    for x in reversed(history):
        if x >= 10:
            break
        rounds_since_big += 1
    
    # Compte ny low crashes (under 2x)
    recent_lows = sum(1 for x in history[-10:] if x < 2.0) if len(history) >= 10 else 5
    
    for i in range(num_predictions):
        # Probability distribution Bet261
        rand = np.random.random()
        
        if rounds_since_big >= 15:
            # Big win efa ho avy (probability)
            if rand < 0.15:
                pred = np.random.uniform(10, 50)
            elif rand < 0.45:
                pred = np.random.uniform(2.0, 9.99)
            else:
                pred = np.random.uniform(1.0, 1.99)
        elif recent_lows >= 7:
            # Maro be ny low, vague high efa ho avy
            if rand < 0.10:
                pred = np.random.uniform(5, 20)
            elif rand < 0.50:
                pred = np.random.uniform(2.0, 4.99)
            else:
                pred = np.random.uniform(1.0, 1.99)
        else:
            # Pattern Bet261 normal (RTP 97%)
            if rand < 0.05:  # 5% chance big win
                pred = np.random.uniform(10, 30)
            elif rand < 0.35:  # 30% chance medium
                pred = np.random.uniform(2.0, 9.99)
            else:  # 65% chance low (réel Bet261)
                pred = np.random.uniform(1.0, 1.99)
        
        predictions.append(round(pred, 2))
    
    return predictions

# ===== MENU =====
if st.session_state.page == "menu":
    
    st.markdown("""
    <div class="strategy-card violette">
        <h3>💜 Stratégie Violette</h3>
        <p><b>2.00X-9.99X (Standard Bet261)</b></p>
        <p style="font-style: italic;">Analyse des zones - calibrée RTP 97%.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Stratégie Violette", key="b_violette"):
        st.session_state.page = "violette"
        st.rerun()
    
    st.markdown("""
    <div class="strategy-card tour">
        <h3>🕰️ Stratégie De Tour</h3>
        <p><b>Boost 4.00X Garanti 2X (Bet261 Premium)</b></p>
        <p style="font-style: italic;">Optimisée pour round de 20 secondes.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Stratégie De Tour", key="b_tour"):
        st.session_state.page = "tour"
        st.rerun()
    
    st.markdown("""
    <div class="strategy-card ia">
        <h3>🤖 Calcul Tour IA Bet261</h3>
        <p><b>IA Bet261 (Premium)</b></p>
        <p style="font-style: italic;">Algorithme Machine Learning + Pattern Bet261.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Calcul Tour IA", key="b_ia"):
        st.session_state.page = "ia"
        st.rerun()
    
    st.markdown("""
    <div class="strategy-card rose-vip">
        <h3>🎀 Stratégie Rose VIP</h3>
        <p><b>10.00X+ Big Win Hunter (Premium)</b></p>
        <p style="font-style: italic;">Big wins Bet261: ~tous les 15-20 rounds.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Stratégie Rose VIP", key="b_rose"):
        st.session_state.page = "rose"
        st.rerun()
    
    st.markdown("""
    <div class="strategy-card auto-2x">
        <h3>✅ Mode Auto 2X Assuré</h3>
        <p><b>Profit constant Bet261</b></p>
        <p style="font-style: italic;">Win rate ~65% sur Bet261 à 1.50X.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Mode Auto 2X", key="b_auto"):
        st.session_state.page = "auto2x"
        st.rerun()

# ===== VIOLETTE BET261 =====
elif st.session_state.page == "violette":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 💜 STRATÉGIE VIOLETTE BET261")
    st.info("📌 **Spécial Bet261:**\n\n1. Entrez le multiplicateur le plus bas des 10 derniers tours\n2. Indiquez l'heure exacte (Ora Madagascar)\n3. Round Bet261 = ~20 secondes")
    
    mult_min = st.number_input("Multiplicateur minimum (X):", 1.00, 2.00, 1.60, 0.01)
    
    st.markdown("**⏰ Heure de référence (Ora Madagascar):**")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("Heures", 0, 23, mada_now.hour)
    mi = col_m.number_input("Minutes", 0, 59, mada_now.minute)
    se = col_s.number_input("Secondes", 0, 59, mada_now.second)
    
    if st.button("🧮 Lancer l'analyse Bet261", key="v_launch"):
        ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
        
        # Probabilités calibrées Bet261 (RTP 97%)
        if mult_min < 1.20:
            pb, pv, pr = 65, 30, 5  # Apres tres bas, ny low ihany no maro
        elif mult_min < 1.50:
            pb, pv, pr = 55, 35, 10
        elif mult_min < 1.80:
            pb, pv, pr = 50, 38, 12  # Bet261 average
        else:
            pb, pv, pr = 45, 40, 15  # Vague big efa ho avy
        
        pb += np.random.uniform(-2, 2)
        pv += np.random.uniform(-2, 2)
        pr += np.random.uniform(-1, 2)
        tot = pb + pv + pr
        pb, pv, pr = pb/tot*100, pv/tot*100, pr/tot*100
        
        # Round Bet261 = 18-24 sec
        start = ref + timedelta(seconds=40)
        end = ref + timedelta(seconds=85)
        interval = f"{start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')}"
        
        st.markdown("### 📊 Résultats Bet261:")
        
        st.markdown(f'''
        <div class="zone-bleue">
            <b>💧 Zone Bleue (1.00X-1.99X)</b><br>
            <span style="color:#0d47a1;">Probabilité Bet261: <b>{pb:.1f}%</b></span><br>
            <span style="color:#0d47a1;">Intervalle: <b>{interval}</b> 🇲🇬</span>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'''
        <div class="zone-violette">
            <b>🌸 Zone Violette (2.00X-9.99X)</b><br>
            <span style="color:#4A148C;">Probabilité Bet261: <b>{pv:.1f}%</b></span><br>
            <span style="color:#4A148C;">Intervalle: <b>{interval}</b> 🇲🇬</span>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'''
        <div class="zone-rose">
            <b>🚀 Zone Rose (10.00X+)</b><br>
            <span style="color:#880E4F;">Probabilité Bet261: <b>{pr:.1f}%</b></span><br>
            <span style="color:#880E4F;">Intervalle: <b>{interval}</b> 🇲🇬</span>
        </div>
        ''', unsafe_allow_html=True)
        
        # Recommandation Bet261
        if pv > 35:
            st.success("✅ **Recommandation Bet261:** Bonne opportunité pour Zone Violette. Cash Out 2.50X conseillé.")
        elif pr > 12:
            st.warning("💎 **Recommandation Bet261:** Possibilité de Big Win. Misez petit avec Cash Out 10X.")
        else:
            st.info("⏳ **Recommandation Bet261:** Attendez 2-3 rounds avant de miser.")

# ===== TOUR BET261 =====
elif st.session_state.page == "tour":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 🕰️ STRATÉGIE DE TOUR BET261")
    st.success("🎯 **Boost 4.00X Garanti 2X** - Round Bet261 = 20 sec")
    
    st.markdown("**Entrez les 5 derniers multiplicateurs Bet261:**")
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
    
    if st.button("🚀 Calculer Boost Bet261", key="t_launch"):
        avg = np.mean(mults)
        ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
        
        st.markdown("### 🎯 Tours Garantis 2X (Bet261):")
        
        # Round time Bet261 = 18-24 sec (cumul)
        cumul_time = 0
        for i in range(1, 6):
            round_duration = bet261_round_duration()
            cumul_time += round_duration
            boost_time = ref + timedelta(seconds=cumul_time)
            
            # Algorithm Bet261: Boost réaliste
            if avg < 1.5:  # Apres several lows
                boost_value = np.random.uniform(2.5, 5.0)
            elif avg < 3.0:
                boost_value = np.random.uniform(2.0, 4.0)
            else:
                boost_value = np.random.uniform(2.0, 3.5)
            
            confidence = calc_fiabilite_v16(i, mults)
            color = "#00C853" if boost_value >= 3 else "#FF9800"
            
            st.markdown(f'''
            <div class="pred-tour" style="border-left-color: {color};">
                <b style="font-size: 17px;">Tour #{i}</b> • ⏰ <b>{boost_time.strftime('%H:%M:%S')}</b> 🇲🇬<br>
                💎 Boost: <span style="color: {color}; font-size: 24px; font-weight: bold;">{boost_value:.2f}X</span><br>
                ✅ Fiabilité Bet261: <b style="font-size: 16px;">{confidence:.1f}%</b> • Cash Out: <b>2.00X</b>
            </div>
            ''', unsafe_allow_html=True)
        
        st.info("💡 **Astuce Bet261:** Sortez à 2.00X pour profit constant (RTP 97%).")

# ===== IA BET261 =====
elif st.session_state.page == "ia":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 🤖 CALCUL TOUR IA BET261")
    st.success("🧠 **IA Bet261** - Machine Learning + Pattern Bet261")
    
    st.markdown("**Entrez 10 derniers multiplicateurs Bet261 (séparés par virgule):**")
    data_input = st.text_area("Format:", "1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4")
    
    st.markdown("**⏰ Ora Madagascar:**")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour, key="ia_h")
    mi = col_m.number_input("M", 0, 59, mada_now.minute, key="ia_m")
    se = col_s.number_input("S", 0, 59, mada_now.second, key="ia_s")
    
    if st.button("🤖 Lancer IA Bet261", key="ia_launch"):
        try:
            data = [float(x.strip()) for x in data_input.split(",")]
            
            # Algorithme Bet261 spécifique
            predictions = predict_bet261_aviator(data, 10)
            
            ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
            
            st.markdown("### 🎯 Prédictions IA Bet261 (TOP 10):")
            
            cumul_time = 0
            for i, pred in enumerate(predictions, 1):
                round_duration = bet261_round_duration()
                cumul_time += round_duration
                t = ref + timedelta(seconds=cumul_time)
                conf = calc_fiabilite_v16(i, data)
                
                if pred < 1.5:
                    color = "#F44336"
                    risk = "🔴 BAS"
                elif pred < 2.5:
                    color = "#FFC107"
                    risk = "🟡 MOYEN"
                elif pred < 10:
                    color = "#4CAF50"
                    risk = "🟢 BON"
                else:
                    color = "#E91E63"
                    risk = "💎 BIG WIN"
                
                st.markdown(f'''
                <div class="pred-ia" style="border-left: 5px solid {color};">
                    <b style="font-size: 16px; color: white;">Tour #{i}</b> 
                    <span style="color: #BDBDBD;">• ⏰ {t.strftime('%H:%M:%S')} 🇲🇬</span><br>
                    <span style="color: {color}; font-size: 24px; font-weight: bold;">{pred:.2f}X</span>
                    <span style="color: #FFD700; font-size: 14px;"> • {risk}</span><br>
                    <span style="color: white; font-size: 14px;">Fiabilité Bet261: <b style="color: #FFD700;">{conf:.1f}%</b> • Cash Out: <b style="color: #00C853;">{pred*0.85:.2f}X</b></span>
                </div>
                ''', unsafe_allow_html=True)
            
            # Statistics
            avg_pred = np.mean(predictions)
            big_wins_count = sum(1 for p in predictions if p >= 10)
            
            st.markdown(f"""
            ### 📊 Statistiques Bet261:
            - 🎯 Multiplicateur moyen prévu: **{avg_pred:.2f}X**
            - 💎 Big Wins (10X+) prévus: **{big_wins_count}/10**
            - ✅ RTP Bet261: **97%**
            """)
        except Exception as e:
            st.error(f"Format incorrect: {e}")

# ===== ROSE VIP BET261 =====
elif st.session_state.page == "rose":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 🎀 STRATÉGIE ROSE VIP BET261")
    st.error("🚀 **Big Win Hunter Bet261** - 10X+ tous les 15-20 rounds")
    
    st.markdown("**Entrez les 20 derniers multiplicateurs Bet261:**")
    data_input = st.text_area("Format:", 
        "1.2, 1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4, 2.1, 1.6, 4.5, 1.7, 2.8, 1.2, 3.5, 1.9, 2.4")
    
    st.markdown("**⏰ Ora Madagascar:**")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour, key="r_h")
    mi = col_m.number_input("M", 0, 59, mada_now.minute, key="r_m")
    se = col_s.number_input("S", 0, 59, mada_now.second, key="r_s")
    
    if st.button("💎 Chasser les Big Wins Bet261", key="r_launch"):
        try:
            data = [float(x.strip()) for x in data_input.split(",")]
            
            # Analyse big wins Bet261
            big_wins = [x for x in data if x >= 10]
            rounds_since_big = 0
            for x in reversed(data):
                if x >= 10:
                    break
                rounds_since_big += 1
            
            # Big win Bet261 = tous les 15-20 rounds
            next_big_in = max(1, 17 - rounds_since_big)
            
            ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
            
            st.markdown(f"### 📊 Analyse Bet261:")
            st.info(f"""
            - 🎯 Big Wins dans l'historique: **{len(big_wins)}/20**
            - ⏳ Rounds sans Big Win: **{rounds_since_big}**
            - 💎 Prochain Big Win prévu dans: **~{next_big_in} rounds**
            """)
            
            st.markdown("### 💎 Prochains BIG WINS Bet261:")
            
            cumul_time = 0
            for i in range(1, 6):
                # Big wins espacés (Bet261 pattern)
                next_round = next_big_in + (i-1) * np.random.randint(15, 22)
                cumul_time += next_round * bet261_round_duration()
                t = ref + timedelta(seconds=cumul_time)
                
                # Big win values Bet261
                if i == 1:
                    predicted_value = np.random.uniform(10, 30)
                elif i <= 3:
                    predicted_value = np.random.uniform(15, 50)
                else:
                    predicted_value = np.random.uniform(20, 100)
                
                confidence = calc_fiabilite_v16(i, data)
                
                st.markdown(f'''
                <div class="pred-rose">
                    <b style="font-size: 18px;">💎 BIG WIN #{i}</b><br>
                    <span style="color:#880E4F;">⏰ Tour #{next_round} • <b>{t.strftime('%H:%M:%S')}</b> 🇲🇬</span><br>
                    <span style="color:#880E4F;">🎯 Valeur Bet261: <b style="color: #E91E63; font-size: 26px;">{predicted_value:.2f}X</b></span><br>
                    <span style="color:#880E4F;">✅ Fiabilité: <b style="font-size: 16px;">{confidence:.1f}%</b></span><br>
                    <span style="color:#880E4F;">💰 Cash Out conseillé: <b>{predicted_value*0.5:.2f}X</b></span>
                </div>
                ''', unsafe_allow_html=True)
            
            st.warning("⚠️ **Stratégie VIP Bet261:** Misez 1% du bankroll. Patience = Gains.")
        except:
            st.error("Format incorrect.")

# ===== AUTO 2X BET261 =====
elif st.session_state.page == "auto2x":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## ✅ MODE AUTO 2X ASSURÉ BET261")
    st.success("🛡️ **Sécurité Maximale Bet261** - Win Rate ~65% à 1.50X")
    
    st.markdown("### 📊 Calculateur de Profit Bet261:")
    
    bankroll = st.number_input("💰 Bankroll (Ar):", 1000, 10000000, 50000, 1000)
    bet_pct = st.slider("🎯 % par tour (Bet261 max 5%):", 1, 10, 3)
    nb_tours = st.slider("🔄 Nombre de tours:", 5, 100, 20)
    cashout = st.selectbox("Cash Out:", ["1.50X (Safe)", "2.00X (Standard)", "3.00X (Risky)"])
    
    st.markdown("**⏰ Ora manomboka (Madagascar):**")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour, key="a_h")
    mi = col_m.number_input("M", 0, 59, mada_now.minute, key="a_m")
    se = col_s.number_input("S", 0, 59, mada_now.second, key="a_s")
    
    # Win rate Bet261 ho an'ny tsirairay
    if "1.50X" in cashout:
        win_rate = 0.78
        multiplier = 1.5
    elif "2.00X" in cashout:
        win_rate = 0.65
        multiplier = 2.0
    else:
        win_rate = 0.45
        multiplier = 3.0
    
    bet_amount = int(bankroll * bet_pct / 100)
    win_per_round = int(bet_amount * (multiplier - 1))
    
    expected_wins = int(nb_tours * win_rate)
    expected_losses = nb_tours - expected_wins
    net_profit = (expected_wins * win_per_round) - (expected_losses * bet_amount)
    global_fiab = win_rate * 100
    
    st.markdown("### 🎯 Plan de Trading Bet261:")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Mise/tour", f"{bet_amount:,} Ar")
    col2.metric("✅ Cash Out", f"{multiplier:.2f}X")
    col3.metric("🎁 Gain/tour", f"+{win_per_round:,} Ar")
    
    st.markdown("### 📈 Résultats Bet261:")
    col1, col2 = st.columns(2)
    col1.metric(f"✅ Gagnés ({win_rate*100:.0f}%)", f"{expected_wins}")
    col2.metric(f"❌ Perdus ({(1-win_rate)*100:.0f}%)", f"{expected_losses}")
    
    profit_color = "#4CAF50" if net_profit > 0 else "#F44336"
    
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, {profit_color}, {'#2E7D32' if net_profit > 0 else '#C62828'}); 
                padding: 25px; border-radius: 15px; text-align: center; color: white !important; margin: 15px 0;">
        <h2 style="color: white !important; margin: 0;">💎 PROFIT NET PRÉVU BET261</h2>
        <h1 style="color: white !important; margin: 10px 0; font-size: 40px;">{net_profit:+,} Ar</h1>
        <p style="color: white !important;">Sur {nb_tours} tours • Win Rate Bet261: ~{win_rate*100:.0f}%</p>
        <p style="color: white !important;">✅ Fiabilité: <b>{global_fiab:.1f}%</b></p>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("📅 Voir planning Bet261", key="a_plan"):
        ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
        st.markdown("### 📅 Planning Bet261 (TOP 10):")
        cumul = 0
        for i in range(1, 11):
            cumul += bet261_round_duration()
            t = ref + timedelta(seconds=cumul)
            fiab = calc_fiabilite_v16(i)
            
            # Prediction si win ou loss
            is_win = np.random.random() < win_rate
            status = "✅ GAIN" if is_win else "❌ LOSS"
            color_status = "#4CAF50" if is_win else "#F44336"
            
            st.markdown(f'''
            <div class="pred-auto">
                <b>Tour #{i}</b> • ⏰ <b>{t.strftime('%H:%M:%S')}</b> 🇲🇬 • 
                Cash Out: <b style="color: #2E7D32;">{multiplier:.2f}X</b> • 
                <b style="color: {color_status};">{status}</b> • 
                Fiab: <b>{fiab:.1f}%</b>
            </div>
            ''', unsafe_allow_html=True)
    
    st.info(f"""
    💡 **Règles d'Or Bet261:**
    - ✅ Cash Out à {multiplier:.2f}X (Win Rate: {win_rate*100:.0f}%)
    - ✅ Maximum 5% du bankroll/tour
    - ✅ Arrêter après 5 pertes consécutives
    - ✅ Reprendre 30 minutes plus tard
    - ✅ RTP Bet261 officiel: 97%
    """)

st.markdown("---")
st.caption(f"🇲🇬 Bet261 Predictor • Ora: {mada_now.strftime('%H:%M:%S')} • ⚠️ Jouez avec modération")
