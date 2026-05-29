import streamlit as st
from science_organism import ScientificTimechain, LabSensor
import pandas as pd
from datetime import datetime
from pypdf import PdfReader

st.set_page_config(page_title="🧬 Scientific Discovery Organism", layout="wide")
st.title("🧬 Scientific Discovery Organism")
st.caption("A living theory soul — immutable qualia-weighted memory for long-term science")

tc = ScientificTimechain("science_timechain.db")

st.subheader("Propose New Ring")
content = st.text_area("Core insight / result / intuition", height=150)

uploaded_file = st.file_uploader("📎 Attach PDF manuscript or research (optional)", type=["pdf"])

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
    experiment_data = {"p_value": 0.03, "effect_size": 1.2, "replicated": False, "researcher_note": researcher_note}
    proposal = tc.propose_scientific_ring(final_content, experiment_data)
    tc.append(final_content, vision=proposal.get("vision"), sensor=LabSensor())
    st.success("✅ Ring sealed forever!")
    st.rerun()

st.divider()

st.subheader("Living Timeline")
rings = [r.to_dict() for r in tc] if hasattr(tc, "__iter__") else []
if rings:
    df = pd.DataFrame(rings)
    st.dataframe(df[["index", "timestamp", "payload"]], use_container_width=True)
else:
    st.info("No rings yet — propose the first one above!")
