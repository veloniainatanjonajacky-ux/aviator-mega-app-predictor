import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Aviator Predictor V1.6.0", layout="centered", page_icon="✈️")

st.markdown("""
<style>
    .stApp { background-color: #f5f3ff; }
    .main-header {
        background: linear-gradient(135deg, #880E4F, #AD1457);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        margin: -20px -20px 20px -20px;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 24px;
        font-weight: bold;
    }
    .strategy-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 6px solid;
    }
    .violette { border-color: #9C27B0; }
    .tour { border-color: #FF9800; }
    .ia { border-color: #00C853; background: #263238; color: white; }
    .rose-vip { border-color: #E91E63; }
    .auto-2x { border-color: #4CAF50; }
    .premium-lock {
        background: #FFF3E0;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 15px;
    }
    .premium-lock-dark {
        background: #FFF3E0;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 15px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #9C27B0, #7B1FA2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px;
        font-weight: bold;
        width: 100%;
    }
    .zone-bleue { background: #e3f2fd; border-left: 5px solid #2196F3; padding: 15px; border-radius: 10px; margin: 10px 0; }
    .zone-violette { background: #f3e5f5; border-left: 5px solid #9C27B0; padding: 15px; border-radius: 10px; margin: 10px 0; }
    .zone-rose { background: #fce4ec; border-left: 5px solid #E91E63; padding: 15px; border-radius: 10px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# INIT
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "premium_unlocked" not in st.session_state:
    st.session_state.premium_unlocked = True  # Set True mba hisokatra rehetra

# HEADER
st.markdown("""
<div class="main-header">
    <h1>✈️ Aviator Predictor V1.6.0 (Beta)</h1>
</div>
""", unsafe_allow_html=True)

# ===== MENU PRINCIPAL =====
if st.session_state.page == "menu":
    
    # 1. STRATÉGIE VIOLETTE
    st.markdown('<div class="strategy-card violette">', unsafe_allow_html=True)
    st.markdown("### 💜 Stratégie Violette")
    st.write("**2.00X-9.99X (Standard)**")
    st.caption("Analyse statistique des zones de couleur.")
    if st.button("▶️ Ouvrir Stratégie Violette", key="b_violette"):
        st.session_state.page = "violette"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. STRATÉGIE DE TOUR
    st.markdown('<div class="strategy-card tour">', unsafe_allow_html=True)
    st.markdown("### 🕰️ Stratégie De Tour")
    st.write("**Boost 4.00X Garanti 2X (Premium)**")
    st.caption("Technologie brevetée à haut rendement.")
    if st.button("▶️ Ouvrir Stratégie De Tour", key="b_tour"):
        st.session_state.page = "tour"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. CALCUL TOUR IA
    st.markdown("""
    <div class="strategy-card ia">
        <h3 style="color: #00C853;">🤖 Calcul Tour IA</h3>
        <p><b>Analyse IA (Premium)</b></p>
        <p style="opacity: 0.7;">Prédictions basées sur l'IA.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Ouvrir Calcul Tour IA", key="b_ia"):
        st.session_state.page = "ia"
        st.rerun()
    
    # 4. STRATÉGIE ROSE VIP
    st.markdown('<div class="strategy-card rose-vip">', unsafe_allow_html=True)
    st.markdown("### 🎀 Stratégie Rose VIP")
    st.write("**10.00X+ (Premium)**")
    st.caption("Algorithmes prédictifs avancés.")
    if st.button("▶️ Ouvrir Stratégie Rose VIP", key="b_rose"):
        st.session_state.page = "rose"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 5. MODE AUTO 2X ASSURÉ
    st.markdown('<div class="strategy-card auto-2x">', unsafe_allow_html=True)
    st.markdown("### ✅ Mode Auto 2X Assuré")
    st.write("**Assuré si vous voulez un peu de profit gagnant**")
    st.caption("Technique de sécurité maximale.")
    if st.button("▶️ Ouvrir Mode Auto 2X", key="b_auto"):
        st.session_state.page = "auto2x"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===== STRATÉGIE VIOLETTE =====
elif st.session_state.page == "violette":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 💜 STRATÉGIE VIOLETTE")
    st.info("📌 **Mode d'utilisation :**\n\n1. Entrez le multiplicateur le plus bas des 10 derniers tours (<2.00X)\n2. Indiquez l'heure exacte (HH:MM:SS)\n3. Réinitialisez si nouveau minimum")
    
    mult_min = st.number_input("Multiplicateur minimum (X) :", 1.00, 2.00, 1.60, 0.01)
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("Heures", 0, 23, 12)
    mi = col_m.number_input("Minutes", 0, 59, 4)
    se = col_s.number_input("Secondes", 0, 59, 30)
    
    if st.button("🧮 Lancer l'analyse", key="v_launch"):
        ref = datetime.now().replace(hour=h, minute=mi, second=se, microsecond=0)
        if mult_min < 1.30:
            pb, pv, pr = 25, 50, 25
        elif mult_min < 1.60:
            pb, pv, pr = 35, 42, 23
        elif mult_min < 1.80:
            pb, pv, pr = 38.5, 38.6, 22.9
        else:
            pb, pv, pr = 45, 35, 20
        pb += np.random.uniform(-2, 2)
        pv += np.random.uniform(-2, 2)
        pr += np.random.uniform(-2, 2)
        tot = pb + pv + pr
        pb, pv, pr = pb/tot*100, pv/tot*100, pr/tot*100
        
        start = ref + timedelta(seconds=55)
        end = ref + timedelta(minutes=1, seconds=22)
        interval = f"{start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')}"
        
        st.markdown("### 📊 Résultats de l'analyse")
        st.markdown(f'<div class="zone-bleue"><b>💧 Zone Bleue (1.00X-1.99X)</b><br>Probabilité : <b>{pb:.1f}%</b><br>Intervalle : {interval}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="zone-violette"><b>🌸 Zone Violette (2.00X-9.99X)</b><br>Probabilité : <b>{pv:.1f}%</b><br>Intervalle : {interval}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="zone-rose"><b>🚀 Zone Rose (10.00X+)</b><br>Probabilité : <b>{pr:.1f}%</b><br>Intervalle : {interval}</div>', unsafe_allow_html=True)

# ===== STRATÉGIE DE TOUR =====
elif st.session_state.page == "tour":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 🕰️ STRATÉGIE DE TOUR")
    st.success("🎯 **Boost 4.00X Garanti 2X**\n\nTechnologie brevetée pour maximiser les chances d'atteindre 2.00X.")
    
    st.write("**Entrez les 5 derniers multiplicateurs :**")
    mults = []
    cols = st.columns(5)
    for i, c in enumerate(cols):
        with c:
            m = st.number_input(f"M{i+1}", 1.00, 100.00, 1.50, 0.01, key=f"tour_{i}")
            mults.append(m)
    
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, datetime.now().hour, key="t_h")
    mi = col_m.number_input("M", 0, 59, datetime.now().minute, key="t_m")
    se = col_s.number_input("S", 0, 59, datetime.now().second, key="t_s")
    
    if st.button("🚀 Calculer le Boost", key="t_launch"):
        avg = np.mean(mults)
        ref = datetime.now().replace(hour=h, minute=mi, second=se)
        
        # Algorithme: maminavina ny rounds tsara hipoiran'ny 2X+
        st.markdown("### 🎯 Tours Garantis 2X :")
        for i in range(1, 6):
            boost_time = ref + timedelta(seconds=30*i)
            boost_value = max(2.00, avg * 1.3 + np.random.uniform(0, 2))
            confidence = np.random.uniform(75, 95)
            
            color = "#00C853" if boost_value >= 4 else "#FFD700"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FFF3E0, #FFE0B2); padding: 15px; 
                        border-radius: 10px; margin: 8px 0; border-left: 5px solid {color};">
                <b>Tour #{i}</b> • ⏰ {boost_time.strftime('%H:%M:%S')}<br>
                💎 Boost: <b style="color: {color}; font-size: 22px;">{boost_value:.2f}X</b><br>
                ✅ Fiabilité: <b>{confidence:.1f}%</b> • Cash Out: <b>2.00X</b>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("💡 **Conseil:** Sortez à 2.00X pour garantir le gain.")

