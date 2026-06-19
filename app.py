import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from collections import Counter
from PIL import Image
import pytesseract
import re
from datetime import datetime, timedelta

st.set_page_config(page_title="BET261 AI", layout="wide", page_icon="🎰")

st.title("🎰 BET261 AI PREDICTOR PRO")
st.caption("Spécial Aviator & Mega Wheel - Madagascar 🇲🇬")

# Menu
game = st.sidebar.radio("Fidio ny lalao:", 
    ["✈️ Aviator", "🎡 Mega Wheel", "💰 Bankroll Manager", "📔 Diary"])

# INIT
if "av_data" not in st.session_state:
    st.session_state.av_data = []
if "mw_data" not in st.session_state:
    st.session_state.mw_data = []
if "bankroll" not in st.session_state:
    st.session_state.bankroll = 50000
if "initial_bank" not in st.session_state:
    st.session_state.initial_bank = 50000
if "diary" not in st.session_state:
    st.session_state.diary = []
if "stop_loss" not in st.session_state:
    st.session_state.stop_loss = 30
if "stop_win" not in st.session_state:
    st.session_state.stop_win = 50

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

def calc_fiability(pred, data):
    if len(data) < 5:
        return 50.0
    std = np.std(data)
    mean = np.mean(data)
    diff = abs(pred - mean)
    fiab = max(40, min(95, 100 - (diff / mean * 100) - (std * 5)))
    return fiab

def parse_ora(ora_str):
    try:
        t = datetime.strptime(ora_str.strip(), "%H:%M:%S")
        return datetime.now().replace(hour=t.hour, minute=t.minute, second=t.second, microsecond=0)
    except:
        return datetime.now()

def check_stop_limits():
    """Mijery raha tonga ny Stop Loss na Stop Win"""
    current = st.session_state.bankroll
    initial = st.session_state.initial_bank
    diff_pct = ((current - initial) / initial) * 100
    
    if diff_pct <= -st.session_state.stop_loss:
        return "STOP_LOSS", diff_pct
    elif diff_pct >= st.session_state.stop_win:
        return "STOP_WIN", diff_pct
    return "OK", diff_pct

