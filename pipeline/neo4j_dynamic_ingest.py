from py2neo import Graph
import streamlit as st

def push_to_neo4j(triples):
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "Shashank@1234"

    try:
        graph = Graph(uri, auth=(user, password))
        graph.run("RETURN 1")  # Test query

        for triple in triples:
            subj = triple["subject"]
            rel = triple["relation"]
            obj = triple["object"]

            query = f"""
            MERGE (a:Entity {{name: $subj}})
            MERGE (b:Entity {{name: $obj}})
            MERGE (a)-[:{rel.upper().replace(" ", "_")}]->(b)
            """
            graph.run(query, subj=subj, obj=obj)
    except Exception as e:
        st.error(f"❌ Could not connect to Neo4j: {e}")
        print(f"[ERROR] Neo4j connection failed: {e}")
