import streamlit as st
import datetime
import random
import numpy as np

# Configuration
st.set_page_config(page_title="Predictor Pro", page_icon="💰")

st.title("💰 Predictor Web App")
st.subheader("Aviator & Mega Wheel 🎯")

# Safidy lalao
st.write("### Safidio ny lalao:")
game = st.radio("", ["Aviator ✈️", "Mega Wheel 🎡"], horizontal=True)

st.markdown("---")

# ============ AVIATOR ============
if game == "Aviator ✈️":
    st.write("### 📊 Ampidiro ny Historique 5 farany (Multiplier):")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        h1 = st.number_input("1er", min_value=1.0, value=1.50, step=0.01, format="%.2f")
    with col2:
        h2 = st.number_input("2e", min_value=1.0, value=2.10, step=0.01, format="%.2f")
    with col3:
        h3 = st.number_input("3e", min_value=1.0, value=1.05, step=0.01, format="%.2f")
    with col4:
        h4 = st.number_input("4e", min_value=1.0, value=3.40, step=0.01, format="%.2f")
    with col5:
        h5 = st.number_input("5e", min_value=1.0, value=1.80, step=0.01, format="%.2f")
    
    history = [h1, h2, h3, h4, h5]
    
    st.markdown("---")
    
    if st.button("🚀 FAHITA SIGNAL (NEXT)", use_container_width=True, type="primary"):
        now = datetime.datetime.now()
        ora = now.hour
        minitra = now.minute
        segondra = now.second
        
        # ===== ALGORITHM =====
        average = sum(history) / len(history)
        max_val = max(history)
        min_val = min(history)
        
        # Mananalisa ny pattern
        low_count = sum(1 for x in history if x < 2.0)
        high_count = sum(1 for x in history if x >= 5.0)
        
        # Time factor
        time_factor = (minitra + segondra/60) / 60
        
        # Vinany
        if high_count >= 1 and history[-1] > 5.0:
            # Vao avy nisy "high" → mety ho ambany manaraka
            prediction = round(1.10 + random.uniform(0.05, 0.50), 2)
            confidence = "⚠️ AMBANY (Safe: 1.20x)"
            color = "🔴"
        elif low_count >= 4:
            # Efa ela nisy "low" → mety hiakatra
            prediction = round(average * 1.8 + time_factor * 2, 2)
            confidence = "🔥 AMBONY (Bet: 2.00x - 5.00x)"
            color = "🟢"
        else:
            # Normal
            prediction = round((average * 0.85) + time_factor, 2)
            confidence = "✅ ANTONONY (Safe: 1.50x)"
            color = "🟡"
        
        # Affichage
        st.success(f"### {color} Vinany manaraka: **{prediction}x**")
        st.info(f"**Confiance:** {confidence}")
        st.write(f"⏰ **Ora:** {now.strftime('%H:%M:%S')}")
        
        # Statistika
        with st.expander("📈 Statistika"):
            st.write(f"- Salan'isa (Average): **{round(average, 2)}x**")
            st.write(f"- Avo indrindra: **{max_val}x**")
            st.write(f"- Ambany indrindra: **{min_val}x**")
            st.write(f"- Isan'ny Low (<2x): **{low_count}/5**")
            st.write(f"- Isan'ny High (≥5x): **{high_count}/5**")

# ============ MEGA WHEEL ============
else:
    st.write("### 📊 Ampidiro ny Historique 5 farany (1, 2, 5, 10, 20, 40):")
    
    options = [1, 2, 5, 10, 20, 40]
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        m1 = st.selectbox("1er", options, key="m1")
    with col2:
        m2 = st.selectbox("2e", options, key="m2")
    with col3:
        m3 = st.selectbox("3e", options, key="m3")
    with col4:
        m4 = st.selectbox("4e", options, key="m4")
    with col5:
        m5 = st.selectbox("5e", options, key="m5")
    
    history = [m1, m2, m3, m4, m5]
    
    st.markdown("---")
    
    if st.button("🎡 FAHITA SIGNAL (NEXT)", use_container_width=True, type="primary"):
        now = datetime.datetime.now()
        
        # Analyse ny frequence
        freq = {opt: history.count(opt) for opt in options}
        
        # Ireo isa tsy mbola nivoaka na vitsy
        rare = sorted(freq.items(), key=lambda x: x[1])[:3]
        prediction_list = [r[0] for r in rare]
        
        main_pred = prediction_list[0]
        
        st.success(f"### 🎯 Vinany manaraka: **{main_pred}x**")
        st.info(f"**Backup numbers:** {prediction_list[1]}x, {prediction_list[2]}x")
        st.write(f"⏰ **Ora:** {now.strftime('%H:%M:%S')}")
        
        with st.expander("📈 Frequence"):
            for num, count in freq.items():
                st.write(f"- **{num}x** → nivoaka **{count}** indray mandeha")

st.markdown("---")
st.caption("⚠️ Fanamarihana: Ity app ity dia simulation. Ampiasao am-pahendrena. Tsy misy garantie 100%.")