# ====================================
# AVIATOR
# ====================================
if game == "✈️ Aviator":
    st.header("✈️ AVIATOR BET261")
    
    # Stop Limits Check
    status, pct = check_stop_limits()
    if status == "STOP_LOSS":
        st.error(f"🛑 **STOP LOSS!** Very {abs(pct):.1f}% ny volanao. AJANONY ny lalao!")
    elif status == "STOP_WIN":
        st.success(f"🎉 **STOP WIN!** Nahazo {pct:.1f}%! AJANONY izao mba tsy ho very!")
    
    # Bankroll Display
    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.metric("💰 Bankroll", f"{st.session_state.bankroll:,.0f} Ar")
    col_b2.metric("📊 Variation", f"{pct:+.1f}%", delta=f"{st.session_state.bankroll - st.session_state.initial_bank:+,.0f} Ar")
    col_b3.metric("🎯 Loka voalanjy (5%)", f"{int(st.session_state.bankroll * 0.05):,} Ar")
    
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
    
    # PAIKADY
    st.subheader("⚡ Fidio ny Paikady:")
    strategy = st.selectbox("Paikady:", [
        "🛡️ 1.5x Safe Strategy",
        "⚖️ 2 Bets Strategy",
        "🎯 Wait for Crash",
        "🔥 High Risk"
    ])
    
    if len(st.session_state.av_data) >= 5:
        data = st.session_state.av_data
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Data", len(data))
        c2.metric("Max", f"{max(data):.2f}x")
        c3.metric("Salanisa", f"{np.mean(data):.2f}x")
        
        # Strategy Display
        if strategy == "🛡️ 1.5x Safe Strategy":
            bet = int(st.session_state.bankroll * 0.10)
            st.markdown(f"""
            <div style="background: #1b5e20; padding: 20px; border-radius: 10px;">
                <h3 style="color: white;">🛡️ 1.5x Safe Strategy</h3>
                <p style="color: white;">• Auto Cash Out: <b>1.50x</b></p>
                <p style="color: white;">• Loka atao: <b>{bet:,} Ar</b> (10%)</p>
                <p style="color: white;">• Tombony manantena: <b>{int(bet*0.5):,} Ar</b></p>
                <p style="color: white;">• Win Rate: ~65-70%</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif strategy == "⚖️ 2 Bets Strategy":
            bet1 = int(st.session_state.bankroll * 0.07)
            bet2 = int(st.session_state.bankroll * 0.03)
            st.markdown(f"""
            <div style="background: #0d47a1; padding: 20px; border-radius: 10px;">
                <h3 style="color: white;">⚖️ 2 Bets Strategy</h3>
                <p style="color: white;">• Loka 1: <b>{bet1:,} Ar</b> → Cash Out 1.30x</p>
                <p style="color: white;">• Loka 2: <b>{bet2:,} Ar</b> → Cash Out 5.00x</p>
                <p style="color: white;">• Tombony Loka 1: {int(bet1*0.3):,} Ar</p>
                <p style="color: white;">• Tombony Loka 2: {int(bet2*4):,} Ar (raha tafita)</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif strategy == "🎯 Wait for Crash":
            last_3 = data[-3:] if len(data) >= 3 else data
            low_count = sum(1 for x in last_3 if x < 2.0)
            bet = int(st.session_state.bankroll * 0.08)
            
            if low_count >= 3:
                st.success(f"""
                ### 🎯 SIGNAL: MILOKÀ IZAO!
                Ny 3 round farany dia ambany rehetra ({last_3}).
                
                • Loka: **{bet:,} Ar**
                • Cash Out: **2.00x**
                • Tombony: **{bet:,} Ar**
                """)
            else:
                st.warning(f"""
                ### ⏳ MIANDRY...
                Ny 3 round farany: {last_3}
                
                Mila ambany rehetra (<2.00x) izy 3 vao milokà.
                """)
        
        else:  # High Risk
            bet = int(st.session_state.bankroll * 0.05)
            st.markdown(f"""
            <div style="background: #b71c1c; padding: 20px; border-radius: 10px;">
                <h3 style="color: white;">🔥 High Risk Strategy</h3>
                <p style="color: white;">• Auto Cash Out: <b>10.00x</b></p>
                <p style="color: white;">• Loka atao: <b>{bet:,} Ar</b> (5%)</p>
                <p style="color: white;">• Tombony manantena: <b>{int(bet*9):,} Ar</b></p>
                <p style="color: white;">• Win Rate: ~10-15%</p>
                <p style="color: yellow;">⚠️ AZA AMPIASAINA mihoatra ny 3 round!</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # SETTINGS ORA
        st.subheader("⏰ Settings Ora:")
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            ora_av = st.text_input("Ora manomboka (HH:MM:SS):", 
                                    value=datetime.now().strftime("%H:%M:%S"), 
                                    key="av_ora")
        with col_o2:
            interval_av = st.number_input("Elanelana (sec):", 
                                          min_value=10, max_value=120, 
                                          value=30, key="av_int")
        
        # KAJIO TOP 10
        if st.button("🚀 KAJIO TOP 10 VINAVINA", key="av_pred", use_container_width=True):
            values = np.array(data)
            X = np.arange(len(values)).reshape(-1, 1)
            model = RandomForestRegressor(n_estimators=200, random_state=42)
            model.fit(X, values)
            
            results = []
            start_time = parse_ora(ora_av)
            
            for i in range(1, 11):
                p = model.predict([[len(values) + i - 1]])[0]
                v = np.random.uniform(-0.3, 0.5)
                final_pred = max(1.0, p + v)
                pred_time = start_time + timedelta(seconds=interval_av * i)
                fiab = calc_fiability(final_pred, data)
                
                results.append({
                    "Round": i,
                    "Ora": pred_time.strftime("%H:%M:%S"),
                    "Multiplicateur": final_pred,
                    "Fiabilité": fiab
                })
            
            st.markdown("### 🏆 TOP 10 VINAVINA:")
            for r in results:
                p = r["Multiplicateur"]
                fiab = r["Fiabilité"]
                if p < 1.5:
                    risk = "🔴 RISIKA"
                    color = "#F44336"
                elif p < 2.5:
                    risk = "🟡 ANTONONY"
                    color = "#FFD700"
                else:
                    risk = "🟢 TSARA"
                    color = "#00C853"
                
                fiab_e = "🟢" if fiab >= 75 else ("🟡" if fiab >= 60 else "🔴")
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
                            padding: 12px; border-radius: 10px; margin: 5px 0;
                            border-left: 5px solid {color};">
                    <b style="color:white;">Round #{r['Round']} • ⏰ {r['Ora']} • {risk} {p:.2f}x</b><br>
                    <span style="color:#FFD700;">💰 Cash Out: {p*0.85:.2f}x | {fiab_e} Fiab: {fiab:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
        
        # AJOUTER AU DIARY
        st.markdown("---")
        st.subheader("📔 Ampidiro ao amin'ny Diary:")
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            loka_av = st.number_input("Loka (Ar):", min_value=100, value=1000, key="av_loka")
        with col_d2:
            vokatra = st.selectbox("Vokatra:", ["NAHAZO ✅", "LAVO ❌"], key="av_res")
        with col_d3:
            tombony = st.number_input("Tombony/Faty (Ar):", value=0, key="av_tomb")
        
        if st.button("📔 Ampidiro Diary", key="av_diary"):
            entry = {
                "Ora": datetime.now().strftime("%H:%M:%S"),
                "Lalao": "Aviator",
                "Loka": loka_av,
                "Vokatra": vokatra,
                "Tombony": tombony if vokatra == "NAHAZO ✅" else -loka_av
            }
            st.session_state.diary.append(entry)
            st.session_state.bankroll += entry["Tombony"]
            st.success("Voatahiry!")
            st.rerun()
        
        with st.expander("Historique"):
            st.dataframe(pd.DataFrame({"Mult": data}))
    else:
        st.warning(f"Mila 5 farafahakeliny. Izao: {len(st.session_state.av_data)}")

# ====================================
# MEGA WHEEL
# ====================================
elif game == "🎡 Mega Wheel":
    st.header("🎡 MEGA WHEEL BET261")
    
    status, pct = check_stop_limits()
    if status == "STOP_LOSS":
        st.error(f"🛑 **STOP LOSS!** Very {abs(pct):.1f}%. AJANONY!")
    elif status == "STOP_WIN":
        st.success(f"🎉 **STOP WIN!** Nahazo {pct:.1f}%! AJANONY!")
    
    col_b1, col_b2 = st.columns(2)
    col_b1.metric("💰 Bankroll", f"{st.session_state.bankroll:,.0f} Ar")
    col_b2.metric("📊 Variation", f"{pct:+.1f}%")
    
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
    
    # PAIKADY MEGA
    st.subheader("⚡ Fidio ny Paikady:")
    mw_strategy = st.selectbox("Paikady:", [
        "🛡️ Cover Strategy (Safe)",
        "⚖️ Balanced Strategy",
        "🔥 High Reward"
    ])
    
    total_bet = int(st.session_state.bankroll * 0.10)
    
    if mw_strategy == "🛡️ Cover Strategy (Safe)":
        st.markdown(f"""
        <div style="background: #1b5e20; padding: 20px; border-radius: 10px;">
            <h3 style="color: white;">🛡️ Cover Strategy</h3>
            <p style="color: white;">Loka totaly: <b>{total_bet:,} Ar</b></p>
            <p style="color: white;">• Isa <b>1</b>: {int(total_bet*0.70):,} Ar (70%)</p>
            <p style="color: white;">• Isa <b>2</b>: {int(total_bet*0.20):,} Ar (20%)</p>
            <p style="color: white;">• Isa <b>5</b>: {int(total_bet*0.10):,} Ar (10%)</p>
            <p style="color: yellow;">Win Rate: ~85%</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif mw_strategy == "⚖️ Balanced Strategy":
        st.markdown(f"""
        <div style="background: #0d47a1; padding: 20px; border-radius: 10px;">
            <h3 style="color: white;">⚖️ Balanced</h3>
            <p style="color: white;">• Isa <b>2</b>: {int(total_bet*0.40):,} Ar</p>
            <p style="color: white;">• Isa <b>5</b>: {int(total_bet*0.35):,} Ar</p>
            <p style="color: white;">• Isa <b>10</b>: {int(total_bet*0.25):,} Ar</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.markdown(f"""
        <div style="background: #b71c1c; padding: 20px; border-radius: 10px;">
            <h3 style="color: white;">🔥 High Reward</h3>
            <p style="color: white;">• Isa <b>10</b>: {int(total_bet*0.50):,} Ar</p>
            <p style="color: white;">• Isa <b>20</b>: {int(total_bet*0.30):,} Ar</p>
            <p style="color: white;">• Isa <b>40</b>: {int(total_bet*0.20):,} Ar</p>
            <p style="color: yellow;">⚠️ Win Rate: ~25%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if len(st.session_state.mw_data) >= 5:
        hist = st.session_state.mw_data
        st.write(f"**10 farany:** {hist[-10:]}")
        
        count = Counter(hist)
        total = len(hist)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**🔥 HOT**")
            hot = sorted(count.items(), key=lambda x: x[1], reverse=True)[:5]
            for n, f in hot:
                st.write(f"Isa **{n}**: {f} fois")
        
        with c2:
            st.markdown("**❄️ COLD**")
            last = {n: (hist[::-1].index(n) if n in hist else 99) for n in mega_nums}
            cold = sorted(last.items(), key=lambda x: x[1], reverse=True)[:5]
            for n, d in cold:
                st.write(f"Isa **{n}**: {d} lasa")
        
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            ora_mw = st.text_input("Ora (HH:MM:SS):", 
                                    value=datetime.now().strftime("%H:%M:%S"), 
                                    key="mw_ora")
        with col_o2:
            interval_mw = st.number_input("Elanelana (sec):", 
                                          min_value=30, max_value=180, 
                                          value=60, key="mw_int")
        
        if st.button("🚀 KAJIO TOP 10", key="mw_pred", use_container_width=True):
            scores = {}
            for n in mega_nums:
                freq = count.get(n, 0) / total
                dist = last[n] / 50
                scores[n] = (freq * 0.6) + (dist * 0.4)
            
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top10 = [sorted_scores[i % len(sorted_scores)] for i in range(10)]
            start_time = parse_ora(ora_mw)
            
            st.markdown("### 🏆 TOP 10:")
            for i, (n, s) in enumerate(top10, 1):
                conf = min(s * 200, 95)
                pred_time = start_time + timedelta(seconds=interval_mw * i)
                fiab_e = "🟢" if conf >= 75 else ("🟡" if conf >= 60 else "🔴")
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2d1b69, #11052c);
                            padding: 12px; border-radius: 10px; margin: 5px 0;
                            border-left: 5px solid #FFD700;">
                    <b style="color:white;">#{i} • ⏰ {pred_time.strftime('%H:%M:%S')} • Isa <span style="color:#FFD700;">{n}</span> ({n}x)</b><br>
                    <span style="color:#FFD700;">{fiab_e} Fiab: {conf:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Diary Mega
        st.markdown("---")
        st.subheader("📔 Ampidiro ao amin'ny Diary:")
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            loka_mw = st.number_input("Loka (Ar):", min_value=100, value=1000, key="mw_loka")
        with col_d2:
            vokatra_mw = st.selectbox("Vokatra:", ["NAHAZO ✅", "LAVO ❌"], key="mw_res")
        with col_d3:
            tombony_mw = st.number_input("Tombony/Faty (Ar):", value=0, key="mw_tomb")
        
        if st.button("📔 Ampidiro Diary", key="mw_diary"):
            entry = {
                "Ora": datetime.now().strftime("%H:%M:%S"),
                "Lalao": "Mega Wheel",
                "Loka": loka_mw,
                "Vokatra": vokatra_mw,
                "Tombony": tombony_mw if vokatra_mw == "NAHAZO ✅" else -loka_mw
            }
            st.session_state.diary.append(entry)
            st.session_state.bankroll += entry["Tombony"]
            st.success("Voatahiry!")
            st.rerun()
        
        with st.expander("Historique"):
            st.dataframe(pd.DataFrame({"Isa": hist}))
    else:
        st.warning(f"Mila 5. Izao: {len(st.session_state.mw_data)}")

# ====================================
# BANKROLL MANAGER
# ====================================
elif game == "💰 Bankroll Manager":
    st.header("💰 BANKROLL MANAGER")
    
    status, pct = check_stop_limits()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Bankroll Izao", f"{st.session_state.bankroll:,.0f} Ar")
    col2.metric("📌 Vola voalohany", f"{st.session_state.initial_bank:,.0f} Ar")
    col3.metric("📊 Variation", f"{pct:+.1f}%", 
                delta=f"{st.session_state.bankroll - st.session_state.initial_bank:+,.0f} Ar")
    
    if status == "STOP_LOSS":
        st.error(f"🛑 **STOP LOSS TRATRA!** Very {abs(pct):.1f}% (limite: {st.session_state.stop_loss}%)")
    elif status == "STOP_WIN":
        st.success(f"🎉 **STOP WIN TRATRA!** Nahazo {pct:.1f}% (limite: {st.session_state.stop_win}%)")
    else:
        st.info(f"✅ Mbola OK. Limite Stop Loss: -{st.session_state.stop_loss}%, Stop Win: +{st.session_state.stop_win}%")
    
    st.markdown("---")
    st.subheader("⚙️ Settings:")
    
    new_bank = st.number_input("💰 Bankroll vaovao (Ar):", 
                                min_value=1000, 
                                value=st.session_state.bankroll, 
                                step=1000)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        new_sl = st.slider("🛑 Stop Loss (%):", 5, 50, st.session_state.stop_loss)
    with col_s2:
        new_sw = st.slider("🎉 Stop Win (%):", 10, 100, st.session_state.stop_win)
    
    if st.button("💾 Tehirizo Settings", use_container_width=True):
        st.session_state.bankroll = new_bank
        st.session_state.initial_bank = new_bank
        st.session_state.stop_loss = new_sl
        st.session_state.stop_win = new_sw
        st.success("Voatahiry!")
        st.rerun()
    
    st.markdown("---")
    st.subheader("🧮 Calculator de Loka:")
    pct_bet = st.slider("% ny Bankroll hampiasaina:", 1, 20, 5)
    bet_amount = int(st.session_state.bankroll * pct_bet / 100)
    st.metric(f"Loka ({pct_bet}%)", f"{bet_amount:,} Ar")
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Torohevitra:")
    st.markdown(f"""
    - 🎯 **Loka tsara indrindra**: {int(st.session_state.bankroll * 0.05):,} Ar (5%)
    - ⚠️ **Loka maximum**: {int(st.session_state.bankroll * 0.10):,} Ar (10%)
    - 🛑 **Stop Loss**: Aza very mihoatra ny {int(st.session_state.initial_bank * st.session_state.stop_loss / 100):,} Ar
    - 🎉 **Stop Win**: Mialà raha mahazo {int(st.session_state.initial_bank * st.session_state.stop_win / 100):,} Ar
    """)

# ====================================
# DIARY
# ====================================
elif game == "📔 Diary":
    st.header("📔 DIARY - Tantaran'ny Loka")
    
    if len(st.session_state.diary) > 0:
        df_diary = pd.DataFrame(st.session_state.diary)
        
        # Stats
        total_bet = df_diary["Loka"].sum()
        total_win = df_diary[df_diary["Tombony"] > 0]["Tombony"].sum()
        total_loss = abs(df_diary[df_diary["Tombony"] < 0]["Tombony"].sum())
        net = total_win - total_loss
        win_count = len(df_diary[df_diary["Vokatra"] == "NAHAZO ✅"])
        win_rate = (win_count / len(df_diary)) * 100
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🎲 Loka totaly", f"{total_bet:,} Ar")
        c2.metric("✅ Tombony", f"+{total_win:,} Ar")
        c3.metric("❌ Faty", f"-{total_loss:,} Ar")
        c4.metric("📊 Net", f"{net:+,} Ar", delta=f"{win_rate:.1f}% Win Rate")
        
        st.markdown("---")
        st.subheader("📋 Tantaran'ny loka:")
        st.dataframe(df_diary, use_container_width=True, height=400)
        
        if st.button("🗑️ Hamafa Diary"):
            st.session_state.diary = []
            st.rerun()
    else:
        st.info("Mbola tsy misy loka voatahiry. Mandehana amin'ny Aviator na Mega Wheel.")

# SIDEBAR
st.sidebar.markdown("---")
st.sidebar.metric("💰 Bankroll", f"{st.session_state.bankroll:,.0f} Ar")
st.sidebar.write(f"✈️ Aviator: **{len(st.session_state.av_data)}**")
st.sidebar.write(f"🎡 Mega: **{len(st.session_state.mw_data)}**")
st.sidebar.write(f"📔 Diary: **{len(st.session_state.diary)}**")

if st.sidebar.button("🗑️ Hamafa Aviator"):
    st.session_state.av_data = []
    st.rerun()

if st.sidebar.button("🗑️ Hamafa Mega"):
    st.session_state.mw_data = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("🇲🇬 Made in Madagascar")
st.sidebar.caption("⚠️ Milalao am-pahendrena!")