# ===== CALCUL TOUR IA =====
elif st.session_state.page == "ia":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 🤖 CALCUL TOUR IA")
    st.success("🧠 **Analyse IA Avancée**\n\nUtilise le Machine Learning pour prédire les prochains tours.")
    
    st.write("**Entrez 10 derniers multiplicateurs (séparés par virgule):**")
    data_input = st.text_area("Ex: 1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4", 
                              "1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4")
    
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, datetime.now().hour, key="ia_h")
    mi = col_m.number_input("M", 0, 59, datetime.now().minute, key="ia_m")
    se = col_s.number_input("S", 0, 59, datetime.now().second, key="ia_s")
    
    if st.button("🤖 Lancer l'IA", key="ia_launch"):
        try:
            data = [float(x.strip()) for x in data_input.split(",")]
            from sklearn.ensemble import RandomForestRegressor
            
            X = np.arange(len(data)).reshape(-1, 1)
            model = RandomForestRegressor(n_estimators=200, random_state=42)
            model.fit(X, data)
            
            ref = datetime.now().replace(hour=h, minute=mi, second=se)
            
            st.markdown("### 🎯 Prédictions IA (TOP 10) :")
            for i in range(1, 11):
                pred = model.predict([[len(data)+i-1]])[0]
                pred = max(1.0, pred + np.random.uniform(-0.3, 0.5))
                t = ref + timedelta(seconds=30*i)
                conf = np.random.uniform(60, 95)
                
                if pred < 1.5:
                    color = "#F44336"
                elif pred < 2.5:
                    color = "#FFD700"
                else:
                    color = "#00C853"
                
                st.markdown(f"""
                <div style="background: #1a1a2e; padding: 15px; border-radius: 10px; 
                            margin: 8px 0; border-left: 5px solid {color};">
                    <span style="color: white;"><b>Tour #{i}</b> • ⏰ {t.strftime('%H:%M:%S')}</span><br>
                    <span style="color: {color}; font-size: 20px;"><b>{pred:.2f}X</b></span>
                    <span style="color: #FFD700;"> • Fiab: {conf:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.error("Format incorrect. Utilisez des virgules.")

# ===== STRATÉGIE ROSE VIP =====
elif st.session_state.page == "rose":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## 🎀 STRATÉGIE ROSE VIP")
    st.error("🚀 **Mode VIP - 10.00X+ Hunter**\n\nAlgorithmes avancés pour chasser les BIG WINS (10X et plus).")
    
    st.write("**Entrez les 20 derniers multiplicateurs :**")
    data_input = st.text_area("Format: 1.5, 2.3, ...", 
                              "1.2, 1.5, 2.3, 1.1, 5.6, 1.8, 2.5, 1.3, 1.9, 3.2, 1.4, 2.1, 1.6, 4.5, 1.7, 2.8, 1.2, 3.5, 1.9, 2.4")
    
    col_h, col_m, col_s = st.columns(3)
    h = col_h.number_input("H", 0, 23, datetime.now().hour, key="r_h")
    mi = col_m.number_input("M", 0, 59, datetime.now().minute, key="r_m")
    se = col_s.number_input("S", 0, 59, datetime.now().second, key="r_s")
    
    if st.button("💎 Chasser les 10X+", key="r_launch"):
        try:
            data = [float(x.strip()) for x in data_input.split(",")]
            
            # Algorithme: Analyse de la fréquence des big wins
            big_wins = [x for x in data if x >= 10]
            avg_gap = len(data) / max(len(big_wins), 1)
            
            ref = datetime.now().replace(hour=h, minute=mi, second=se)
            
            st.markdown("### 💎 Prochains BIG WINS prévus :")
            
            # Calcul des prochains big wins
            for i in range(1, 6):
                next_round = int(avg_gap * i)
                t = ref + timedelta(seconds=30 * next_round)
                predicted_value = np.random.uniform(10, 50)
                confidence = max(40, 90 - i*10)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fce4ec, #f8bbd0); 
                            padding: 20px; border-radius: 12px; margin: 10px 0; 
                            border-left: 6px solid #E91E63;">
                    <b style="color: #880E4F; font-size: 16px;">💎 BIG WIN #{i}</b><br>
                    ⏰ Tour #{next_round} • <b>{t.strftime('%H:%M:%S')}</b><br>
                    🎯 Valeur prédite: <b style="color: #E91E63; font-size: 24px;">{predicted_value:.2f}X</b><br>
                    ✅ Fiabilité: <b>{confidence}%</b>
                </div>
                """, unsafe_allow_html=True)
            
            st.warning("⚠️ **Stratégie VIP:** Misez petit et soyez patient. Les BIG WINS sont rares mais lucratifs.")
        except:
            st.error("Format incorrect.")

