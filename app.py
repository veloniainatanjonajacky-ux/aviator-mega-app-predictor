import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from collections import Counter
from PIL import Image
import pytesseract
import re
from datetime import datetime

st.set_page_config(page_title="BET261 AI", layout="wide", page_icon="🎰")

st.title("🎰 BET261 AI PREDICTOR")
st.caption("Spécial Aviator & Mega Wheel - Madagascar 🇲🇬")

# Menu
game = st.sidebar.radio("Fidio ny lalao:", ["✈️ Aviator", "🎡 Mega Wheel"])

# Init
if "av_data" not in st.session_state:
    st.session_state.av_data = []
if "mw_data" not in st.session_state:
    st.session_state.mw_data = []

# OCR
def read_aviator(img):
    try:
        text = pytesseract.image_to_string(img)
        nums = re.findall(r"(\d+[.,]\d+)", text)
        nums = [float(n.replace(",", ".")) for n in nums]
        nums = [n for n in nums if 1.0 <= n <= 1000.0]
        return nums, text
    except Exception as e:
        return [], str(e)

def read_mega(img):
    try:
        text = pytesseract.image_to_string(img)
        nums = re.findall(r"\b(\d+)\b", text)
        valid = [1, 2, 5, 8, 10, 15, 20, 30, 40]
        results = [int(n) for n in nums if int(n) in valid]
        return results, text
    except Exception as e:
        return [], str(e)

# AVIATOR
if game == "✈️ Aviator":
    st.header("✈️ AVIATOR BET261")
    st.info("📸 Alaivo screenshot ny Round History.")
    
    up = st.file_uploader("Alefaso ny sary", type=["png", "jpg", "jpeg"], key="av_up")
    
    if up:
        img = Image.open(up)
        c1, c2 = st.columns(2)
        with c1:
            st.image(img, use_container_width=True)
        with c2:
            mults, raw = read_aviator(img)
            if mults:
                st.success(f"✅ Nahita {len(mults)} multiplicateur")
                st.dataframe(pd.DataFrame({"Mult": [f"{m}x" for m in mults]}))
                if st.button("➕ AMPIDIRO", key="av_btn"):
                    for m in mults:
                        st.session_state.av_data.append(m)
                    st.success("Voatahiry!")
                    st.rerun()
            else:
                st.error("Tsy hita ny isa.")
    
    st.markdown("---")
    st.subheader("🎯 TOP 5 Vinavina")
    
    if len(st.session_state.av_data) >= 5:
        data = st.session_state.av_data
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", len(data))
        c2.metric("Max", f"{max(data):.2f}x")
        c3.metric("Salanisa", f"{np.mean(data):.2f}x")
        
        if st.button("🚀 KAJIO TOP 5", key="av_pred"):
            values = np.array(data)
            X = np.arange(len(values)).reshape(-1, 1)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, values)
            
            preds = []
            for i in range(1, 6):
                p = model.predict([[len(values) + i - 1]])[0]
                v = np.random.uniform(-0.3, 0.5)
                preds.append(max(1.0, p + v))
            
            st.markdown("### 🏆 TOP 5:")
            for i, p in enumerate(preds, 1):
                if p < 1.5:
                    risk = "🔴 RISIKA"
                elif p < 2.5:
                    risk = "🟡 ANTONONY"
                else:
                    risk = "🟢 TSARA"
                st.success(f"**#{i} • {p:.2f}x** • {risk} • Cash Out: **{p*0.85:.2f}x**")
            
            st.info(f"💡 Auto Cash Out: **{min(preds)*0.85:.2f}x**")
        
        with st.expander("Historique"):
            st.dataframe(pd.DataFrame({"Mult": data}))
    else:
        st.warning(f"Mila 5 farafahakeliny. Izao: {len(st.session_state.av_data)}")

# MEGA WHEEL
else:
    st.header("🎡 MEGA WHEEL BET261")
    mega_nums = [1, 2, 5, 8, 10, 15, 20, 30, 40]
    
    up = st.file_uploader("Alefaso ny sary", type=["png", "jpg", "jpeg"], key="mw_up")
    
    if up:
        img = Image.open(up)
        c1, c2 = st.columns(2)
        with c1:
            st.image(img, use_container_width=True)
        with c2:
            nums, raw = read_mega(img)
            if nums:
                st.success(f"✅ Nahita {len(nums)} isa")
                st.dataframe(pd.DataFrame({"Isa": nums}))
                if st.button("➕ AMPIDIRO", key="mw_btn"):
                    for n in nums:
                        st.session_state.mw_data.append(n)
                    st.success("Voatahiry!")
                    st.rerun()
            else:
                st.error("Tsy hita ny isa.")
    
    with st.expander("✏️ Manual Input"):
        man = st.selectbox("Fidio:", mega_nums, key="mw_sel")
        if st.button("Ampidiro", key="mw_man"):
            st.session_state.mw_data.append(man)
            st.rerun()
    
    st.markdown("---")
    st.subheader("🎯 TOP 5 Vinavina")
    
    if len(st.session_state.mw_data) >= 5:
        hist = st.session_state.mw_data
        st.write(f"**10 farany:** {hist[-10:]}")
        
        count = Counter(hist)
        total = len(hist)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**🔥 HOT**")
            
