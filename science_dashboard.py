import streamlit as st
from science_organism import ScientificTimechain, LabSensor
import pandas as pd
from datetime import datetime
from pypdf import PdfReader

st.set_page_config(page_title="🧬 Scientific Discovery Organism", layout="wide")
st.title("🧬 Scientific Discovery Organism")
st.caption("A living theory soul — immutable qualia-weighted memory for long-term science")

tc = ScientificTimechain("science_timechain.db")

# ====================== PROPOSE RING ======================
st.subheader("Propose New Ring")
content = st.text_area("Core insight / result / intuition", height=120)
researcher_note = st.text_area("Researcher note (goosebump moment)", height=80)

if st.button("✅ Seal this Ring into the Living Theory Soul", type="primary", use_container_width=True):
    experiment_data = {
        "p_value": 0.03,
        "effect_size": 1.2,
        "replicated": False,
        "researcher_note": researcher_note,
    }
    proposal = tc.propose_scientific_ring(content, experiment_data)
    tc.append(content, vision=proposal.get("vision"), sensor=LabSensor())
    st.success("✅ Ring sealed forever! The organism just grew wiser.")
    st.rerun()

st.divider()

# ====================== LIVING TIMELINE ======================
st.subheader("Living Timeline")
rings = [r.to_dict() for r in tc] if hasattr(tc, "__iter__") else []
if rings:
    df = pd.DataFrame(rings)
    st.dataframe(df[["index", "timestamp", "payload"]], use_container_width=True)
else:
    st.info("No rings yet — propose the first one above!")

st.divider()

# ====================== IMPORT PDF ======================
st.subheader("Import PDF Manuscript")
uploaded_file = st.file_uploader("Upload your PDF manuscript or research", type=["pdf"])

if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name}")
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    edited_text = st.text_area("Extracted text (edit if needed)", text[:4000], height=300)
    
    if st.button("✅ Import PDF as Ring", type="primary", use_container_width=True):
        content = f"[Imported PDF: {uploaded_file.name}]\n\n{edited_text}"
        experiment_data = {"p_value": None, "effect_size": None, "replicated": False, "researcher_note": f"Imported from {uploaded_file.name}"}
        proposal = tc.propose_scientific_ring(content, experiment_data)
        tc.append(content, vision=proposal.get("vision"), sensor=LabSensor())
        st.success(f"✅ Imported and sealed {uploaded_file.name}!")
        st.rerun()

st.divider()
st.caption("Data is now saved permanently in science_timechain.db. Refresh the page — your Rings will still be here!")
