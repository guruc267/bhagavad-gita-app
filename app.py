import streamlit as st
from utils.pdf_reader import extract_pages
from utils.hf_llm import get_telugu_bhavam
from utils.audio_utils import generate_audio

st.set_page_config(
    page_title="Bhagavad Gita",
    layout="centered"
)

# Load CSS
with open("assets/book.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center'>📘 Bhagavad Gita</h2>", unsafe_allow_html=True)

pages = extract_pages("data/gita.pdf")

if "page" not in st.session_state:
    st.session_state.page = 0

page = st.session_state.page

# Show page content
st.markdown(f"<div class='book'>{pages[page]}</div>", unsafe_allow_html=True)

if st.button("📖 Explain Bhavam in Telugu"):
    with st.spinner("భావం రూపొందుతోంది..."):
        bhavam = get_telugu_bhavam(pages[page])
        st.markdown("### 📜 తెలుగు భావం")
        st.write(bhavam)

        generate_audio(bhavam, "audio.mp3")
        st.audio("audio.mp3")

col1, col2 = st.columns(2)
if col1.button("⬅️ Previous"):
    st.session_state.page = max(0, page - 1)

if col2.button("➡️ Next"):
    st.session_state.page = min(len(pages) - 1, page + 1)

