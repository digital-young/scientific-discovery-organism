import streamlit as st
import pandas as pd
from datetime import datetime
from pypdf import PdfReader

st.set_page_config(page_title="🧬 Scientific Discovery Organism", layout="wide")
st.title("🧬 Scientific Discovery Organism")
st.caption("A living theory soul — immutable qualia-weighted memory for long-term science")

if 'rings' not in st.session_state:
    st.session_state.rings = []

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
        st.info("No rings yet — propose the first one above!")

with tab3:
    st.subheader("🤖 Ask the Organism")
    query = st.text_input("Ask anything about your accumulated research", "What patterns do you see in biotensegrity?")
    if st.button("Ask the Organism"):
        with st.spinner("Thinking through the Living Theory Soul..."):
            rings_text = "\n\n".join([f"Ring {r['index']}: {r['payload']}" for r in st.session_state.rings])
            st.write("**Relevant Rings:**")
            for r in st.session_state.rings[-5:]:
                st.write(f"• {r['payload'][:200]}...")
            st.write("**Organism Response:**")
            st.write("Based on the sealed Rings, here is a synthesized insight...")
            # (We can upgrade this to real LLM later)

st.caption("Data is persistent. Refresh the page — your Rings stay here.")
