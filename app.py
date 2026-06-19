import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from collections import Counter
from PIL import Image, ImageEnhance
import pytesseract
import re
from datetime import datetime

# CONFIGURATION
st.set_page_config(page_title="BET261 AI Predictor", layout="wide", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #000000 0%, #1a1a1a 100%); color: white; }
    .stApp { background-color: #0a0a0a; }
    h1, h2, h3 { color: #FFD700 !important; }
    .bet261-header {
        background: linear-gradient(90deg, #000000, #00C853, #FFD700);
        padding: 20px; border-radius: 10px; text-align: center;
        margin-bottom: 20px; border: 2px solid #FFD700;
    }
    .pred-aviator {
        background: linear-gradient(135deg, #000000, #00C853);
        padding: 18px; border-radius: 12px; text-align: center;
        color: white; margin: 8px 0; font-size: 22px; font-weight: bold;
        border: 2px solid #FFD700;
    }
    .pred-mega {
        background: linear-gradient(135deg, #000000, #FFD700);
        padding: 18px; border-radius: 12px; text-align: center;
        color: #000000; margin: 8px 0; font-size: 22px; font-weight: bold;
        border: 2px solid #00C853;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00C853, #FFD700);
        color: black; font-weight: bold; border: none; border-radius: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
    <div class="bet261-header">
        <h1 style="margin:0; color: #FFD700;">🎰 BET261 AI PREDICTOR 🎰</h1>
        <p style="color: white; margin: 5px 0;">Spécial Aviator & Mega Wheel</p>
    </div>
""", unsafe_allow_html=True)

# MENU
st.sidebar.title("⚡ BET261 MENU ⚡")
game = st.sidebar.radio("🎮 Fidio ny lalao:", ["✈️ Aviator", "🎡 Mega Wheel"])

# INIT
if 'aviator_data' not in st.session_state:
    st.session_state.aviator_data = []
if 'mega_data' not in st.session_state:
    st.session_state.mega_data = []

# OCR FUNCTIONS
def enhance_image(image):
    img = image.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    return img

def extract_aviator(image):
    try:
        enhanced = enhance_image(image)
        text = pytesseract.image_to_string(enhanced)
        mults = re.findall(r'(\d+[.,]\d+)x?', text)
        mults = [float(m.replace(',', '.')) for m in mults]
        mults = [m for m in mults if 1.0 <= m <= 1000.0]
        return mults, text
    except Exception as e:
        return [], str(e)

def extract_mega(image):
    try:
        enhanced = enhance_image(image)
        text = pytesseract.image_to_string(enhanced)
        nums = re.findall(r'\b(\d+)\b', text)
        valid = [1, 2, 5, 8, 10, 15, 20, 30, 40]
        results = [int(n) for n in nums if int(n) in valid]
        return results, text
    except Exception as e:
        return [], str(e)

# AVIATOR
if game == "✈️ Aviator":
    st.markdown("## ✈️ AVIATOR BET261")
    st.info("💡 Alaivo screenshot ny Round History eo amin'ny Aviator Bet261.")
    
    uploaded = st.file_uploader("📤 Alefaso ny sary", type=['png','jpg','jpeg'], key="av")
    
    if uploaded:
        image = Image.open(uploaded)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Sary", use_container_width=True)
        
        with col2:
            mults, raw = extract_aviator(image)
            if mults:
                st.success(f"✅ Nahita {len(mults)} multiplicateur")
                df_show = pd.DataFrame({
                    'N': range(1, len(mults)+1),
                    'Mult': [f"{m:.2f}x" for m in mults]
                })
                st.dataframe(df_show, height=300, use_container_width=True)
                
                if st.button("➕ AMPIDIRO", key="av_add"):
                    for m in mults:
                        st.session_state.aviator_data.append({
                            'Mult': m,
                            'Ora': datetime.now().strftime("%H:%M:%S")
                        })
                    st.success(f"Voatahiry {len(mults)}!")
                    st.rerun()
            else:
                st.error("Tsy hita ny isa.")
                with st.expander("Raw text"):
                    st.code(raw)
    
    st.markdown("---")
    st.markdown("### 🎯 TOP 5 Vinavina")
    
    if len(st.session_state.aviator_data) >= 5:
        df = pd.DataFrame(st.session_state.aviator_data)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", len(df))
        c2.metric("Max", f"{df['Mult'].max():.2f}x")
        c3.metric("Min", f"{df['Mult'].min():.2f}x")
        c4.metric("Salanisa", f"{df['Mult'].mean():.2f}x")
        
        red = len(df[df['Mult'] < 2])
        purple = len(df[(df['Mult'] >= 2) & (df['Mult'] < 10)])
        gold = len(df[df['Mult'] >= 10])
        
        st.markdown("#### 🎨 Loko:")
        cc1, cc2, cc3 = st.columns(3)
        cc1.metric("🔴 Mena", f"{red} ({red/len(df)*100:.0f}%)")
        cc2.metric("🟣 Volomparasy", f"{purple} ({purple/len(df)*100:.0f}%)")
        cc3.metric("🟡 Volamena", f"{gold} ({gold/len(df)*100:.0f}%)")
        
        if st.button("🚀 KAJIO TOP 5", use_container_width=True, key="av_pred"):
            with st.spinner("AI mikajy..."):
                values = df['Mult'].values
                X = np.arange(len(values)).reshape(-1, 1)
                model = RandomForestRegressor(n_estimators=200, random_state=42)
                model.fit(X, values)
                
                preds = []
                for i in range(1, 6):
                    pred = model.predict([[len(values)+i-1]])[0]
                    variation = np.random.uniform(-0.4, 0.6)
                    preds.append(max(1.0, pred + variation))
                
                st.markdown("### 🏆 TOP 5:")
                for idx, p in enumerate(preds, 1):
                    if p < 1.5:
                        risk = "🔴 RISIKA"
                    elif p < 2.5:
                        risk = "🟡 ANTONONY"
                    else:
                        risk = "🟢 TSARA"
                    safe = p * 0.85
                    st.markdown(f"""<div class="pred-aviator">#{idx} • {p:.2f}x • {risk}<br><small>Cash Out: {safe:.2f}x</small></div>""", unsafe_allow_html=True)
                
                st.info(f"💡 Auto Cash Out: **{min(preds)*0.85:.2f}x**")
        
        with st.expander("📜 Historique"):
            st.dataframe(df.tail(30), use_container_width=True)
    else:
        st.warning(f"⚠️ Mila 5 farafahakeliny (izao: {len(st.session_state.aviator_data)})")

# MEGA WHEEL
elif game == "🎡 Mega Wheel":
    st.markdown("## 🎡 MEGA WHEEL BET261")
    mega_numbers = [1, 2, 5, 
