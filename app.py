import streamlit as st
import json
from utils.hf_llm import get_telugu_bhavam
from utils.audio_utils import generate_audio

st.set_page_config(page_title="Bhagavad Gita", layout="centered")

with open("data/gita_6_to_10.json", "r", encoding="utf-8") as f:
    gita = json.load(f)

st.title("📘 Bhagavad Gita")

chapter = st.selectbox(
    "అధ్యాయం ఎంచుకోండి",
    sorted(gita.keys(), key=int),
    format_func=lambda x: f"{x}. {gita[x]['name']}"
)

sloka = st.selectbox(
    "శ్లోకం ఎంచుకోండి",
    sorted(gita[chapter]["slokas"].keys(), key=int)
)

sloka_data = gita[chapter]["slokas"][sloka]

st.markdown("### 🕉️ శ్లోకం")
st.write(sloka_data["telugu"])

if st.button("📖 తెలుగు భావం వివరించు"):
    with st.spinner("భావం రూపొందుతోంది..."):
        bhavam = get_telugu_bhavam(sloka_data["telugu"])
        st.markdown("### 📜 భావం")
        st.write(bhavam)

        generate_audio(bhavam, "audio.mp3")
        st.audio("audio.mp3")
