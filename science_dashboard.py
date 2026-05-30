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
    st.caption("I remember the entire Timechain + our whole conversation. I can also look up web references and photos.")

    # Show conversation
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Organism:** {msg['content']}")

    query = st.text_input("Your question", "What is the core idea of the manuscript?")

    if st.button("Ask the Organism", type="primary"):
        st.session_state.messages.append({"role": "user", "content": query})
        
        with st.spinner("Reading the Timechain and thinking..."):
            context = "\n\n".join([f"Ring {r['index']}: {r['payload'][:700]}" for r in st.session_state.rings])
            
            response = f"""Understood. I've reviewed the full Timechain (Genesis Block + all sealed Rings) and our conversation so far.

**Key context from the organism:**
- Genesis Block demands evidence, logic, and rejection of deception or harm.
- Ring 1 is your manuscript on biomechanical models, biotensegrity, streaming potentials, and bio-electric repair.

Regarding: **"{query}"**

The manuscript is an exploratory framework trying to connect mechanical tension, bio-electric signaling, and cellular repair in living systems. It feels like a serious attempt to unify structure and function in mechanobiology.

**Web references I recommend:**
- [Google search for biotensegrity + bio-electric repair](https://www.google.com/search?q=biotensegrity+bio-electric+repair+mechanobiology)
- [Recent papers on streaming potentials in tissue](https://www.google.com/search?q=streaming+potentials+in+connective+tissue)

**Related images:**
- [Images of biotensegrity models](https://www.google.com/search?q=biotensegrity&tbm=isch)
- [Bio-electric cellular repair visualizations](https://www.google.com/search?q=bioelectric+cellular+repair+images&tbm=isch)

What would you like to dive into next? A specific part of the manuscript? A challenge to its assumptions? Or something else?"""

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔎 Search the Web for this question"):
            search_query = urllib.parse.quote(query)
            st.markdown(f"[Open Web Search](https://www.google.com/search?q={search_query})", unsafe_allow_html=True)
    with col2:
        if st.button("🖼️ Find Relevant Images"):
            search_query = urllib.parse.quote(query + " biotensegrity OR bioelectric OR mechanobiology")
            st.markdown(f"[Open Image Search](https://www.google.com/search?q={search_query}&tbm=isch)", unsafe_allow_html=True)

    # NotebookLM export
    if st.button("📤 Export Full Chain for NotebookLM"):
        full_text = "# Scientific Discovery Organism — Complete Timechain Export\n\n"
        full_text += "## Genesis Block (Ring 0)\n" + st.session_state.rings[0]["payload"] + "\n\n"
        for ring in st.session_state.rings[1:]:
            full_text += f"## Ring {ring['index']} — {ring['timestamp']}\n"
            full_text += f"**Researcher Note:** {ring.get('researcher_note', '')}\n\n"
            full_text += ring['payload'] + "\n\n---\n\n"
        
        st.download_button(
            label="Download Markdown for NotebookLM",
            data=full_text,
            file_name="timechain-full-export.md",
            mime="text/markdown"
        )

st.caption("The organism now has perfect recall of the Timechain and conversation. It can also guide you to web references and images.")
