import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from collections import Counter
from PIL import Image
import pytesseract
import re
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Casino AI Predictor", layout="wide", page_icon="🎰")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .big-pred {
        background: linear-gradient(135deg, #e91e63, #9c27b0);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 10px 0;
        font-size: 22px;
        font-weight: bold;
    }
    .mega-pred {
        background: linear-gradient(135deg, #FF9800, #F44336);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 10px 0;
        font-size: 22px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- MENU ---
st.sidebar.title("🎮 MENU LEHIBE")
game = st.sidebar.radio("Fidio ny lalao:", ["✈️ Aviator", "🎡 Mega Wheel"])

# --- INITIALISATION ---
if 'aviator_data' not in st.session_state:
    st.session_state.aviator_data = []
if 'mega_data' not in st.session_state:
    st.session_state.mega_data = []

# --- FONCTION OCR ---
def extract_aviator(image):
    """Maka ny multiplicateur (ohatra: 1.50x)"""
    try:
        text = pytesseract.image_to_string(image)
        mults = re.findall(r'(\d+\.\d+)x?', text)
        mults = [float(m) for m in mults if 1.0 <= float(m) <= 1000.0]
        return mults, text
    except Exception as e:
        return [], str(e)

def extract_mega(image):
    """Maka ny isa Mega Wheel (1, 2, 5, 8, 10, 15, 20, 30, 40)"""
    try:
        text = pytesseract.image_to_string(image)
        nums = re.findall(r'\b(\d+)\b', text)
        valid = [1, 2, 5, 8, 10, 15, 20, 30, 40]
        results = [int(n) for n in nums if int(n) in valid]
        return results, text
    except Exception as e:
        return [], str(e)

# =====================================================
# FIZARANA 1: AVIATOR
# =====================================================
if game == "✈️ Aviator":
    st.title("✈️ AVIATOR Vision AI")
    st.write("Alefaso ny Screenshot an'ny Historique Aviator.")
    
    # Upload sary
    st.subheader("📸 Dingana 1: Capture")
    uploaded = st.file_uploader("Fidio ny sary Aviator", type=['png','jpg','jpeg'], key="av_upload")
    
    if uploaded:
        image = Image.open(uploaded)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Sary", use_column_width=True)
        
        with col2:
            mults, raw = extract_aviator(image)
            if mults:
                st.success(f"✅ Nahita {len(mults)} multiplicateur")
                df_show = pd.DataFrame({'N°': range(1, len(mults)+1), 'Mult': [f"{m}x" for m in mults]})
                st.dataframe(df_show, height=250)
                
                if st.button("➕ Ampidiro", type="primary", key="av_add"):
                    for m in mults:
                        st.session_state.aviator_data.append({
                            'Mult': m,
                            'Ora': datetime.now().strftime("%H:%M:%S")
                        })
                    st.success(f"Voatahiry {len(mults)} data!")
                    st.rerun()
            else:
                st.error("Tsy hita ny isa. Andramo sary mazava kokoa.")
                with st.expander("Raw text"):
                    st.text(raw)
    
    # Prediction
    st.markdown("---")
    st.subheader("🎯 Dingana 2: TOP 5 Vinavina")
    
    if len(st.session_state.aviator_data) >= 5:
        df = pd.DataFrame(st.session_state.aviator_data)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", len(df))
        c2.metric("Max", f"{df['Mult'].max():.2f}x")
        c3.metric("Min", f"{df['Mult'].min():.2f}x")
        c4.metric("Salanisa", f"{df['Mult'].mean():.2f}x")
        
        if st.button("🚀 KAJIO TOP 5", type="primary", use_container_width=True, key="av_pred"):
            with st.spinner("AI mikajy..."):
                values = df['Mult'].values
                X = np.arange(len(values)).reshape(-1, 1)
                model = RandomForestRegressor(n_estimators=200, random_state=42)
                model.fit(X, values)
                
                preds = []
                for i in range(1, 6):
                    pred = model.predict([[len(values)+i-1]])[0]
                    variation = np.random.uniform(-0.3, 0.5)
                    preds.append(max(1.0, pred + variation))
                
                st.markdown("### 🏆 TOP 5 Vinavina:")
                for idx, p in enumerate(preds, 1):
                    risk = "🔴 RISIKA" if p < 1.5 else ("🟡 ANTONONY" if p < 2.5 else "🟢 TSARA")
                    safe = p * 0.85
                    st.markdown(f"""
                    <div class="big-pred">
                        #{idx} - {p:.2f}x {risk}<br>
                        <small>Cash Out: {safe:.2f}x</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.info(f"💡 Mivoaha eo amin'ny **{min(preds)*0.85:.2f}x** ho fiarovana.")
        
        with st.expander("📜 Historique"):
            st.dataframe(df.tail(30), use_container_width=True)
    else:
        st.warning(f"⚠️ Ampidiro 5 farafahakeliny (izao: {len(st.session_state.aviator_data)})")

# =====================================================
# FIZARANA 2: MEGA WHEEL
# =====================================================
elif game == "🎡 Mega Wheel":
    st.title("🎡 MEGA WHEEL Vision AI")
    st.write("Alefaso ny Screenshot an'ny Historique Mega Wheel.")
    
    mega_numbers = [1, 2, 5, 8, 10, 15, 20, 30, 40]
    
    st.subheader("📸 Dingana 1: Capture")
    uploaded = st.file_uploader("Fidio ny sary Mega Wheel", type=['png','jpg','jpeg'], key="mw_upload")
    
    if uploaded:
        image = Image.open(uploaded)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Sary", use_column_width=True)
        
        with col2:
            nums, raw = extract_mega(image)
            if nums:
                st.success(f"✅ Nahita {len(nums)} isa")
                df_show = pd.DataFrame({'N°': range(1, len(nums)+1), 'Isa': nums})
                st.dataframe(df_show, height=250)
                
                if st.button("➕ Ampidiro", type="primary", key="mw_add"):
                    for n in nums:
                        st.session_state.mega_data.append(n)
                    st.success(f"Voatahiry {len(nums)} data!")
                    st.rerun()
            else:
                st.error("Tsy hita ny isa.")
                with st.expander("Raw text"):
                    st.text(raw)
    
    # Manual input
    with st.expander("✏️ Na ampidiro amin'ny tanana"):
        manual = st.selectbox("Fidio:", mega_numbers, key="mw_manual")
        if st.button("Ampidiro Manual", key="mw_btn"):
            st.session_state.mega_data.append(manual)
            st.rerun()
    
    # Prediction
    st.markdown("---")
    st.subheader("🎯 Dingana 2: TOP 5 Vinavina")
    
    if len(st.session_state.mega_data) >= 5:
        history = st.session_state.mega_data
        st.write(f"**10 farany:** {history[-10:]}")
        
        count = Counter(history)
        total = len(history)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🔥 HOT (Matetika)")
            hot = sorted(count.items(), key=lambda x: x[1], reverse=True)[:5]
            for n, f in hot:
                pct = (f/total)*100
                st.write(f"Isa **{n}**: {f} fois ({pct:.1f}%)")
        
        with c2:
            st.subheader("❄️ COLD (Efa ela)")
            last_app = {n: (history[::-1].index(n) if n in history else 99) for n in mega_numbers}
            cold = sorted(last_app.items(), key=lambda x: x[1], reverse=True)[:5]
            for n, d in cold:
                st.write(f"Isa **{n}**: {d} rounds lasa")
        
        if st.button("🚀 KAJIO TOP 5", type="primary", use_container_width=True, key="mw_pred"):
            with st.spinner("AI mikajy..."):
                # Algorithme: Atambatra ny Hot sy ny Cold
                scores = {}
                for n in mega_numbers:
                    freq = count.get(n, 0) / total
                    distance = last_app[n] / 50
                    # Score: matetika nivoaka + efa ela tsy nivoaka
                    scores[n] = (freq * 0.6) + (distance * 0.4)
                
                top5 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
                
                st.markdown("### 🏆 TOP 5 Vinavina:")
                for idx, (n, score) in enumerate(top5, 1):
                    confidence = score * 100
                    st.markdown(f"""
                    <div class="mega-pred">
                        #{idx} - Isa {n} <br>
                        <small>Confidence: {confidence:.1f}%</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.info("💡 **Strategy:** Milokà amin'ny TOP 3 mba hisy fiarovana.")
        
        with st.expander("📜 Historique"):
            st.dataframe(pd.DataFrame({'Isa': history}).tail(30), use_container_width=True)
    else:
        st.warning(f"⚠️ Ampidiro 5 farafahakeliny (izao: {len(st.session_state.mega_data)})")

# --- SIDEBAR INFO ---
st.sidebar.markdown("---")
st.sidebar.write(f"**Aviator Data:** {len(st.session_state.aviator_data)}")
st.sidebar.write(f"**Mega Wheel Data:** {len(st.session_state.mega_data)}")

if st.sidebar.button("🗑️ Hamafa Aviator"):
    st.session_state.aviator_data = []
    st.rerun()

if st.sidebar.button("🗑️ Hamafa Mega Wheel"):
    st.session_state.mega_data = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📖 Fomba ampiasana:
1. Fidio ny lalao (Aviator na Mega Wheel)
2. Alaivo Screenshot ny History
3. Alefaso ilay sary
4. Tsindrio "Ampidiro"
5. Tsindrio "KAJIO TOP 5"
""")
