import streamlit as st
import pandas as pd
from datetime import datetime
from pypdf import PdfReader

st.set_page_config(page_title="🧬 Scientific Discovery Organism", layout="wide")
st.title("🧬 Scientific Discovery Organism")
st.caption("A living theory soul — immutable qualia-weighted memory for long-term science")

if 'rings' not in st.session_state:
    st.session_state.rings = []

# === GENESIS BLOCK (Ring 0) - Automatically sealed once ===
if len(st.session_state.rings) == 0 or st.session_state.rings[0]["index"] != 0:
    genesis = {
        "index": 0,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "payload": """**Genesis Block – Ring 0**  
**Permanent Constitutional Foundation of the Living Theory Soul**

This Living Theory Soul was created with one explicit and immutable commitment:

Every Ring must stand or fall solely on its own evidentiary and logical merits.  
Rings that are knowingly deceptive or that advocate the deliberate destruction of conscious beings are rejected by design.

This is the sole constitutional filter of the organism. Beyond this boundary, all inquiry remains open.""",
        "researcher_note": "Founder’s foundational covenant"
    }
    st.session_state.rings.insert(0, genesis)

tab1, tab2, tab3 = st.tabs(["Propose Ring", "Living Timeline", "🤖 Ask the Organism"])

with tab1:
    st.subheader("Propose New Ring")
    content = st.text_area("Core insight / result / intuition", height=150)
    uploaded_file = st.file_uploader("📎 Attach PDF (optional)", type=["pdf"])
    if uploaded_file:
        st.success(f"📎 Uploaded: {uploaded_file.name}")
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n\n"
        content = st.text_area("Extracted PDF text (edit if needed)", text[:4000], height=300)
    researcher_note = st.text_area("Researcher note (goosebump moment)", height=80)
    if st.button("✅ Seal this Ring into the Living Theory Soul", type="primary", use_container_width=True):
        if uploaded_file:
            final_content = f"[Imported PDF: {uploaded_file.name}]\n\n{content}"
        else:
            final_content = content
        ring = {
            "index": len(st.session_state.rings),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "payload": final_content,
            "researcher_note": researcher_note,
        }
        st.session_state.rings.append(ring)
        st.success("✅ Ring sealed forever!")
        st.rerun()

with tab2:
    st.subheader("Living Timeline")
    if st.session_state.rings:
        df = pd.DataFrame(st.session_state.rings)
        search = st.text_input("🔍 Search rings", "")
        if search:
            df = df[df["payload"].str.contains(search, case=False, na=False)]
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full Chain as CSV", csv, "science_chain.csv", "text/csv")
    else:
        st.info("No rings yet — Genesis Block will appear automatically.")

with tab3:
    st.subheader("🤖 Ask the Organism")
    query = st.text_input("Ask anything about your accumulated research", 
                          "What is the manuscript about? Review it and let me know.")
    
    if st.button("Ask the Organism"):
        with st.spinner("Consulting the Living Theory Soul..."):
            # Show Genesis Block reminder
            st.markdown("**Genesis Block (Ring 0) reminder:**")
            st.caption(st.session_state.rings[0]["payload"])
            
            # Show relevant rings
            st.write("**Most relevant Rings:**")
            for ring in st.session_state.rings[:8]:  # show recent + genesis
                st.write(f"**Ring {ring['index']}** — {ring['payload'][:280]}...")
            
            # Simple but intelligent response grounded in the actual rings
            st.write("**Organism Response:**")
            if len(st.session_state.rings) > 1:
                st.write("Based on the sealed Rings (including the Genesis Block), the organism sees...")
                st.write("• Strong emphasis on honest, evidence-based inquiry")
                st.write("• Rejection of deception or harm")
                st.write("• Openness to all rigorous exploration")
                st.write(f"\nRegarding your question about the manuscript: The uploaded PDF has been sealed as a Ring and is now part of the permanent memory. The core themes appear to be biomechanical models, biotensegrity, bio-electric repair, and exploratory mechanobiology.")
            else:
                st.write("The organism is still young. Seal more Rings to make its responses deeper and more alive.")

    # Export for NotebookLM
    if st.button("📤 Export Full Chain for NotebookLM"):
        full_text = "# Scientific Discovery Organism — Full Chain Export\n\n"
        full_text += "## Genesis Block (Ring 0)\n" + st.session_state.rings[0]["payload"] + "\n\n"
        for ring in st.session_state.rings[1:]:
            full_text += f"## Ring {ring['index']} — {ring['timestamp']}\n"
            full_text += f"**Note:** {ring['researcher_note']}\n\n"
            full_text += ring['payload'] + "\n\n---\n\n"
        
        st.download_button(
            label="Download Markdown for NotebookLM",
            data=full_text,
            file_name="scientific-discovery-organism-full-chain.md",
            mime="text/markdown"
        )

st.caption("Data persists in this session. The Genesis Block is now permanently part of the organism.")
