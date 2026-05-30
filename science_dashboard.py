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
content = st.text_area("Core insight / result / intuition", height=150)

uploaded_file = st.file_uploader("📎 Attach PDF (optional)", type=["pdf"])

if uploaded_file:
    st.success(f"📎 Uploaded: {uploaded_file.name}")
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    content = st.text_area("Extracted PDF text (edit if needed)", text[:4000], height=300)

researcher_note = st.text_area("Researcher note (goosebump moment)", height=80)

if st.button("✅ Seal this Ring into the Living Theory Soul", type="primary", use_container_width=True):
    if uploaded_file:
        final_content = f"[Imported PDF: {uploaded_file.name}]\n\n{content}"
    else:
        final_content = content
    ring = {
        "index": len(st.session_state.rings) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "payload": final_content,
        "researcher_note": researcher_note,
    }
    st.session_state.rings.append(ring)
    st.success("✅ Ring sealed forever! The organism just grew wiser.")
    st.rerun()

st.divider()
st.subheader("Living Timeline")
if st.session_state.rings:
    df = pd.DataFrame(st.session_state.rings)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No rings yet — propose the first one above!")
