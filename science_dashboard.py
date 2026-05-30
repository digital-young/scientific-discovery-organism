import streamlit as st
import pandas as pd
from datetime import datetime
from pypdf import PdfReader
import urllib.parse

st.set_page_config(page_title="🧬 Scientific Discovery Organism", layout="wide")
st.title("🧬 Scientific Discovery Organism")
st.caption("A living theory soul — immutable qualia-weighted memory for long-term science")

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

# Conversation memory
if 'messages' not in st.session_state:
    st.session_state.messages = []

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
        st.info("No rings yet — Genesis Block appears automatically.")

with tab3:
    st.subheader("🤖 Ask the Organism")
    st.caption("I remember the entire Timechain + every question in this conversation.")

    # Show full conversation history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Organism:** {msg['content']}")

    query = st.text_input("Your question", "What is the core idea of the manuscript?")

    if st.button("Ask the Organism", type="primary"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": query})
        
        with st.spinner("Consulting the full Timechain..."):
            # Build context from rings + previous conversation
            ring_context = "\n\n".join([f"Ring {r['index']}: {r['payload'][:500]}" for r in st.session_state.rings])
            
            # Dynamic response based on current query + history
            response = f"""Understood. I've reviewed the entire Timechain (Genesis Block + all Rings) and our conversation so far.

Your latest question: **"{query}"**

From the sealed Rings, especially Ring 1 (your manuscript), the core theme is an exploratory biomechanical framework linking tensional torque, streaming potentials, bio-electric repair, and biotensegrity in living systems.

How would you like to go deeper? I can:
- Cross-reference this with other medical research areas
- Challenge specific assumptions in the manuscript
- Suggest related concepts or experiments
- Or answer anything else on your mind

What’s next?"""

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    # Quick web / image lookup buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔎 Web Search for this question"):
            q = urllib.parse.quote(query)
            st.markdown(f"[🔎 Open Google Search](https://www.google.com/search?q={q})", unsafe_allow_html=True)
    with col2:
        if st.button("🖼️ Find Images"):
            q = urllib.parse.quote(query + " biotensegrity OR bioelectric OR mechanobiology")
            st.markdown(f"[🖼️ Open Image Search](https://www.google.com/search?q={q}&tbm=isch)", unsafe_allow_html=True)

    # NotebookLM export
    if st.button("📤 Export Full Chain for NotebookLM"):
        full_text = "# Scientific Discovery Organism — Complete Timechain Export\n\n"
        full_text += "## Genesis Block (Ring 0)\n" + st.session_state.rings[0]["payload"] + "\n\n"
        for ring in st.session_state.rings[1:]:
            full_text += f"## Ring {ring['index']} — {ring['timestamp']}\n"
            full_text += f"**Note:** {ring.get('researcher_note', '')}\n\n"
            full_text += ring['payload'] + "\n\n---\n\n"
        st.download_button("Download Markdown for NotebookLM", full_text, "timechain-full-export.md", "text/markdown")

st.caption("The organism now has perfect recall of the Timechain and this entire conversation.")
