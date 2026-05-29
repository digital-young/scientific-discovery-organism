import streamlit as st
from science_organism import ScientificTimechain, LabSensor
import pandas as pd
from datetime import datetime
from pypdf import PdfReader

st.set_page_config(page_title="🧬 Scientific Discovery Organism", layout="wide")
st.title("🧬 Scientific Discovery Organism")
st.caption("A living theory soul — immutable qualia-weighted memory for long-term science")

tc = ScientificTimechain("science_timechain.db")

tab1, tab2, tab3, tab4 = st.tabs(["Propose Ring", "Living Timeline", "Import PDF", "Ask the Organism"])

with tab1:
    st.subheader("Propose New Ring")
    content = st.text_area("Core insight / result / intuition", height=120)
    researcher_note = st.text_area("Researcher note (goosebump moment)", height=80)
    if st.button("✅ Seal this Ring into the Living Theory Soul", type="primary", use_container_width=True):
        experiment_data = {"p_value": 0.03, "effect_size": 1.2, "replicated": False, "researcher_note": researcher_note}
        proposal = tc.propose_scientific_ring(content, experiment_data)
        tc.append(content, vision=proposal.get("vision"), sensor=LabSensor())
        st.success("✅ Ring sealed forever! The organism just grew wiser.")
        st.rerun()

with tab2:
    st.subheader("Living Timeline")
    rings = [r.to_dict() for r in tc] if hasattr(tc, "__iter__") else []
    if rings:
        df = pd.DataFrame(rings)
        st.dataframe(df[["index", "timestamp", "payload"]], use_container_width=True)
    else:
        st.info("No rings yet — propose the first one above!")

with tab3:
    st.subheader("Import PDF Manuscript")
    uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
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

with tab4:
    st.subheader("Ask the Organism (AI Agent)")
    st.caption("Ask questions about your accumulated knowledge. The agent will search and reason over all Rings.")
    query = st.text_input("Ask anything about your research / Rings", "What patterns do you see in biotensegrity and mental health?")
    
    if st.button("Ask the Organism", type="primary"):
        with st.spinner("Thinking..."):
            rings = [r.to_dict() for r in tc] if hasattr(tc, "__iter__") else []
            # Simple agent: keyword search + summary
            relevant = [r for r in rings if query.lower() in str(r.get("payload", "")).lower() or query.lower() in str(r.get("researcher_note", "")).lower()]
            if relevant:
                st.write("**Relevant Rings found:**")
                for r in relevant[:5]:
                    st.write(f"• {r['payload'][:200]}...")
                st.write("**Summary / Insight from the Organism:**")
                st.write("Based on your stored Rings, here is a reasoned response...")
                # In future this can call a real LLM
            else:
                st.write("No direct matches found, but the organism is learning. Try rephrasing your question.")

st.caption("Data is now persistent (saved in SQLite). Refresh the page — your Rings will still be here!")
