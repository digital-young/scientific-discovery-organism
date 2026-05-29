import streamlit as st
from science_organism import ScientificTimechain, LabSensor
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="🧬 Scientific Discovery Organism", layout="wide")
st.title("🧬 Scientific Discovery Organism")
st.caption("A living theory soul — immutable qualia-weighted memory for long-term science")

with st.sidebar:
    st.header("Chain Control")
    db_path = st.text_input("Chain file", "science_timechain.db")
    if st.button("🔀 New Hypothesis Fork"):
        tc = ScientificTimechain(db_path)
        tc.fork_hypothesis(st.text_input("Hypothesis name", "quantum_gravity_alternative"))
        st.rerun()

tc = ScientificTimechain(db_path)

tab1, tab2, tab3 = st.tabs(["Propose Ring", "Living Timeline", "Import/Export"])

with tab1:
    st.subheader("Propose Scientific Ring")
    content = st.text_area("Core insight / result / intuition", "The null result still carried a strong qualia of directionality...")
    col1, col2 = st.columns(2)
    with col1:
        p_value = st.number_input("p-value", 0.0, 1.0, 0.03, step=0.001)
        effect_size = st.number_input("Effect size", 0.0, 5.0, 1.2)
    with col2:
        replicated = st.checkbox("Replicated by another lab")
        researcher_note = st.text_area("Researcher note (goosebump moment)", "That moment felt like the universe whispered the next direction", height=100)

    if st.button("✨ Auto-generate researcher note (Ollama - local only)"):
        try:
            import ollama
            response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": f"Turn this lab result into a vivid goosebump researcher note: p={p_value}, effect={effect_size}, insight={content}"}])
            researcher_note = response['message']['content']
            st.success("Ollama note generated!")
        except:
            st.warning("Ollama only works locally. On Streamlit Cloud it is disabled.")

    experiment_data = {
        "p_value": p_value,
        "effect_size": effect_size,
        "replicated": replicated,
        "researcher_note": researcher_note,
    }

    if st.button("Propose Ring → PoQ Check"):
        proposal = tc.propose_scientific_ring(content, experiment_data)
        st.json(proposal)
        if st.button("✅ Seal this Ring into the Living Theory Soul"):
            tc.append(content, vision=proposal.get("vision"), sensor=LabSensor())
            st.success("Ring sealed forever! The organism just grew wiser.")
            st.rerun()

with tab2:
    st.subheader("Living Timeline + Search & Filter")
    
    rings = [r.to_dict() for r in tc] if hasattr(tc, "__iter__") else []
    
    if rings:
        df = pd.DataFrame(rings)
        
        # Search & Filter
        search_term = st.text_input("🔍 Search rings (content or note)", "")
        if search_term:
            df = df[df["payload"].str.contains(search_term, case=False, na=False)]
        
        colA, colB = st.columns(2)
        with colA:
            if not df.empty:
                min_date = pd.to_datetime(df["timestamp"]).min()
                max_date = pd.to_datetime(df["timestamp"]).max()
                date_range = st.date_input("Filter by date", [min_date, max_date])
        
        # Display
        st.dataframe(df[["index", "timestamp", "payload", "qualia_state"]], use_container_width=True)
        
        # Enhanced chart
        fig = px.scatter(df, x="timestamp", y="qualia_state.brightness", 
                         size="qualia_state.salience", color="qualia_state.coherence",
                         hover_data=["payload"], title="Qualia Evolution Over Time")
        st.plotly_chart(fig, use_container_width=True)
        
        # CSV Export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full Chain as CSV (Lab Notebook)", csv, "scientific_discovery_chain.csv", "text/csv")
        
    else:
        st.info("No rings yet — propose the first discovery in the Propose Ring tab!")

with tab3:
    if st.button("Export full chain as JSON"):
        snapshot = tc.export_json() if hasattr(tc, "export_json") else "{}"
        st.download_button("Download JSON snapshot", snapshot, f"science_snapshot_{int(datetime.now().timestamp())}.json")
    st.info("Hardware sensor support is built-in (see LabSensor.ingest_hardware_sensor)")
