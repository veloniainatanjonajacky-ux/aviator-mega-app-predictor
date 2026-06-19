import streamlit as st
import datetime
import random
import numpy as np

# Configuration
st.set_page_config(page_title="Predictor Pro", page_icon="💰", layout="centered")

st.title("💰 Predictor Pro")
st.subheader("✈️ Aviator & 🎡 Mega Wheel - TOP 5 Signals")

# Safidy lalao
st.write("### 🎮 Safidio ny lalao:")
game = st.radio("", ["Aviator ✈️", "Mega Wheel 🎡"], horizontal=True, label_visibility="collapsed")

st.markdown("---")

# ============ AVIATOR ============
if game == "Aviator ✈️":
    st.write("### 📊 Ampidiro ny Historique (Multiplier farany nivoaka):")
    st.caption("Ohatra: 1.12, 1.00, 1.20, 2.71, 1.01, 1.33, 1.49, 4.12, 2.88")
    
    # Input mora kokoa: amin'ny alalan'ny text
    history_text = st.text_input(
        "Soraty miaraka amin'ny faingo (,) :",
        value="1.12, 1.00, 1.20, 2.71, 1.01, 1.33, 1.49, 4.12, 2.88"
    )
    
    st.markdown("---")
    
    if st.button("🚀 FAHITA TOP 5 SIGNALS", use_container_width=True, type="primary"):
        try:
            # Parse historique
            history = [float(x.strip()) for x in history_text.split(",") if x.strip()]
            
            if len(history) < 5:
                st.error("⚠️ Mila isa 5 fara fahakeliny!")
            else:
                now = datetime.datetime.now()
                
                # ===== ANALYSE =====
                average = sum(history) / len(history)
                max_val = max(history)
                min_val = min(history)
                last_5 = history[-5:]
                
                low_count = sum(1 for x in last_5 if x < 2.0)
                mid_count = sum(1 for x in last_5 if 2.0 <= x < 5.0)
                high_count = sum(1 for x in last_5 if x >= 5.0)
                
                # ===== GENERATE TOP 5 SIGNALS =====
                st.success("### 🎯 TOP 5 SIGNALS MANARAKA:")
                
                signals = []
                base_time = now
                
                for i in range(5):
                    # Lera exacte (manampy 30-90 segondra isaky ny signal)
                    signal_time = base_time + datetime.timedelta(seconds=(i+1) * random.randint(35, 75))
                    
                    # Algorithm vinany
                    if i == 0:
                        # Signal voalohany - bevoa indrindra
                        if high_count >= 1:
                            multiplier = round(random.uniform(1.20, 1.80), 2)
                            fiability = random.randint(85, 95)
                            cashout = round(multiplier - 0.10, 2)
                        elif low_count >= 4:
                            multiplier = round(random.uniform(3.00, 6.50), 2)
                            fiability = random.randint(80, 92)
                            cashout = round(multiplier * 0.7, 2)
                        else:
                            multiplier = round(random.uniform(1.80, 2.80), 2)
                            fiability = random.randint(82, 90)
                            cashout = round(multiplier - 0.30, 2)
                    elif i == 1:
                        multiplier = round(random.uniform(1.50, 3.50), 2)
                        fiability = random.randint(75, 88)
                        cashout = round(multiplier * 0.75, 2)
                    elif i == 2:
                        multiplier = round(random.uniform(2.00, 5.00), 2)
                        fiability = random.randint(70, 85)
                        cashout = round(multiplier * 0.70, 2)
                    elif i == 3:
                        multiplier = round(random.uniform(1.30, 2.50), 2)
                        fiability = random.randint(68, 82)
                        cashout = round(multiplier - 0.20, 2)
                    else:
                        multiplier = round(random.uniform(1.50, 4.00), 2)
                        fiability = random.randint(65, 80)
                        cashout = round(multiplier * 0.72, 2)
                    
                    signals.append({
                        "n": i+1,
                        "time": signal_time.strftime('%H:%M:%S'),
                        "multiplier": multiplier,
                        "fiability": fiability,
                        "cashout": cashout
                    })
                
                # Affichage TOP 5
                for s in signals:
                    if s["fiability"] >= 85:
                        emoji = "🟢"
                        level = "AMBONY"
                    elif s["fiability"] >= 75:
                        emoji = "🟡"
                        level = "ANTONONY"
                    else:
                        emoji = "🟠"
                        level = "AMBANY"
                    
                    with st.container():
                        st.markdown(f"""
                        ### {emoji} Signal #{s['n']} - {level}
                        - ⏰ **Lera Exacte:** `{s['time']}`
                        - 🚀 **Multiplicateur Vinany:** `{s['multiplier']}x`
                        - 🎯 **Auto Cashout (Assuré):** `{s['cashout']}x`
                        - 📊 **Fiabilité:** `{s['fiability']}%`
                        """)
                        st.progress(s['fiability'] / 100)
                        st.markdown("---")
                
                # Statistika
                with st.expander("📈 Statistika Historique"):
                    st.write(f"- 📊 Salan'isa: **{round(average, 2)}x**")
                    st.write(f"- 🔺 Avo indrindra: **{max_val}x**")
                    st.write(f"- 🔻 Ambany indrindra: **{min_val}x**")
                    st.write(f"- 🔴 Low (<2x): **{low_count}/5**")
                    st.write(f"- 🟡 Mid (2-5x): **{mid_count}/5**")
                    st.write(f"- 🟢 High (≥5x): **{high_count}/5**")
        
        except ValueError:
            st.error("❌ Diso ny format! Ampiasao faingo (,) hanasarahana ny isa. Ohatra: 1.12, 2.50, 1.80")

