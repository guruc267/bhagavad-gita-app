import streamlit as st
import json
import os

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="భగవద్గీత",
    page_icon="📘",
    layout="centered"
)

# -------------------------
# Session state for page turn
# -------------------------
if "sloka_index" not in st.session_state:
    st.session_state.sloka_index = 0

# -------------------------
# Load CSS (temple / book UI)
# -------------------------
with open("assets/book.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------
# Load Gita JSON
# -------------------------
with open("data/gita_6_to_10.json", "r", encoding="utf-8") as f:
    gita = json.load(f)

# -------------------------
# App title
# -------------------------
st.markdown(
    "<h1 style='text-align:center;'>📘 భగవద్గీత</h1>",
    unsafe_allow_html=True
)

# -------------------------
# Chapter selection
# -------------------------
chapter_key = st.selectbox(
    "అధ్యాయం ఎంచుకోండి",
    sorted(gita.keys(), key=int),
    format_func=lambda x: f"{x}. {gita[x]['name']}"
)

chapter = gita[chapter_key]
slokas = chapter["slokas"]

# Reset page when chapter changes
if st.session_state.get("last_chapter") != chapter_key:
    st.session_state.sloka_index = 0
    st.session_state.last_chapter = chapter_key

# -------------------------
# Sloka navigation (book style)
# -------------------------
sloka_keys = sorted(slokas.keys(), key=int)
sloka_key = sloka_keys[st.session_state.sloka_index]
sloka_data = slokas[sloka_key]
audio_path = sloka_data["audio"]

# -------------------------
# Display Slokam (Sanskrit)
# -------------------------
st.markdown("## 🕉️ శ్లోకం")
st.markdown(
    f"<pre class='slokam-box'>{sloka_data['sanskrit']}</pre>",
    unsafe_allow_html=True
)

# -------------------------
# Telugu meaning
# -------------------------
st.markdown("## 📖 తెలుగు అర్థం")
st.write(sloka_data["telugu"])

# -------------------------
# Bhavam
# -------------------------
st.markdown("## 📜 భావం")
st.write(sloka_data["bhavam"])

# -------------------------
# Audio playback
# -------------------------
st.markdown("## 🔊 శ్రవణం")
if os.path.exists(audio_path):
    st.audio(audio_path)
else:
    st.info("🔊 ఈ శ్లోకానికి రికార్డింగ్ ఇంకా అందుబాటులో లేదు.")

# -------------------------
# Page turn controls
# -------------------------
st.markdown("<hr>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ ముందు"):
        if st.session_state.sloka_index > 0:
            st.session_state.sloka_index -= 1
            st.rerun()

with col2:
    st.markdown(
        f"<p style='text-align:center;'>శ్లోకం {sloka_key} / {len(sloka_keys)}</p>",
        unsafe_allow_html=True
    )

with col3:
    if st.button("తర్వాత ➡️"):
        if st.session_state.sloka_index < len(sloka_keys) - 1:
            st.session_state.sloka_index += 1
            st.rerun()

# -------------------------
# Admin section (MP3 upload)
# -------------------------
with st.expander("🔐 Admin (రికార్డింగ్ అప్లోడ్)"):
    admin_key = st.text_input("Admin Key", type="password")

    if admin_key == st.secrets.get("ADMIN_KEY"):
        uploaded_file = st.file_uploader(
            "🎙️ MP3 రికార్డింగ్ అప్లోడ్ చేయండి",
            type=["mp3"]
        )

        if uploaded_file is not None:
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)

            with open(audio_path, "wb") as f:
                f.write(uploaded_file.read())

            st.success("✅ రికార్డింగ్ విజయవంతంగా సేవ్ చేయబడింది.")
            st.audio(audio_path)

    elif admin_key:
        st.error("❌ తప్పు Admin Key")
