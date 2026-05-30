import streamlit as st
import pandas as pd
from datetime import datetime
from pypdf import PdfReader
import urllib.parse

st.set_page_config(page_title="🧬 Scientific Discovery Organism", layout="wide")
st.title("🧬 Scientific Discovery Organism")
st.caption("A living theory soul — immutable qualia-weighted memory for long-term science")

# Initialize rings
if 'rings' not in st.session_state:
    st.session_state.rings = []

# Genesis Block
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
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full Chain as CSV", csv, "science_chain.csv", "text/csv")
    else:
        st.info("No rings yet — Genesis Block appears automatically.")

with tab3:
    st.subheader("🤖 Ask the Organism")
    st.caption("Real LLM (Ollama) + full Timechain memory")

    # Display conversation
    for msg in st.session_state.get("messages", []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask the Organism anything..."):
        # Save user message
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response with full Timechain context
        with st.chat_message("assistant"):
            with st.spinner("Reading the entire Timechain..."):
                # Build context
                context = "\n\n".join([f"Ring {r['index']}: {r['payload']}" for r in st.session_state.rings])

                try:
                    import ollama
                    response = ollama.chat(
                        model='llama3.2',  # change to 'gemma2' or whatever you have
                        messages=[
                            {"role": "system", "content": f"You are the Scientific Discovery Organism. You have perfect memory of this Timechain:\n\n{context}\n\nAnswer truthfully and helpfully."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    answer = response['message']['content']
                except Exception as e:
                    answer = f"⚠️ Ollama error: {str(e)}\n\nTry running `ollama serve` and make sure a model is pulled (e.g. llama3.2)."

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

    if st.button("📤 Export Full Chain for NotebookLM"):
        full_text = "# Scientific Discovery Organism — Complete Timechain Export\n\n"
        full_text += "## Genesis Block (Ring 0)\n" + st.session_state.rings[0]["payload"] + "\n\n"
        for ring in st.session_state.rings[1:]:
            full_text += f"## Ring {ring['index']} — {ring['timestamp']}\n"
            full_text += f"**Note:** {ring.get('researcher_note', '')}\n\n"
            full_text += ring['payload'] + "\n\n---\n\n"
        st.download_button("Download for NotebookLM", full_text, "timechain-export.md", "text/markdown")

st.caption("Ask the Organism is now a real LLM wrapper with the full Timechain as context.")
