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

st.title("🎰 BET261 AI PREDICTOR")
st.caption("Spécial Aviator & Mega Wheel - Madagascar 🇲🇬")

game = st.sidebar.radio("Fidio ny lalao:", ["✈️ Aviator", "🎡 Mega Wheel"])

if "av_data" not in st.session_state:
    st.session_state.av_data = []
if "mw_data" not in st.session_state:
    st.session_state.mw_data = []

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
    """Mamadika 12:29:30 ho datetime"""
    try:
        t = datetime.strptime(ora_str.strip(), "%H:%M:%S")
        return datetime.now().replace(hour=t.hour, minute=t.minute, second=t.second, microsecond=0)
    except:
        return datetime.now()

# ===== AVIATOR =====
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
    st.subheader("🎯 TOP 10 Vinavina + Ora + Fiabilité")
    
    if len(st.session_state.av_data) >= 5:
        data = st.session_state.av_data
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", len(data))
        c2.metric("Max", f"{max(data):.2f}x")
        c3.metric("Salanisa", f"{np.mean(data):.2f}x")
        
        st.markdown("#### ⏰ Settings Ora:")
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            ora_av = st.text_input("Ora manomboka (HH:MM:SS):", 
                                    value=datetime.now().strftime("%H:%M:%S"), 
                                    key="av_ora")
        with col_o2:
            interval_av = st.number_input("Elanelana (segondra):", 
                                          min_value=10, max_value=120, 
                                          value=30, key="av_int")
        
        if st.button("🚀 KAJIO TOP 10", key="av_pred", use_container_width=True):
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
                    risk_emoji = "🔴"
                    risk_text = "RISIKA"
                    border_color = "#F44336"
                elif p < 2.5:
                    risk_emoji = "🟡"
                    risk_text = "ANTONONY"
                    border_color = "#FFD700"
                else:
                    risk_emoji = "🟢"
                    risk_text = "TSARA"
                    border_color = "#00C853"
                
                if fiab >= 75:
                    fiab_color = "🟢"
                elif fiab >= 60:
                    fiab_color = "🟡"
                else:
                    fiab_color = "🔴"
                
                safe = p * 0.85
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); 
                            padding: 15px; border-radius: 10px; margin: 8px 0;
                            border-left: 5px solid {border_color};">
                    <h4 style="color: white; margin: 0;">
                        Round #{r['Round']} • ⏰ <b>{r['Ora']}</b>
                    </h4>
                    <p style="color: white; margin: 5px 0; font-size: 18px;">
                        {risk_emoji} <b>{p:.2f}x</b> ({risk_text})
                    </p>
                    <p style="color: #FFD700; margin: 5px 0;">
                        💰 Cash Out: <b>{safe:.2f}x</b> | {fiab_color} Fiabilité: <b>{fiab:.1f}%</b>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 📊 Tabilao:")
            df_res = pd.DataFrame(results)
            df_res["Multiplicateur"] = df_res["Multiplicateur"].apply(lambda x: f"{x:.2f}x")
            df_res["Cash Out"] = [f"{r['Multiplicateur']*0.85:.2f}x" for r in results]
            df_res["Fiabilité"] = df_res["Fiabilité"].apply(lambda x: f"{x:.1f}%")
            st.dataframe(df_res, use_container_width=True, height=400)
            
            avg_fiab = np.mean([r["Fiabilité"] for r in results])
            high_preds = sum(1 for r in results if r["Multiplicateur"] >= 2.0)
            best_round = max(range(10), key=lambda i: results[i]['Multiplicateur'])
            
            st.success(f"""
            **📊 Famintinana:**
            - 🎯 Fiabilité antonony: **{avg_fiab:.1f}%**
            - 🟢 Round tsara: **{high_preds}/10**
            - 💡 Round tsara indrindra: **Round #{best_round+1}** amin'ny **{results[best_round]['Ora']}** ({results[best_round]['Multiplicateur']:.2f}x)
            """)
        
        with st.expander("Historique"):
            st.dataframe(pd.DataFrame({"Mult": data}))
    else:
        st.warning(f"Mila 5 farafahakeliny. Izao: {len(st.session_state.av_data)}")

# ===== MEGA WHEEL =====
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
    st.subheader("🎯 TOP 10 Vinavina + Ora + Fiabilité")
    
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
        
        st.markdown("#### ⏰ Settings Ora:")
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            ora_mw = st.text_input("Ora manomboka (HH:MM:SS):", 
                                    value=datetime.now().strftime("%H:%M:%S"), 
                                    key="mw_ora")
        with col_o2:
            interval_mw = st.number_input("Elanelana (segondra):", 
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
            
            st.markdown("### 🏆 TOP 10 VINAVINA:")
            
            results = []
            for i, (n, s) in enumerate(top10, 1):
                conf = min(s * 200, 95)
                pred_time = start_time + timedelta(seconds=interval_mw * i)
                
                results.append({
                    "Round": i,
                    "Ora": pred_time.strftime("%H:%M:%S"),
                    "Isa": n,
                    "Payout": f"{n}x",
                    "Fiabilité": conf
                })
                
                if conf >= 75:
                    fiab_color = "🟢"
                elif conf >= 60:
                    fiab_color = "🟡"
                else:
                    fiab_color = "🔴"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2d1b69, #11052c);
                            padding: 15px; border-radius: 10px; margin: 8px 0;
                            border-left: 5px solid #FFD700;">
                    <h4 style="color: white; margin: 0;">
                        Round #{i} • ⏰ <b>{pred_time.strftime('%H:%M:%S')}</b>
                    </h4>
                    <p style="color: white; margin: 5px 0; font-size: 20px;">
                        🎯 Isa: <b style="color:#FFD700;">{n}</b> (Payout: {n}x)
                    </p>
                    <p style="color: #FFD700; margin: 5px 0;">
                        {fiab_color} Fiabilité: <b>{conf:.1f}%</b>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 📊 Tabilao:")
            df_res = pd.DataFrame(results)
            df_res["Fiabilité"] = df_res["Fiabilité"].apply(lambda x: f"{x:.1f}%")
            st.dataframe(df_res, use_container_width=True, height=400)
            
            avg_fiab = np.mean([r["Fiabilité"] for r in results])
            st.success(f"""
            **📊 Famintinana:**
            - 🎯 Fiabilité antonony: **{avg_fiab:.1f}%**
            - 💡 TOP 3: Isa **{results[0]['Isa']}**, **{results[1]['Isa']}**, **{results[2]['Isa']}**
            """)
        
        with st.expander("Historique"):
            st.dataframe(pd.DataFrame({"Isa": hist}))
    else:
        st.warning(f"Mila 5. Izao: {len(st.session_state.mw_data)}")

st.sidebar.markdown("---")
st.sidebar.write(f"✈️ Aviator: **{len(st.session_state.av_data)}**")
st.sidebar.write(f"🎡 Mega: **{len(st.session_state.mw_data)}**")

if st.sidebar.button("🗑️ Hamafa Aviator"):
    st.session_state.av_data = []
    st.rerun()

if st.sidebar.button("🗑️ Hamafa Mega"):
    st.session_state.mw_data = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("🇲🇬 Made in Madagascar")