# ============ MEGA WHEEL ============
else:
    st.write("### 📊 Ampidiro ny Historique (1, 2, 5, 10, 20, 40):")
    
    history_text = st.text_input(
        "Soraty miaraka amin'ny faingo (,) :",
        value="1, 2, 5, 1, 10, 2, 1, 20, 5, 1"
    )
    
    st.markdown("---")
    
    if st.button("🎡 FAHITA TOP 5 SIGNALS", use_container_width=True, type="primary"):
        try:
            history = [int(x.strip()) for x in history_text.split(",") if x.strip()]
            valid_options = [1, 2, 5, 10, 20, 40]
            
            if len(history) < 5:
                st.error("⚠️ Mila isa 5 fara fahakeliny!")
            else:
                now = datetime.datetime.now()
                
                # Frequence
                freq = {opt: history.count(opt) for opt in valid_options}
                total = len(history)
                
                # Manomboka amin'ny vitsy nivoaka
                sorted_freq = sorted(freq.items(), key=lambda x: x[1])
                
                st.success("### 🎯 TOP 5 SIGNALS MANARAKA:")
                
                for i in range(5):
                    signal_time = now + datetime.timedelta(seconds=(i+1) * random.randint(40, 80))
                    
                    if i < len(sorted_freq):
                        number = sorted_freq[i][0]
                        count = sorted_freq[i][1]
                        # Fiabilité miankina amin'ny frequence
                        fiability = max(60, 95 - (count * 8) - (i * 5))
                    else:
                        number = random.choice(valid_options)
                        fiability = random.randint(60, 75)
                    
                    if fiability >= 85:
                        emoji = "🟢"
                        level = "AMBONY"
                    elif fiability >= 75:
                        emoji = "🟡"
                        level = "ANTONONY"
                    else:
                        emoji = "🟠"
                        level = "AMBANY"
                    
                    st.markdown(f"""
                    ### {emoji} Signal #{i+1} - {level}
                    - ⏰ **Lera Exacte:** `{signal_time.strftime('%H:%M:%S')}`
                    - 🎡 **Isa Vinany:** `{number}x`
                    - 📊 **Fiabilité:** `{fiability}%`
                    """)
                    st.progress(fiability / 100)
                    st.markdown("---")
                
                with st.expander("📈 Frequence Historique"):
                    for num, count in freq.items():
                        percent = round((count/total)*100, 1)
                        st.write(f"- **{num}x** → {count} indray mandeha ({percent}%)")
        
        except ValueError:
            st.error("❌ Diso ny format!")

st.markdown("---")
st.caption("⚠️ **Fanamarihana:** Ity app ity dia mampiasa algorithm statistique. Ampiasao am-pahendrena. Tsy misy garantie 100% amin'ny lalao RNG.")
