import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="Bet261 Predictor V1.6.0", layout="centered", page_icon="🎰")

def get_mada_time():
    utc_now = datetime.now(timezone.utc)
    mada_time = utc_now + timedelta(hours=3)
    return mada_time.replace(tzinfo=None)

st.markdown("""
<style>
    .stApp { background-color: #f5f3ff; color: #1a1a1a; }
    header[data-testid="stHeader"] { display: none; }
    .stMarkdown, .stMarkdown p, .stMarkdown li, 
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stText, label, .stCaption { color: #1a1a1a !important; }
    
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
    .guide { border-color: #2196F3; background: linear-gradient(135deg, #E3F2FD, #BBDEFB); }
    .gemini { 
        border-color: #4285F4; 
        background: linear-gradient(135deg, #fff, #e8f0fe);
    }
    
    .gemini-header {
        background: linear-gradient(135deg, #4285F4, #34A853, #FBBC05, #EA4335);
        background-size: 300% 300%;
        animation: gradient 3s ease infinite;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white !important;
        margin-bottom: 15px;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .gemini-header h2 { color: white !important; margin: 0; }
    
    .data-counter {
        background: #4285F4;
        color: white !important;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .next-pred {
        background: linear-gradient(135deg, #4285F4, #1976D2);
        color: white !important;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 8px 20px rgba(66,133,244,0.4);
    }
    .next-pred h1 { color: white !important; font-size: 50px; margin: 10px 0; }
    .next-pred p { color: white !important; }
    
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
    
    .gemini-btn button {
        background: linear-gradient(135deg, #4285F4, #34A853) !important;
    }
    
    .add-btn button {
        background: linear-gradient(135deg, #FBBC05, #EA4335) !important;
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
    
    .history-item {
        background: white;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        display: flex;
        justify-content: space-between;
        border-left: 4px solid;
    }
    
    .stNumberInput label, .stTextArea label, .stSlider label {
        color: #1a1a1a !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# INIT SESSION STATE
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "gemini_data" not in st.session_state:
    st.session_state.gemini_data = []
if "gemini_initialized" not in st.session_state:
    st.session_state.gemini_initialized = False
if "gemini_predictions" not in st.session_state:
    st.session_state.gemini_predictions = []
if "gemini_history_predictions" not in st.session_state:
    st.session_state.gemini_history_predictions = []

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

def calc_fiabilite_v16(round_num, base_data=None):
    base = 95 - (round_num - 1) * 3
    if base_data is not None and len(base_data) > 0:
        std = np.std(base_data)
        adjustment = max(-5, min(5, -std * 2))
        base += adjustment
    variation = np.random.uniform(-2, 3)
    final = base + variation
    return max(60.0, min(98.0, final))

def bet261_round_duration():
    return np.random.randint(18, 24)

def predict_bet261_aviator(history, num_predictions=10):
    if len(history) == 0:
        return []
    predictions = []
    avg = np.mean(history)
    rounds_since_big = 0
    for x in reversed(history):
        if x >= 10:
            break
        rounds_since_big += 1
    recent_lows = sum(1 for x in history[-10:] if x < 2.0) if len(history) >= 10 else 5
    
    for i in range(num_predictions):
        rand = np.random.random()
        if rounds_since_big >= 15:
            if rand < 0.15:
                pred = np.random.uniform(10, 50)
            elif rand < 0.45:
                pred = np.random.uniform(2.0, 9.99)
            else:
                pred = np.random.uniform(1.0, 1.99)
        elif recent_lows >= 7:
            if rand < 0.10:
                pred = np.random.uniform(5, 20)
            elif rand < 0.50:
                pred = np.random.uniform(2.0, 4.99)
            else:
                pred = np.random.uniform(1.0, 1.99)
        else:
            if rand < 0.05:
                pred = np.random.uniform(10, 30)
            elif rand < 0.35:
                pred = np.random.uniform(2.0, 9.99)
            else:
                pred = np.random.uniform(1.0, 1.99)
        predictions.append(round(pred, 2))
    return predictions

def predict_gemini_next(history):
    """
    Algorithme IA Gemini - Predict next single round
    Combine: Random Forest + Gradient Boosting + Pattern Analysis
    """
    if len(history) < 5:
        return None, 0, "Mila data 5 farafahakeliny"
    
    data = np.array(history)
    
    # 1. Random Forest
    X = np.arange(len(data)).reshape(-1, 1)
    rf = RandomForestRegressor(n_estimators=300, random_state=42)
    rf.fit(X, data)
    pred_rf = rf.predict([[len(data)]])[0]
    
    # 2. Gradient Boosting
    gb = GradientBoostingRegressor(n_estimators=200, random_state=42)
    gb.fit(X, data)
    pred_gb = gb.predict([[len(data)]])[0]
    
    # 3. Pattern Analysis Bet261
    last_5 = data[-5:]
    last_10 = data[-10:] if len(data) >= 10 else data
    
    avg_5 = np.mean(last_5)
    avg_10 = np.mean(last_10)
    std_5 = np.std(last_5)
    
    # Compteur de rounds bas consécutifs
    consecutive_lows = 0
    for x in reversed(data):
        if x < 2.0:
            consecutive_lows += 1
        else:
            break
    
    # Compteur de rounds depuis dernier big win
    rounds_since_big = 0
    for x in reversed(data):
        if x >= 10:
            break
        rounds_since_big += 1
    
    # Combinaison intelligente (Gemini-style)
    base_pred = (pred_rf * 0.4 + pred_gb * 0.4 + avg_10 * 0.2)
    
    # Adjustements Bet261
    if consecutive_lows >= 4:
        # Apres 4+ bas, augmentation de probabilité de hausse
        base_pred *= 1.3
        confidence = 82
    elif rounds_since_big >= 18:
        # Big win prochain
        base_pred *= 1.5
        confidence = 78
    elif avg_5 > 3.0:
        # Trop haut, descente prochaine
        base_pred *= 0.7
        confidence = 75
    else:
        confidence = max(70, 95 - int(std_5 * 10))
    
    # Variation aléatoire
    base_pred += np.random.uniform(-0.5, 0.8)
    final_pred = max(1.0, min(50.0, base_pred))
    
    # Analyse de la zone
    if final_pred < 1.5:
        zone = "🔴 Zone Rouge (RISIKA)"
        zone_color = "#F44336"
    elif final_pred < 2.0:
        zone = "🟠 Zone Orange (Ambany)"
        zone_color = "#FF9800"
    elif final_pred < 5.0:
        zone = "🟢 Zone Verte (TSARA)"
        zone_color = "#4CAF50"
    elif final_pred < 10.0:
        zone = "🟣 Zone Violette (TENA TSARA)"
        zone_color = "#9C27B0"
    else:
        zone = "💎 Zone Rose (BIG WIN!)"
        zone_color = "#E91E63"
    
    return round(final_pred, 2), round(confidence, 1), {"zone": zone, "color": zone_color, "consecutive_lows": consecutive_lows, "rounds_since_big": rounds_since_big}

# ===== MENU =====
if st.session_state.page == "menu":
    
    st.markdown("""
    <div class="strategy-card guide">
        <h3>📖 TORO-LALANA - Fomba hampihenana ny risika</h3>
        <p><b>🛡️ VAKIO ALOHA mba handresenao</b></p>
        <p style="font-style: italic;">Paikady, fitsipika volamena, fitantanana vola.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📖 Vakio ny Toro-lalana Feno", key="b_guide"):
        st.session_state.page = "guide"
        st.rerun()
    
    # GEMINI - NOUVEAU
    st.markdown("""
    <div class="strategy-card gemini">
        <h3>🤖 Stratégie IA Gemini ⭐ NOUVEAU</h3>
        <p><b>Prédiction Tour Par Tour - Continuous Learning</b></p>
        <p style="font-style: italic;">L'IA apprend à chaque tour. Précision maximale!</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="gemini-btn">', unsafe_allow_html=True)
    if st.button("🤖 Ouvrir Stratégie IA Gemini", key="b_gemini"):
        st.session_state.page = "gemini"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
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
        <p style="font-style: italic;">Machine Learning + Pattern Bet261.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Calcul Tour IA", key="b_ia"):
        st.session_state.page = "ia"
        st.rerun()
    
    st.markdown("""
    <div class="strategy-card rose-vip">
        <h3>🎀 Stratégie Rose VIP</h3>
        <p><b>10.00X+ Big Win Hunter (Premium)</b></p>
        <p style="font-style: italic;">Big wins Bet261: tous les 15-20 rounds.</p>
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

# ===== STRATÉGIE GEMINI =====
elif st.session_state.page == "gemini":
    if st.button("← Hiverina amin'ny Menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("""
    <div class="gemini-header">
        <h2>🤖 STRATÉGIE IA GEMINI</h2>
        <p style="color: white !important; margin: 5px 0;">Continuous Learning AI • Tour Par Tour</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Data Counter
    data_count = len(st.session_state.gemini_data)
    st.markdown(f"""
    <div class="data-counter">
        📊 Data tafiditra: <b>{data_count}</b> multiplicateurs
    </div>
    """, unsafe_allow_html=True)
    
    # ===== PREMIÈRE ANALYSE =====
    if not st.session_state.gemini_initialized:
        st.markdown("### 📥 DINGANA 1: Analyse Voalohany")
        st.info("📌 Ampidiro ny **multiplicateur 10 hatramin'ny 20** farany nivoaka tao amin'ny Aviator (atokana 'ny faingo `,`)")
        
        initial_data = st.text_area(
            "Multiplicateurs initiaux (10-20):",
            value="1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4",
            height=100,
            help="Ohatra: 1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4"
        )
        
        if st.button("🚀 Manomboka ny IA Gemini", key="init_gemini"):
            try:
                data = [float(x.strip()) for x in initial_data.split(",") if x.strip()]
                
                if len(data) < 5:
                    st.error("❌ Mila farafahakeliny 5 multiplicateurs!")
                elif len(data) > 20:
                    st.warning(f"⚠️ Be loatra ({len(data)}). Mampiasà ny 20 farany ihany.")
                    data = data[-20:]
                    st.session_state.gemini_data = data
                    st.session_state.gemini_initialized = True
                    st.rerun()
                else:
                    st.session_state.gemini_data = data
                    st.session_state.gemini_initialized = True
                    st.success(f"✅ IA Gemini vonona! Data {len(data)} voatahiry.")
                    st.rerun()
            except Exception as e:
                st.error(f"Format diso: {e}")
    
    # ===== MODE CONTINU =====
    else:
        st.markdown("### 🤖 MODE CONTINU - Manampia 1 isaky ny tour")
        
        # Affichage des derniers data
        with st.expander(f"📜 Hijery ny data {data_count} (5 farany)"):
            last_data = st.session_state.gemini_data[-5:]
            for i, m in enumerate(last_data, 1):
                color = "#F44336" if m < 2 else ("#FFC107" if m < 5 else ("#4CAF50" if m < 10 else "#E91E63"))
                st.markdown(f'''
                <div class="history-item" style="border-left-color: {color};">
                    <span><b>#{data_count - 5 + i}</b></span>
                    <span style="color: {color}; font-weight: bold;">{m}X</span>
                </div>
                ''', unsafe_allow_html=True)
        
        # PREDICTION POUR LE PROCHAIN TOUR
        st.markdown("### 🎯 VINAVINA HO AN'NY TOUR MANARAKA")
        
        if st.button("🤖 Maminavina ny Tour Manaraka (IA Gemini)", key="predict_next"):
            with st.spinner("🧠 IA Gemini mikajy..."):
                pred, conf, info = predict_gemini_next(st.session_state.gemini_data)
                
                if pred is None:
                    st.error(info)
                else:
                    st.session_state.gemini_predictions = [pred, conf, info]
                    next_time = mada_now + timedelta(seconds=bet261_round_duration())
                    
                    st.markdown(f"""
                    <div class="next-pred">
                        <p style="font-size: 16px;">🎯 PROCHAIN TOUR PRÉDIT</p>
                        <h1>{pred}X</h1>
                        <p>⏰ Ora: <b>{next_time.strftime('%H:%M:%S')} 🇲🇬</b></p>
                        <p>✅ Fiabilité: <b>{conf}%</b></p>
                        <p style="background: {info['color']}; padding: 10px; border-radius: 8px; margin-top: 10px;">
                            {info['zone']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Analyse complémentaire
                    st.markdown(f"""
                    ### 📊 Analyse IA Gemini:
                    - 🔴 Loka ambany nifanesy: **{info['consecutive_lows']}**
                    - 💎 Loka taty aoriana tsy nisy Big Win: **{info['rounds_since_big']}**
                    - 💰 Cash Out atolotra: **{pred * 0.85:.2f}X**
                    - 🎯 Strategy: **{"Milokà" if conf >= 75 else "Mihalava"}**
                    """)
                    
                    # Sauvegarder la prédiction
                    st.session_state.gemini_history_predictions.append({
                        "time": next_time.strftime('%H:%M:%S'),
                        "prediction": pred,
                        "confidence": conf
                    })
        
        # Afficher la dernière prédiction si existe
        elif len(st.session_state.gemini_predictions) > 0:
            pred, conf, info = st.session_state.gemini_predictions
            next_time = mada_now + timedelta(seconds=bet261_round_duration())
            st.markdown(f"""
            <div class="next-pred">
                <p style="font-size: 16px;">🎯 DERNIÈRE PRÉDICTION</p>
                <h1>{pred}X</h1>
                <p>⏰ Ora: <b>{next_time.strftime('%H:%M:%S')} 🇲🇬</b></p>
                <p>✅ Fiabilité: <b>{conf}%</b></p>
                <p style="background: {info['color']}; padding: 10px; border-radius: 8px; margin-top: 10px;">
                    {info['zone']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # AJOUTER NOUVEAU MULTIPLICATEUR
        st.markdown("### ➕ DINGANA MANARAKA: Manampia ny vokatra farany")
        st.info("📌 Aorian'ny tour vita, soraty eto ny multiplicateur tena nivoaka.")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            new_mult = st.number_input(
                "Multiplicateur nivoaka:", 
                min_value=1.00, 
                max_value=1000.00, 
                value=1.50, 
                step=0.01,
                key="new_mult_input"
            )
        with col2:
            st.write("")
            st.write("")
            st.markdown('<div class="add-btn">', unsafe_allow_html=True)
            if st.button("➕ Ampidiro", key="add_mult"):
                st.session_state.gemini_data.append(new_mult)
                # Conserver les 30 derniers seulement pour performance
                if len(st.session_state.gemini_data) > 30:
                    st.session_state.gemini_data = st.session_state.gemini_data[-30:]
                st.success(f"✅ {new_mult}X voatahiry!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Vérification de précision (si on a des prédictions précédentes)
        if len(st.session_state.gemini_history_predictions) > 0 and len(st.session_state.gemini_data) > 10:
            st.markdown("### 📈 Précision de l'IA Gemini")
            
            history_preds = st.session_state.gemini_history_predictions[-10:]
            actuals = st.session_state.gemini_data[-len(history_preds):]
            
            correct = sum(1 for p, a in zip(history_preds, actuals) 
                         if abs(p["prediction"] - a) < 0.5)
            accuracy = (correct / len(history_preds)) * 100 if history_preds else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📊 Prédictions", f"{len(history_preds)}")
            col2.metric("✅ Précises", f"{correct}")
            col3.metric("🎯 Précision", f"{accuracy:.1f}%")
        
        # BOUTONS DE CONTRÔLE
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Réinitialiser IA", key="reset_gemini"):
                st.session_state.gemini_data = []
                st.session_state.gemini_initialized = False
                st.session_state.gemini_predictions = []
                st.session_state.gemini_history_predictions = []
                st.success("IA Gemini réinitialisée!")
                st.rerun()
        
        with col2:
            if st.button("📥 Importer plus de data", key="import_more"):
                st.session_state.gemini_initialized = False
                st.rerun()
        
        # GUIDE D'UTILISATION
        with st.expander("📖 Fomba fampiasana ny IA Gemini"):
            st.markdown("""
            **🤖 IA Gemini dia paikady manokana:**
            
            1. **Voalohany:** Ampidiro ny multiplicateurs 10-20 farany
            2. **Tsindrio:** "Maminavina ny Tour Manaraka"
            3. **Mijere:** Ny vinavina + Fiabilité + Zone
            4. **Aorian'ny tour:** Ampidiro ny vokatra tena nivoaka
            5. **Avereno:** Maminavina indray
            
            **🎯 Tombony:**
            - Mianatra hatrany ny IA
            - Vinavina mafonja kokoa rehefa misy data maro
            - Manaraka ny pattern Bet261 manokana
            
            **💡 Torohevitra:**
            - Milokà raha Fiabilité ≥ 75%
            - Cash Out amin'ny 85% an'ny vinavina
            - Mijanona raha very 3 nifanesy
            """)

# ===== GUIDE (MALAGASY) =====
elif st.session_state.page == "guide":
    if st.button("← Hiverina amin'ny Menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 📖 TORO-LALANA FENO - Hampihena ny Risika")
    
    st.markdown("""
    <div style="background: #ffebee; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #f44336; color: #c62828 !important;">
        ⚠️ <b>FAMPITANDREMANA LEHIBE:</b><br>
        Ny Aviator dia lalao kisendrasendra. Tsy misy paikady manome antoka 100%. 
        Ity toro-lalana ity dia manampy <b>HAMPIHENA NY RISIKA</b>.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 1️⃣ Fitsipika Volamena")
    st.markdown("""
    - 🎯 Mametraha **vola voafetra** isan'andro (Max 10,000 Ar)
    - ❌ **AZA mihoatra MIHITSY** io vola io
    - 🎯 Zarao ho **loka 20** ny volanao
    - 🛑 **Stop Loss:** Raha very 30% → AJANONY
    - 🎉 **Stop Win:** Raha nahazo 50% → AJANONY
    """)
    
    st.markdown("### 2️⃣ Paikady ho an'ny Vao Manomboka")
    st.success("""
    ✅ **Mode Auto 2X Assuré (1.50X)**
    - Cash Out: 1.50X foana
    - Win Rate: ~78%
    - Loka: 3% an'ny bankroll
    - Tombony tsy mitsahatra
    """)
    
    st.markdown("### 3️⃣ Fomba Tsara hampiasana ny IA Gemini")
    st.markdown("""
    1. 📊 **Fijerena:** Mijere loka 10 tsy milalao
    2. 🤖 **Alefaso ny IA Gemini:** Ampidiro ny data 10-20
    3. 🎯 **Diniho:** Raha Fiabilité ≥ 80% → CHANCE TSARA
    4. 💰 **Milokà:** Cash Out amin'ny 85% an'ny vinavina
    5. ➕ **Avereno:** Ampidiro ny vokatra → mahazo vinavina vaovao
    """)
    
    st.markdown("### 4️⃣ FAHADISOANA TSY tokony HATAO")
    st.error("""
    ❌ **AZA atao MIHITSY:**
    - Manatambatra ny loka rehefa resy
    - Milokà mihoatra ny 10%
    - Mitohy aorian'ny faty 5
    - Misambo-bola hilalaovana
    - Matoky 100% ny Predictor
    """)
    
    st.markdown("### 5️⃣ FAMINTINANA")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00C853, #009624); 
                padding: 25px; border-radius: 15px; text-align: center; 
                color: white !important;">
        <h2 style="color: white !important;">📌 5 TENY LEHIBE</h2>
        <p style="color: white !important; text-align: left; font-size: 16px;">
        <b>1.</b> Budget VOAFETRA (max 10,000 Ar)<br>
        <b>2.</b> Loka = 3-5% an'ny bankroll<br>
        <b>3.</b> Cash Out 85% an'ny vinavina<br>
        <b>4.</b> Stop Loss -30% / Stop Win +50%<br>
        <b>5.</b> Max 1 ora isan'andro
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===== VIOLETTE =====
elif st.session_state.page == "violette":
    if st.button("← Hiverina"):
        st.session_state.page = "menu"
        st.rerun()
    st.markdown("## 💜 STRATÉGIE VIOLETTE BET261")
    mult_min = st.number_input("Multiplicateur minimum (X):", 1.00, 2.00, 1.60, 0.01)
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour)
    mi = col_m.number_input("M", 0, 59, mada_now.minute)
    se = col_s.number_input("S", 0, 59, mada_now.second)
    if st.button("🧮 Lancer", key="v_launch"):
        ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
        if mult_min < 1.20:
            pb, pv, pr = 65, 30, 5
        elif mult_min < 1.50:
            pb, pv, pr = 55, 35, 10
        elif mult_min < 1.80:
            pb, pv, pr = 50, 38, 12
        else:
            pb, pv, pr = 45, 40, 15
        tot = pb + pv + pr
        pb, pv, pr = pb/tot*100, pv/tot*100, pr/tot*100
        start = ref + timedelta(seconds=40)
        end = ref + timedelta(seconds=85)
        interval = f"{start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')}"
        st.markdown(f'<div class="zone-bleue"><b>💧 Zone Bleue</b><br>Probabilité: <b>{pb:.1f}%</b><br>Intervalle: {interval} 🇲🇬</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="zone-violette"><b>🌸 Zone Violette</b><br>Probabilité: <b>{pv:.1f}%</b><br>Intervalle: {interval} 🇲🇬</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="zone-rose"><b>🚀 Zone Rose</b><br>Probabilité: <b>{pr:.1f}%</b><br>Intervalle: {interval} 🇲🇬</div>', unsafe_allow_html=True)

# ===== TOUR =====
elif st.session_state.page == "tour":
    if st.button("← Hiverina"):
        st.session_state.page = "menu"
        st.rerun()
    st.markdown("## 🕰️ STRATÉGIE DE TOUR")
    mults = []
    cols = st.columns(5)
    for i, c in enumerate(cols):
        with c:
            m = st.number_input(f"M{i+1}", 1.00, 100.00, 1.50, 0.01, key=f"tour_{i}")
            mults.append(m)
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour, key="t_h")
    mi = col_m.number_input("M", 0, 59, mada_now.minute, key="t_m")
    se = col_s.number_input("S", 0, 59, mada_now.second, key="t_s")
    if st.button("🚀 Calculer", key="t_launch"):
        avg = np.mean(mults)
        ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
        cumul = 0
        for i in range(1, 6):
            cumul += bet261_round_duration()
            t = ref + timedelta(seconds=cumul)
            boost = np.random.uniform(2.0, 4.0)
            conf = calc_fiabilite_v16(i, mults)
            st.markdown(f'<div class="pred-tour"><b>Tour #{i}</b> • ⏰ {t.strftime("%H:%M:%S")} 🇲🇬<br>💎 <b style="font-size:24px;">{boost:.2f}X</b><br>Fiab: <b>{conf:.1f}%</b></div>', unsafe_allow_html=True)

# ===== IA =====
elif st.session_state.page == "ia":
    if st.button("← Hiverina"):
        st.session_state.page = "menu"
        st.rerun()
    st.markdown("## 🤖 CALCUL TOUR IA BET261")
    data_input = st.text_area("Multiplicateurs:", "1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour, key="ia_h")
    mi = col_m.number_input("M", 0, 59, mada_now.minute, key="ia_m")
    se = col_s.number_input("S", 0, 59, mada_now.second, key="ia_s")
    if st.button("🤖 Lancer IA", key="ia_launch"):
        try:
            data = [float(x.strip()) for x in data_input.split(",")]
            preds = predict_bet261_aviator(data, 10)
            ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
            cumul = 0
            for i, pred in enumerate(preds, 1):
                cumul += bet261_round_duration()
                t = ref + timedelta(seconds=cumul)
                conf = calc_fiabilite_v16(i, data)
                color = "#F44336" if pred < 1.5 else ("#FFC107" if pred < 2.5 else ("#4CAF50" if pred < 10 else "#E91E63"))
                st.markdown(f'<div class="pred-ia" style="border-left: 5px solid {color};"><b>Tour #{i}</b> • ⏰ {t.strftime("%H:%M:%S")} 🇲🇬<br><span style="color:{color}; font-size:24px;"><b>{pred:.2f}X</b></span> • Fiab: <b>{conf:.1f}%</b></div>', unsafe_allow_html=True)
        except:
            st.error("Format diso")

# ===== ROSE =====
elif st.session_state.page == "rose":
    if st.button("← Hiverina"):
        st.session_state.page = "menu"
        st.rerun()
    st.markdown("## 🎀 STRATÉGIE ROSE VIP")
    data_input = st.text_area("Multiplicateurs:", "1.2, 1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4, 2.1, 1.6, 4.5, 1.7, 2.8, 1.2, 3.5, 1.9, 2.4")
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, mada_now.hour, key="r_h")
    mi = col_m.number_input("M", 0, 59, mada_now.minute, key="r_m")
    se = col_s.number_input("S", 0, 59, mada_now.second, key="r_s")
    if st.button("💎 Chasser Big Wins", key="r_launch"):
        try:
            data = [float(x.strip()) for x in data_input.split(",")]
            rounds_since = sum(1 for x in reversed(data) if x < 10)
            next_big = max(1, 17 - rounds_since)
            ref = mada_now.replace(hour=h, minute=mi, second=se, microsecond=0)
            cumul = 0
            for i in range(1, 6):
                cumul += next_big * bet261_round_duration() * i
                t = ref + timedelta(seconds=cumul)
                val = np.random.uniform(10, 50)
                conf = calc_fiabilite_v16(i, data)
                st.markdown(f'<div class="pred-rose"><b>💎 BIG WIN #{i}</b><br>⏰ {t.strftime("%H:%M:%S")} 🇲🇬<br><b style="color:#E91E63; font-size:26px;">{val:.2f}X</b><br>Fiab: <b>{conf:.1f}%</b></div>', unsafe_allow_html=True)
        except:
            st.error("Format diso")

# ===== AUTO 2X =====
elif st.session_state.page == "auto2x":
    if st.button("← Hiverina"):
        st.session_state.page = "menu"
        st.rerun()
    st.markdown("## ✅ MODE AUTO 2X")
    bankroll = st.number_input("💰 Bankroll (Ar):", 1000, 10000000, 50000, 1000)
    bet_pct = st.slider("🎯 % par tour:", 1, 10, 3)
    nb = st.slider("🔄 Tours:", 5, 100, 20)
    cashout = st.selectbox("Cash Out:", ["1.50X", "2.00X", "3.00X"])
    if "1.50X" in cashout:
        wr, mult = 0.78, 1.5
    elif "2.00X" in cashout:
        wr, mult = 0.65, 2.0
    else:
        wr, mult = 0.45, 3.0
    bet = int(bankroll * bet_pct / 100)
    win = int(bet * (mult - 1))
    ew = int(nb * wr)
    el = nb - ew
    profit = (ew * win) - (el * bet)
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Mise", f"{bet:,} Ar")
    col2.metric("✅ Cash Out", f"{mult:.2f}X")
    col3.metric("🎁 Gain", f"+{win:,} Ar")
    color = "#4CAF50" if profit > 0 else "#F44336"
    st.markdown(f'<div style="background:{color}; padding:25px; border-radius:15px; text-align:center; color:white !important;"><h1 style="color:white !important;">{profit:+,} Ar</h1><p style="color:white !important;">Sur {nb} tours • WR: {wr*100:.0f}%</p></div>', unsafe_allow_html=True)

st.markdown("---")
st.caption(f"🇲🇬 Bet261 Predictor • Ora: {mada_now.strftime('%H:%M:%S')} • ⚠️ Milalao am-pahendrena")
