import streamlit as st
import random
import time

# Endriky ny pejy
st.set_page_config(page_title="Predictor VIP", page_icon="💰")

# Styliste kely amin'ny CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 Predictor Web App")
st.subheader("Aviator & Mega Wheel")

# Safidy lalao
game = st.radio("Safidio ny lalao:", ["Aviator ✈️", "Mega Wheel 🎡"], horizontal=True)

if game == "Aviator ✈️":
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Aviator_Logo.png/640px-Aviator_Logo.png", width=100)
    st.write("---")
    if st.button("FAHITA SIGNAL (NEXT)"):
        with st.spinner('Mandinika ny algorithm...'):
            time.sleep(2)
            prediction = round(random.uniform(1.10, 5.50), 2)
            st.metric(label="Cote azo antoka", value=f"{prediction}x")
            st.success("Miloka dieny izao!")

else:
    st.write("🎡 **Mega Wheel Predictor**")
    st.write("---")
    numbers = [1, 2, 5, 8, 10, 15, 20, 30, 40]
    if st.button("HINANY ISA MANARAKA"):
        with st.spinner('Mikajy ny probability...'):
            time.sleep(2)
            res = random.choice(numbers)
            st.info(f"Isa mety hivoaka: {res}")

st.write("---")
st.caption("Fanamarihana: Ity app ity dia simulation fotsiny. Ampiasao am-pahendrena.")
