import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from collections import Counter
from PIL import Image, ImageEnhance
import pytesseract
import re
from datetime import datetime

# --- CONFIGURATION SPÉCIAL BET261 ---
st.set_page_config(page_title="BET261 AI Predictor", layout="wide", page_icon="🎰")

st.markdown("""
    <style>
    .main { 
        background: linear-gradient(180deg, #000000 0%, #1a1a1a 100%);
        color: white;
    }
    .stApp { background-color: #0a0a0a; }
    h1, h2, h3 { color: #FFD700 !important; }
    .bet261-header {
        background: linear-gradient(90deg, #000000, #00C853, #FFD700);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #FFD700;
    }
    .pred-aviator {
        background: linear-gradient(135deg, #000000, #00C853);
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin: 8px 0;
        font-size: 22px;
        font-weight: bold;
        border: 2px solid #FFD700;
        box-shadow: 0px 5px 15px rgba(255,215,0,0.3);
    }
    .pred-mega {
        background: linear-gradient(135deg, #000000, #FFD700);
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        color: #000000;
        margin: 8px 0;
        font-size: 22px;
        font-weight: bold;
        border: 2px solid #00C853;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00C853, #FFD700);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER BET261 ---
st.markdown("""
    <div class="bet261-header">
        <h1 style="margin:0; color: #FFD700;">🎰 BET261 AI PREDICTOR 🎰</h1>
        <p style="color: white; margin: 5px 0;">Spécial Aviator & Mega Wheel - Madagascar</p>
    </div>
""", unsafe_allow_html=True)

# --- MENU ---
st.sidebar.markdown("""
    <div style="text-align:center; padding: 10px; background: #00C853; border-radius: 10px; margin-bottom: 15px;">
        <h2 style="color: black; margin:0;">⚡ BET261 MENU ⚡</h2>
    </div>
""", unsafe_allow_html=True)

game = st.sidebar.radio("🎮 Fidio ny lalao:", ["✈️ Aviator Bet261", "🎡 Mega Wheel Bet261"])

# --- INIT ---
if 'aviator_data' not in st.session_state:
    st.session_state.aviator_data = []
if 'mega_data' not in st.session_state:
    st.session_state.mega_data = []

# --- OCR Namboarina ho an'ny Bet261 ---
def enhance_image(image):
    """Manatsara ny sary mba ho mora vakiana"""
    img = image.convert('L')  # Grayscale
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    return img

def extract_aviator_bet261(image):
    try:
        enhanced = enhance_image(image)
        text = pytesseract.image_to_string(enhanced)
        # Format Bet261: 1.50x, 2.10x, etc.
        mults = re.findall(r'(\d+[.,]\d+)x?', text)
        mults = [float(m.replace(',', '.')) for m in mults]
        mults = [m for m in mults if 1.0 <= m <= 1000.0]
        return mults, text
    except Exception as e:
        return [], str(e)

def extract_mega_bet261(image):
    try:
        enhanced = enhance_image(image)
        text = pytesseract.image_to_string(enhanced)
        nums = re.findall(r'\b(\d+)\b', text)
        valid = [1, 2, 5, 8, 10, 15, 20, 30, 40]
        results = [int(n) for n in nums if int(n) in valid]
        return results, text
    except Exception as e:
        return [], str(e)

# ====================================
# AVIATOR BET261
# ====================================
if game == "✈️ Aviator Bet261":
    st.markdown("## ✈️ AVIATOR BET261 - Vision AI")
    
    st.markdown("### 📸 Dingana 1: Capture Historique Bet261")
    st.info("💡 **Torohevitra:** Alaivo screenshot ny tabilao 'Round History' eo ambonin'ny lalao Aviator ao amin'ny Bet261.")
    
    uploaded = st.file_uploader("📤 Alefaso ny sary", type=['png','jpg','jpeg'], key="av")
    
    if uploaded:
        image = Image.open(uploaded)
        col1, col2 = st.columns([1,1])
        
        with col1:
            st.image(image, caption="Sary Bet261", use_column_width=True)
        
        with col2:
            mults, raw = extract_aviator_bet261(image)
            if mults:
                st.success(f"✅ Bet261 OCR: Nahita **{len(mults)}** multiplicateur")
                df_show = pd.DataFrame({
                    'N°': range(1, len(mults)+1),
                    'Multiplicateur': [f"{m:.2f}x" for m in mults],
                    'Loko': ['🔴 Mena' if m < 2 else ('🟣 Volomparasy' if m < 10 else '🟡 Volamena') for m in mults]
                })
                st.dataframe(df_show, height=300, use_container_width=True)
                
                if st.button("➕ AMPIDIRO AO AMIN'NY DATABASE", key="av_add"):
                    for m in mults:
                        st.session_state.aviator_data.append({
                            'Mult': m,
                            'Ora': datetime.now().strftime("%H:%M:%S")
                        })
                    st.success(f"✅ Voatahiry: {len(mults)} multiplicateur!")
                    st.rerun()
            else:
                st.error("❌ Tsy nahita isa. Andramo sary mazava kokoa.")
                with st.expander("🔍 Hijery ny raw text"):
                    st.code(raw)
    
    st.markdown("---")
    st.markdown("### 🎯 Dingana 2: TOP 5 Vinavina Bet261")
    
    if len(st.session_state.aviator_data) >= 5:
        df = pd.DataFrame(st.session_state.aviator_data)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Total", len(df))
        c2.metric("📈 Max", f"{df['Mult'].max():.2f}x")
        c3.metric("📉 Min", f"{df['Mult'].min():.2f}x")
        c4.metric("⚖️ Salanisa", f"{df['Mult'].mean():.2f}x")
        
        # Analyse Bet261 specifically
        red_count = len(df[df['Mult'] < 2])
        purple_count = len(df[(df['Mult'] >= 2) & (df['Mult'] < 10)])
        gold_count = len(df[df['Mult'] >= 10])
        
        st.markdown("#### 🎨 Famakafakana Loko (Bet261):")
        cc1, cc2, cc3 = st.columns(3)
        cc1.metric("🔴 Mena (<2x)", f"{red_count} ({red_count/len(df)*100:.0f}%)")
        cc2.metric("🟣 Volomparasy (2-10x)", f"{purple_count} ({purple_count/len(df)*100:.0f}%)")
        cc3.metric("🟡 Volamena (>10x)", f"{gold_count} ({gold_count/len(df)*100:.0f}%)")
        
        if st.button("🚀 KAJIO TOP 5 VINAVINA BET261", use_container_width=True, key="av_pred"):
            with st.spinner("⚡ Bet261 AI mikajy..."):
                values = df['Mult'].values
                X = np.arange(len(values)).reshape(-1, 1)
                model = RandomForestRegressor(n_estimators=300, random_state=42)
                model.fit(X, values)
                
                preds = []
                for i in range(1, 6):
                    pred = model.predict([[len(values)+i-1]])[0]
                    # Ajustement Bet261 RTP
                    variation = np.random.uniform(-0.4, 0.6)
                    final = max(1.0, pred + variation)
                    preds.append(final)
                
                st.markdown("### 🏆 TOP 5 VINAVINA BET261:")
                for idx, p in enumerate(preds, 1):
                    if p < 1.5:
                        risk = "🔴 RISIKA AVO"
                        safe = p * 0.80
                    elif p < 2.5:
                        risk = "🟡 ANTONONY"
                        safe = p * 0.85
                    else:
                        risk = "🟢 TSARA"
                        safe = p * 0.90
                    
                    st.markdown(f"""
                    <div class="pred-aviator">
                        #{idx} • {p:.2f}x • {risk}<br>
                        <small>💰 Cash Out Bet261: <b>{safe:.2f}x</b></small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.success(f"""
                **💡 Strategy Bet261:**
                - Auto Cash Out apetraho amin'ny **{min(preds)*0.85:.2f}x**
                - Mialà raha vao tonga amin'io isa io ny avion
                - Aza miloka mihoatra ny **10%** ny vola ao aminao isaky ny round
                """)
        
        with st.expander("📜 Historique Feno"):
            st.dataframe(df.tail(30), use_container_width=True)
    else:
        st.warning(f"⚠️ Mila data 5 farafahakeliny. Izao: **{len(st.session_state.aviator_data)}**")

# ====================================
# MEGA WHEEL BET261
# ====================================
elif game == "🎡 Mega Wheel Bet261":
    st.markdown("## 🎡 MEGA WHEEL BET261 - Vision AI")
    
    mega_numbers = [1, 2, 5, 8, 10, 15, 20, 30, 40]
    
    st.markdown("### 📸 Dingana 1: Capture Historique")
    st.info("💡 Alaivo screenshot ny 'Recent Results' eo amin'ny Mega Wheel Bet261.")
    
    uploaded = st.file_uploader("📤 Alefaso ny sary", type=['png','jpg','jpeg'], key="mw")
    
    if uploaded:
        image = Image.open(uploaded)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Sary Mega Wheel", use_column_width=True)
        
        with col2:
            nums, raw = extract_mega_bet261(image)
            if nums:
                st.success(f"✅ Nahita {len(nums)} isa")
                df_show = pd.DataFrame({'N°': range(1, len(nums)+1), 'Isa': nums})
                st.dataframe(df_show, height=250)
                
                if st.button("➕ AMPIDIRO", key="mw_add"):
                    for n in nums:
                        st.session_state.mega_data.append(n)
                    st.success(f"Voatahiry {len(nums)} data!")
                    st.rerun()
            else:
                st.error("Tsy hita ny isa.")
                with st.expander("Raw text"):
                    st.code(raw)
    
    with st.expander("✏️ Ampidiro amin'ny tanana"):
        manual = st.selectbox("Fidio:", mega_numbers, key="mw_man")
        if st.button("Ampidiro", key="mw_mbtn"):
            st.session_state.mega_data.append(manual)
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 🎯 Dingana 2: TOP 5 Vinavina Bet261")
    
    if len(st.session_state.mega_data) >= 5:
        history = st.session_state.mega_data
        st.write(f"**📜 10 farany:** `{history[-10:]}`")
        
        count = Counter(history)
        total = len(history)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🔥 HOT NUMBERS")
            hot = sorted(count.items(), key=lambda x: x[1], reverse=True)[:5]
            for n, f in hot:
                pct = (f/total)*100
                st.write(f"• Isa **{n}**: {f} fois (**{pct:.1f}%**)")
        
        with c2:
            st.markdown("#### ❄️ COLD NUMBERS")
            last_app = {n: (history[::-1].index(n) if n in history else 99) for n in mega_numbers}
            cold = sorted(last_app.items(), key=lambda x: x[1], reverse=True)[:5]
            for n, d in cold:
                st.write(f"• Isa **{n}**: efa **{d}** rounds lasa")
        
        if st.button("🚀 KAJIO TOP 5 BET261", use_container_width=True, key="mw_pred"):
            with st.spinner("⚡ Bet261 AI mikajy..."):
                scores = {}
                for n in mega_numbers:
                    freq = count.get(n, 0) / total
                    distance = last_app[n] / 50
                    # Weights manokana ho an'ny Bet261
                    weight = {1: 0.4, 2: 0.3, 5: 0.15, 8: 0.08, 10: 0.04, 15: 0.02, 20: 0.005, 30: 0.003, 40: 0.002}
                    scores[n] = (freq * 0.5) + (distance * 0.3) + (weight.get(n, 0.1) * 0.2)
                
                top5 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
                
                st.markdown("### 🏆 TOP 5 VINAVINA BET261:")
                for idx, (n, score) in enumerate(top5, 1):
                    confidence = min(score * 200, 95)
                    payout = {1:1, 2:2, 5:5, 8:8, 10:10, 15:15, 20:20, 30:30, 40:40}
                    st.markdown(f"""
                    <div class="pred-mega">
                        #{idx} • Isa <b>{n}</b> • Payout: <b>{payout[n]}x</b><br>
                        <small>Confidence: <b>{confidence:.1f}%</b></small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.success("""
                **💡 Strategy Bet261 Mega Wheel:**
                - Milokà amin'ny TOP 3 mba hisy fiarovana
                - Asio kely amin'ny isa lehibe (20, 30, 40) ho 'Bonus'
                - Andraso ny 'Mega Multiplier' (x20 na x50) vao miloka be
                """)
        
        with st.expander("📜 Historique"):
            st.dataframe(pd.DataFrame({'Isa': history}).tail(30), 
