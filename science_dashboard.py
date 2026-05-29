import streamlit as st
import pandas as pd
from datetime import datetime
from pypdf import PdfReader

st.set_page_config(page_title="🧬 Scientific Discovery Organism", layout="wide")
st.title("🧬 Scientific Discovery Organism")
st.caption("A living theory soul — immutable qualia-weighted memory for long-term science")

if 'rings' not in st.session_state:
    st.session_state.rings = []

st.subheader("Propose New Ring")
content = st.text_area("Core insight / result / intuition", "how much is biotensegrity a part of mental health", height=120)
researcher_note = st.text_area("Researcher note", "That moment felt like the universe whispered the next direction", height=80)

if st.button("✅ Seal this Ring into the Living Theory Soul", type="primary", use_container_width=True):
    ring = {
        "index": len(st.session_state.rings) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "payload": content,
        "researcher_note": researcher_note,
    }
    st.session_state.rings.append(ring)
    st.success("✅ Ring sealed forever!")
    st.rerun()

st.divider()

st.subheader("Living Timeline")
if st.session_state.rings:
    df = pd.DataFrame(st.session_state.rings)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No rings yet — propose the first one above!")

st.divider()

st.subheader("Import PDF Manuscript")
uploaded_file = st.file_uploader("Upload your PDF manuscript", type=["pdf"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    edited_text = st.text_area("Extracted text (edit if needed)", text[:4000], height=300)
    
    # Simple button in main flow
    if st.button("✅ Import PDF as Ring", type="primary", use_container_width=True):
        ring = {
            "index": len(st.session_state.rings) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "payload": f"[Imported PDF: {uploaded_file.name}]\n\n{edited_text}",
            "researcher_note": f"Imported from {uploaded_file.name}"
        }
        st.session_state.rings.append(ring)
        st.success(f"✅ Successfully imported {uploaded_file.name} as Ring!")
        st.rerun()
