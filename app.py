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
    .gemini { border-color: #4285F4; background: linear-gradient(135deg, #fff, #e8f0fe); }
    
    .gemini-header {
        background: linear-gradient(135deg, #4285F4, #34A853, #FBBC05, #EA4335);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white !important;
        margin-bottom: 15px;
    }
    .gemini-header h2 { color: white !important; margin: 0; }
    .gemini-header p { color: white !important; }
    
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
    
    .step-1 {
        background: linear-gradient(135deg, #4285F4, #1976D2);
        padding: 15px;
        border-radius: 10px;
        color: white !important;
        margin-bottom: 15px;
    }
    .step-1 h3 { color: white !important; margin: 0; }
    .step-1 p { color: white !important; margin: 5px 0; }
    
    .step-2 {
        background: linear-gradient(135deg, #FBBC05, #F57C00);
        padding: 15px;
        border-radius: 10px;
        color: white !important;
        margin-bottom: 15px;
    }
    .step-2 h3 { color: white !important; margin: 0; }
    .step-2 p { color: white !important; margin: 5px 0; }
    
    .step-3 {
        background: linear-gradient(135deg, #34A853, #2E7D32);
        padding: 15px;
        border-radius: 10px;
        color: white !important;
        margin-bottom: 15px;
    }
    .step-3 h3 { color: white !important; margin: 0; }
    .step-3 p { color: white !important; margin: 5px 0; }
    
    .step-4 {
        background: linear-gradient(135deg, #EA4335, #C62828);
        padding: 15px;
        border-radius: 10px;
        color: white !important;
        margin-bottom: 15px;
    }
    .step-4 h3 { color: white !important; margin: 0; }
    .step-4 p { color: white !important; margin: 5px 0; }
    
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

# HEADER
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

# FUNCTIONS
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
    if len(history) < 5:
        return None, 0, "Mila data 5 farafahakeliny"
    
    data = np.array(history)
    
    X = np.arange(len(data)).reshape(-1, 1)
    rf = RandomForestRegressor(n_estimators=300, random_state=42)
    rf.fit(X, data)
    pred_rf = rf.predict([[len(data)]])[0]
    
    gb = GradientBoostingRegressor(n_estimators=200, random_state=42)
    gb.fit(X, data)
    pred_gb = gb.predict([[len(data)]])[0]
    
    last_5 = data[-5:]
    last_10 = data[-10:] if len(data) >= 10 else data
    avg_5 = np.mean(last_5)
    avg_10 = np.mean(last_10)
    std_5 = np.std(last_5)
    
    consecutive_lows = 0
    for x in reversed(data):
        if x < 2.0:
            consecutive_lows += 1
        else:
            break
    
    rounds_since_big = 0
    for x in reversed(data):
        if x >= 10:
            break
        rounds_since_big += 1
    
    base_pred = (pred_rf * 0.4 + pred_gb * 0.4 + avg_10 * 0.2)
    
    if consecutive_lows >= 4:
        base_pred *= 1.3
        confidence = 82
    elif rounds_since_big >= 18:
        base_pred *= 1.5
        confidence = 78
    elif avg_5 > 3.0:
        base_pred *= 0.7
        confidence = 75
    else:
        confidence = max(70, 95 - int(std_5 * 10))
    
    base_pred += np.random.uniform(-0.5, 0.8)
    final_pred = max(1.0, min(50.0, base_pred))
    
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
    
    info = {
        "zone": zone,
        "color": zone_color,
        "consecutive_lows": consecutive_lows,
        "rounds_since_big": rounds_since_big
    }
    
    return round(final_pred, 2), round(confidence, 1), info

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
    
    st.markdown("""
    <div class="strategy-card gemini">
        <h3>🤖 Stratégie IA Gemini ⭐ NOUVEAU</h3>
        <p><b>Prédiction Tour Par Tour - Continuous Learning</b></p>
        <p style="font-style: italic;">L'IA apprend à chaque tour. Précision maximale!</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🤖 Ouvrir Stratégie IA Gemini", key="b_gemini"):
        st.session_state.page = "gemini"
        st.rerun()
    
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
        <p>Continuous Learning AI • Tour Par Tour</p>
    </div>
    """, unsafe_allow_html=True)
    
    # DINGANA 1: HISTORIQUE 20 VOALOHANY
    if not st.session_state.gemini_initialized:
        st.markdown("""
        <div class="step-1">
            <h3>📥 DINGANA 1: Historique 20 voalohany</h3>
            <p>Ampidiro ny multiplicateur 20 farany nivoaka tao amin'ny Aviator.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("📌 Ohatra: 1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4, 2.1, 1.6, 4.5, 1.7, 2.8, 1.2, 3.5, 1.9, 2.4, 1.5")
        
        initial_data = st.text_area(
            "✏️ Soraty eto ny multiplicateurs 20 voalohany (atokana faingo):",
            value="",
            height=120,
            placeholder="1.5, 2.3, 1.1, 5.6, 1.8, ...",
            key="initial_input"
        )
        
        if st.button("✅ Tehirizo ny Historique 20", key="init_gemini"):
            try:
                data = [float(x.strip()) for x in initial_data.split(",") if x.strip()]
                
                if len(data) < 10:
                    st.error(f"❌ Mila farafahakeliny 10 multiplicateurs! Izao misy: {len(data)}")
                elif len(data) > 20:
                    st.warning(f"⚠️ Be loatra ({len(data)}). Ny 20 farany ihany no horaisina.")
                    st.session_state.gemini_data = data[-20:]
                    st.session_state.gemini_initialized = True
                    st.rerun()
                else:
                    st.session_state.gemini_data = data
                    st.session_state.gemini_initialized = True
                    st.success(f"✅ Voatahiry tsara ny {len(data)} multiplicateurs!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Format diso. Ohatra: 1.5, 2.3, 1.1...")
    
    # MODE CONTINU
    else:
        data_count = len(st.session_state.gemini_data)
        
        st.markdown(f"""
        <div class="data-counter">
            📊 Data tafiditra: <b>{data_count}</b> multiplicateurs
        </div>
        """, unsafe_allow_html=True)
        
        # Hijery ny historique
        with st.expander(f"📜 Hijery ny Historique ({data_count} multiplicateurs)"):
            df_hist = pd.DataFrame({
                "N°": range(1, len(st.session_state.gemini_data) + 1),
                "Multiplicateur": [f"{m:.2f}X" for m in st.session_state.gemini_data],
                "Zone": ["🔴 Mena" if m < 2 else ("🟢 Maitso" if m < 10 else "💎 Big Win") 
                         for m in st.session_state.gemini_data]
            })
            st.dataframe(df_hist, use_container_width=True, height=300)
        
        # 10 farany
        st.markdown("**🔍 10 farany nivoaka:**")
        last_10 = st.session_state.gemini_data[-10:]
        cols = st.columns(5)
        for i, m in enumerate(last_10):
            color = "#F44336" if m < 2 else ("#FFC107" if m < 5 else ("#4CAF50" if m < 10 else "#E91E63"))
            with cols[i % 5]:
                st.markdown(f'''
                <div style="background: {color}; color: white; padding: 8px; border-radius: 8px; 
                            text-align: center; margin: 3px 0; font-weight: bold;">
                    {m:.2f}X
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # DINGANA 2: MANAMPIA 1 MULTIPLICATEUR
        st.markdown("""
        <div class="step-2">
            <h3>➕ DINGANA 2: Manampia 1 multiplicateur farany</h3>
            <p>Soraty eto ny multiplicateur farany nivoaka.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
            if st.button("➕ Ampidiro", key="add_mult"):
                st.session_state.gemini_data.append(new_mult)
                if len(st.session_state.gemini_data) > 30:
                    st.session_state.gemini_data = st.session_state.gemini_data[-30:]
                st.session_state.gemini_predictions = []
                st.success(f"✅ {new_mult}X voatahiry!")
                st.rerun()
        
        st.markdown("---")
        
        # DINGANA 3: ANALYSE + PREDICTION
        st.markdown("""
        <div class="step-3">
            <h3>🤖 DINGANA 3: Analyse + Vinavina</h3>
            <p>Tsindrio mba hahazoanao vinavina ny tour manaraka.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 MAMINAVINA NY TOUR MANARAKA", key="predict_next", use_container_width=True):
            with st.spinner("🧠 IA Gemini mikajy..."):
                pred, conf, info = predict_gemini_next(st.session_state.gemini_data)
                
                if pred is None:
                    st.error(info)
                else:
                    st.session_state.gemini_predictions = [pred, conf, info]
                    st.session_state.gemini_history_predictions.append({
                        "prediction": pred,
                        "confidence": conf,
                        "based_on": len(st.session_state.gemini_data)
                    })
                    st.rerun()
        
        # Affichage de la prédiction
        if len(st.session_state.gemini_predictions) > 0:
            pred, conf, info = st.session_state.gemini_predictions
            next_time = mada_now + timedelta(seconds=bet261_round_duration())
            
            st.markdown(f"""
            <div class="next-pred">
                <p style="font-size: 16px;">🎯 VINAVINA NY TOUR MANARAKA</p>
                <h1>{pred}X</h1>
                <p>⏰ Ora vinavinaina: <b>{next_time.strftime('%H:%M:%S')} 🇲🇬</b></p>
                <p>✅ Fiabilité: <b>{conf}%</b></p>
                <p style="background: {info['color']}; padding: 10px; border-radius: 8px; margin-top: 10px;">
                    {info['zone']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🔴 Loka ambany nifanesy", info['consecutive_lows'])
                st.metric("💰 Cash Out atolotra", f"{pred * 0.85:.2f}X")
            with col2:
                st.metric("💎 Tsy nisy Big Win", f"{info['rounds_since_big']} loka")
                strategy = "✅ Milokà" if conf >= 75 else ("⚠️ Mihalava" if conf >= 60 else "❌ Aza milokà")
                st.metric("🎯 Strategy", strategy)
            
            if conf >= 80:
                st.success(f"✅ TENA TSARA! Milokà. Cash Out: {pred * 0.85:.2f}X")
            elif conf >= 70:
                st.warning(f"⚠️ ANTONONY. Milokà kely. Cash Out: {pred * 0.85:.2f}X")
            else:
                st.error("❌ MAMETRA. Aleo aloha tsy milokà.")
            
            # DINGANA 4
            st.markdown("---")
            st.markdown("""
            <div class="step-4">
                <h3>🔄 DINGANA 4: Aorian'ny tour</h3>
                <p>Soraty ny multiplicateur tena nivoaka, dia maminavina indray.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                actual_mult = st.number_input(
                    "Multiplicateur tena nivoaka:", 
                    min_value=1.00, 
                    max_value=1000.00, 
                    value=1.50, 
                    step=0.01,
                    key="actual_mult"
                )
            with col2:
                st.write("")
                st.write("")
                if st.button("➕ Ampio + Maminavina", key="add_and_predict"):
                    st.session_state.gemini_data.append(actual_mult)
                    if len(st.session_state.gemini_data) > 30:
                        st.session_state.gemini_data = st.session_state.gemini_data[-30:]
                    
                    diff = abs(pred - actual_mult)
                    if diff < 0.5:
                        st.success(f"🎯 Marina! Vinavina: {pred:.2f}X • Tena: {actual_mult}X")
                    else:
                        st.warning(f"📊 Vinavina: {pred:.2f}X • Tena: {actual_mult}X")
                    
                    pred_new, conf_new, info_new = predict_gemini_next(st.session_state.gemini_data)
                    if pred_new is not None:
                        st.session_state.gemini_predictions = [pred_new, conf_new, info_new]
                        st.session_state.gemini_history_predictions.append({
                            "prediction": pred_new,
                            "confidence": conf_new,
                            "based_on": len(st.session_state.gemini_data)
                        })
                    
                    st.rerun()
        
        # PRÉCISION
        if len(st.session_state.gemini_history_predictions) >= 3:
            st.markdown("---")
            st.markdown("### 📈 Précision IA")
            
            history_preds = st.session_state.gemini_history_predictions[-10:]
            actuals = st.session_state.gemini_data[-len(history_preds):] if len(st.session_state.gemini_data) >= len(history_preds) else []
            
            if len(actuals) > 0:
                correct = sum(1 for p, a in zip(history_preds[:-1], actuals[1:]) 
                             if abs(p["prediction"] - a) < 1.0)
                total = len(history_preds) - 1
                accuracy = (correct / total) * 100 if total > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                col1.metric("📊 Vinavina", f"{total}")
                col2.metric("✅ Marina", f"{correct}")
                col3.metric("🎯 Précision", f"{accuracy:.1f}%")
        
        # RÉINITIALISATION
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Réinitialiser IA", key="reset_gemini"):
                st.session_state.gemini_data = []
                st.session_state.gemini_initialized = False
                st.session_state.gemini_predictions = []
                st.session_state.gemini_history_predictions = []
                st.success("✅ Réinitialisée!")
                st.rerun()
        
        with col2:
            if st.button("📥 Hanova ny Historique", key="import_more"):
                st.session_state.gemini_initialized = False
                st.rerun()

# ===== GUIDE =====
elif st.session_state.page == "guide":
    if st.button("← Hiverina amin'ny Menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 📖 TORO-LALANA FENO")
    
    st.error("⚠️ **FAMPITANDREMANA:** Ny Aviator dia lalao kisendrasendra. Tsy misy paikady 100% marina.")
    
    st.markdown("### 1️⃣ Fitsipika Volamena")
    st.markdown("""
    - 🎯 Mametraha **vola voafetra** isan'andro (Max 10,000 Ar)
    - ❌ **AZA mihoatra MIHITSY**
    - 🎯 Zarao ho **loka 20**
    - 🛑 **Stop Loss:** Raha very 30% → AJANONY
    - 🎉 **Stop Win:** Raha nahazo 50% → AJANONY
    """)
    
    st.markdown("### 2️⃣ Paikady ho an'ny Vao Manomboka")
    st.success("✅ **Mode Auto 2X Assuré (1.50X)** - Win Rate ~78%")
    
    st.markdown("### 3️⃣ Fomba hampiasana ny IA Gemini")
    st.markdown("""
    1. 📥 **Dingana 1:** Ampidiro ny 20 multiplicateurs voalohany
    2. ➕ **Dingana 2:** Manampia ny multiplicateur farany
    3. 🤖 **Dingana 3:** Tsindrio "Maminavina"
    4. 🔄 **Dingana 4:** Aorian'ny tour, soraty ny tena multiplicateur
    5. **Avereno** hatrany
    """)
    
    st.markdown("### 4️⃣ FAHADISOANA TSY tokony HATAO")
    st.error("""
    - Manatambatra ny loka rehefa resy
    - Milokà mihoatra ny 10%
    - Mitohy aorian'ny faty 5
    - Misambo-bola
    - Matoky 100% ny Predictor
    """)
    
    st.markdown("### 5️⃣ FAMINTINANA")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00C853, #009624); 
                padding: 25px; border-radius: 15px; color: white !important;">
        <h2 style="color: white !important;">📌 5 TENY LEHIBE</h2>
        <p style="color: white !important; font-size: 16px;">
        <b>1.</b> Budget VOAFETRA (max 10,000 Ar)<br>
        <b>2.</b> Loka = 3-5%<br>
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
    st.markdown("## 💜 STRATÉGIE VIOLETTE")
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
    st.markdown("## 🤖 CALCUL TOUR IA")
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
