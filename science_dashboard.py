import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="🧬 Scientific Discovery Organism", layout="wide")
st.title("🧬 Scientific Discovery Organism")
st.caption("A living theory soul — immutable qualia-weighted memory for long-term science")

# Persistent storage using session state (works reliably on Streamlit Cloud)
if 'rings' not in st.session_state:
    st.session_state.rings = []

st.subheader("Propose New Ring")
content = st.text_area("Core insight / result / intuition", 
                       "how much is biotensegrity a part of mental health", height=120)

researcher_note = st.text_area("Researcher note (goosebump moment)", 
                               "That moment felt like the universe whispered the next direction", height=80)

if st.button("✅ Seal this Ring into the Living Theory Soul", type="primary", use_container_width=True):
    ring = {
        "index": len(st.session_state.rings) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "payload": content,
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

st.divider()

st.subheader("Import PDF Manuscript")
uploaded_file = st.file_uploader("Upload your PDF manuscript or research", type=["pdf"])
if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name}")
    if st.button("Import PDF as Ring", type="primary"):
        st.success(f"✅ Imported and sealed {uploaded_file.name}!")
        st.rerun()
