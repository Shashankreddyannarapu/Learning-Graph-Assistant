# Learning-Graph-Assistant
Learning Graph Assistant

Learning Graph Assistant is an interactive Streamlit-based application that transforms unstructured text into a structured knowledge graph using local LLMs (via Ollama), supports multi-session graph merging, visualizes connections with PyVis, and enables question-answering over the graph using Neo4j.

---

## Features:

- ✍️ **Multi-format Input** – Paste or upload `.txt` files.
- 🔍 **Triple Extraction** – Uses Ollama (Mistral) to extract Subject-Predicate-Object (SPO) triples.
- 🌐 **Graph Visualization** – Builds an interactive color-coded graph with PyVis.
- 🔁 **Graph Merging** – Dynamically adds new data to an existing graph without loss.
- 🧠 **Neo4j Integration** – Triples are pushed to a Neo4j graph database.
- ❓ **Graph Q&A** – Ask questions based on your custom graph and receive answers via LLM reasoning over Neo4j.
- 🎨 **Node Coloring** – 
  - Red: Newly added main nodes
  - Green: Existing connected nodes
- 🧹 **Reset Option** – Clear all memory and start fresh.

---

## Folder Structure:

```
Final_Project_Learning_Graph_Assistant/
│
├── webapp/
│   └── app.py                         # Streamlit frontend
│
├── pipeline/                          # Core logic
│   ├── clean_text.py
│   ├── extract_llm_fn.py
│   ├── structure_triples_fn.py
│   ├── graph_builder.py
│   ├── graph_memory.py
│   ├── neo4j_dynamic_ingest.py
│   └── qa_engine.py
│
├── graph_memory.json                  # Persistent triple storage
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

---

## Installation & Setup

1. Clone the repository

```bash
git clone https://github.com/your-username/Learning-Graph-Assistant.git
cd Learning-Graph-Assistant
```

2. Set up Python environment

```bash
pip install -r requirements.txt
```

3. Install & Run Ollama

- Download from: [https://ollama.com/download](https://ollama.com/download)
- Pull the model used:

```bash
ollama pull mistral
```

4. Start Neo4j

- Install Neo4j Desktop or use Docker
- Default config:
  - **Bolt URL:** `bolt://localhost:7687`
  - **Username:** `neo4j`
  - **Password:** `test`  
> *(Change in `qa_engine.py` and `neo4j_dynamic_ingest.py` if you use a different password)*

---

## Running the App:

```bash
cd webapp
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Example Use Case:

1. Paste a paragraph about Quantum Computing.
2. Triples extracted (e.g.):
   ```
   quantum computing → uses → qubits
   qubits → enable → parallelism
   ```
3. Interactive graph is rendered.
4. Ask: _"What does quantum computing use?"_
5. Get an LLM-generated answer based on your evolving Neo4j knowledge base.

---

## Technologies Used:

| Layer        | Technology                     |
|--------------|--------------------------------|
| Frontend     | `Streamlit`, `PyVis`           |
| LLM          | `Ollama` with `Mistral` model  |
| Triple Extraction | `LangChain`, Custom Prompt |
| Graph DB     | `Neo4j`, `py2neo`              |
| Q&A Engine   | `LangChain`, `Neo4j Cypher`    |
| Others       | `Python`, `JSON`, `HTML`       |

---

## 📌 Future Enhancements:

- PDF & DOCX input support
- Embedding-based semantic Q&A
- Editable node/edge properties in graph UI
- Export session to PDF or markdown

---

## Author:
Shashank Reddy Annarapu - Master’s Student in Computer Science, CSU Fullerton.
Pavana Manjunath - Master’s Student in Computer Science, CSU Fullerton.

Shashank Reddy Annarapu – Master’s Student in Computer Science, CSU Fullerton 
Pavana Manjunath - Master’s Student in Computer Science, CSU Fullerton 
