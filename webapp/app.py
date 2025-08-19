# app.py

import streamlit as st
import os
import tempfile
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.clean_text import clean_text
from pipeline.extract_llm_fn import extract_triples_llm as extract_relations
from pipeline.structure_triples_fn import structure_triples
from pipeline.neo4j_dynamic_ingest import push_to_neo4j
from pipeline.graph_builder import build_pyvis_graph
from pipeline.graph_memory import GraphMemory
from pipeline.qa_engine import answer_question

# ─── SESSION STATE INITIALIZATION ───────────────────────────────
if "graph_memory" not in st.session_state:
    st.session_state.graph_memory = GraphMemory()

if "node_set" not in st.session_state:
    st.session_state.node_set = set()
if "edge_set" not in st.session_state:
    st.session_state.edge_set = set()
if "all_triples" not in st.session_state:
    st.session_state.all_triples = []
if "raw_outputs" not in st.session_state:
    st.session_state.raw_outputs = []
if "last_graph_html" not in st.session_state:
    st.session_state.last_graph_html = None
if "input_history" not in st.session_state:
    st.session_state.input_history = []

# ─── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(page_title="🧠 Learning Graph Assistant", layout="wide")
st.title("🧠 Learning Graph Assistant")
st.markdown("Build a dynamic knowledge graph from multiple texts and ask questions!")

# ─── INPUT HANDLING ─────────────────────────────────────────────
option = st.radio("Choose input type:", ["📄 Upload .txt File", "🖍️ Paste Text"])
if option == "📄 Upload .txt File":
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    raw_text = uploaded_file.read().decode("utf-8") if uploaded_file else ""
else:
    raw_text = st.text_area("Paste your learning content here", height=250)

# ─── MAIN GRAPH GENERATION ──────────────────────────────────────
if raw_text and st.button("🚀 Generate Knowledge Graph"):
    st.session_state.input_history.append(raw_text)

    st.info("🔄 Cleaning text...")
    cleaned_text = clean_text(raw_text)

    st.info("🤖 Extracting triples using Ollama...")
    extracted = extract_relations(cleaned_text)
    if not extracted:
        st.warning("⚠️ No triples extracted. Try more informative text.")
    else:
        st.session_state.raw_outputs.extend(extracted)

        st.info("📐 Structuring triples...")
        triples = structure_triples(extracted)

        # Add new triples to memory and get full merged version
        st.session_state.graph_memory.add_triples(triples)
        merged_triples = st.session_state.graph_memory.get_all_triples()
        st.session_state.all_triples = merged_triples

        st.info("📈 Building graph with PyVis...")
        net, new_node_set, new_edge_set = build_pyvis_graph(
            triples,  # only new triples for node color logic
            existing_nodes=st.session_state.node_set,
            existing_edges=st.session_state.edge_set
        )
        st.session_state.node_set = new_node_set
        st.session_state.edge_set = new_edge_set

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
            html_path = tmp.name
            net.show(html_path, notebook=False)
            with open(html_path, "r", encoding="utf-8") as f:
                st.session_state.last_graph_html = f.read()

        st.success("✅ Graph rendered below!")
        st.components.v1.html(st.session_state.last_graph_html, height=750)

        st.info("📡 Pushing to Neo4j...")
        push_to_neo4j(triples)
        st.success("🧠 Knowledge ingested into Neo4j!")

# ─── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📂 Exploration Panel")

    if st.button("🔁 Show Last Rendered Graph"):
        if st.session_state.last_graph_html:
            st.components.v1.html(
                st.session_state.last_graph_html, height=750, scrolling=True
            )
        else:
            st.warning("⚠️ No graph rendered yet.")

    if st.checkbox("📦 Show All Extracted Triples"):
        st.markdown("### 📦 Extracted Triples")
        st.json(st.session_state.get("all_triples", []))

    if st.checkbox("🧾 Show Raw REBEL Outputs (debug)"):
        st.markdown("### 🔍 Raw LLM Outputs")
        for i, raw in enumerate(st.session_state.get("raw_outputs", [])):
            st.text(f"Chunk {i + 1} output:")
            st.code(str(raw), language="text")

    if st.checkbox("📝 Show Previous Input Texts"):
        for i, t in enumerate(st.session_state.input_history):
            st.markdown(f"**Input {i+1}:**")
            st.code(t)

    if st.button("🔄 Reset Graph Memory"):
        st.session_state.graph_memory = GraphMemory()
        st.session_state.node_set = set()
        st.session_state.edge_set = set()
        st.session_state.all_triples = []
        st.session_state.raw_outputs = []
        st.session_state.last_graph_html = None
        st.session_state.input_history = []
        try:
            os.remove("graph_memory.json")
            st.success("✅ Graph memory and stored data cleared.")
        except FileNotFoundError:
            st.info("ℹ️ No previous memory file found.")

# ─── Q&A SECTION ───────────────────────────────────────────────
st.markdown("---")
st.header("❓ Ask Questions about Your Graph")
question = st.text_input("🔍 What do you want to know?", placeholder="e.g., What does quantum computing use?")
if question:
    with st.spinner("🧠 Thinking..."):
        answer = answer_question(question)
        st.markdown(f"**🗣️ Answer:** {answer}")