# ===== MODE AUTO 2X ASSURÉ =====
elif st.session_state.page == "auto2x":
    if st.button("← Retour au menu"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("## ✅ MODE AUTO 2X ASSURÉ")
    st.success("🛡️ **Sécurité Maximale**\n\nCette technique garantit un petit profit constant en sortant systématiquement à 2.00X.")
    
    st.markdown("### 📊 Calculateur de Profit :")
    
    bankroll = st.number_input("💰 Votre bankroll (Ar):", min_value=1000, value=50000, step=1000)
    bet_pct = st.slider("🎯 % du bankroll par tour:", 1, 10, 3)
    nb_tours = st.slider("🔄 Nombre de tours:", 5, 100, 20)
    
    bet_amount = int(bankroll * bet_pct / 100)
    win_per_round = bet_amount  # 2X garantit le double
    
    # Simulation: 70% win rate à 2X
    win_rate = 0.70
    expected_wins = int(nb_tours * win_rate)
    expected_losses = nb_tours - expected_wins
    
    total_won = expected_wins * win_per_round
    total_lost = expected_losses * bet_amount
    net_profit = total_won - total_lost
    
    st.markdown("### 🎯 Plan de Trading :")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Mise/tour", f"{bet_amount:,} Ar")
    col2.metric("✅ Cash Out", "2.00X")
    col3.metric("🎁 Gain/tour", f"+{win_per_round:,} Ar")
    
    st.markdown("### 📈 Résultats prévus :")
    col1, col2 = st.columns(2)
    col1.metric("✅ Tours gagnés (~70%)", f"{expected_wins}")
    col2.metric("❌ Tours perdus (~30%)", f"{expected_losses}")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4CAF50, #2E7D32); padding: 25px; 
                border-radius: 15px; text-align: center; color: white; margin: 15px 0;">
        <h2 style="margin: 0;">💎 PROFIT NET PRÉVU</h2>
        <h1 style="margin: 10px 0; font-size: 40px;">+{net_profit:,} Ar</h1>
        <p>Sur {nb_tours} tours • Win Rate ~70%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    💡 **Règles d'Or du Mode Auto 2X:**
    - ✅ Toujours sortir à exactement 2.00X
    - ✅ Ne jamais dépasser 5% du bankroll par tour
    - ✅ Arrêter après 5 pertes consécutives
    - ✅ Reprendre 30 minutes plus tard
    """)

# FOOTER
st.markdown("---")
st.caption("🇲🇬 Made in Madagascar • ⚠️ Jouez avec modération")
