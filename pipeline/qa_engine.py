# pipeline/qa_engine.py

from neo4j import GraphDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama


# 🧠 Initialize Ollama LLM
llm = Ollama(model="mistral")


# 📡 Connect to Neo4j
def get_context_from_neo4j(question, uri="bolt://localhost:7687", user="neo4j", password="Shashank@1234"):
    driver = GraphDatabase.driver(uri, auth=(user, password))

    def match_question_entities(tx, q):
        q = q.lower()
        result = tx.run("""
            MATCH (n)
            WHERE toLower(n.name) CONTAINS $query OR $query CONTAINS toLower(n.name)
            RETURN DISTINCT n.name AS name LIMIT 10
        """, {"query": q})
        return [record["name"] for record in result]

    def fetch_related_triples(tx, nodes):
        if not nodes:
            return []
        result = tx.run("""
            UNWIND $nodes AS nodeName
            MATCH (s)-[r]->(o)
            WHERE toLower(s.name) = toLower(nodeName) OR toLower(o.name) = toLower(nodeName)
            RETURN DISTINCT s.name AS subject, type(r) AS predicate, o.name AS object
        """, {"nodes": nodes})
        return [{"subject": r["subject"], "relation": r["predicate"], "object": r["object"]} for r in result]

    with driver.session() as session:
        matched_nodes = session.read_transaction(match_question_entities, question)
        triples = session.read_transaction(fetch_related_triples, matched_nodes)

    driver.close()

    context_text = "\n".join([f"{t['subject']} -[{t['relation']}]-> {t['object']}" for t in triples])
    return context_text


# 🤖 Generate Answer using LLM
def answer_question(question):
    context = get_context_from_neo4j(question)
    if not context:
        return "Sorry, I couldn't find anything relevant in the graph."

    prompt = PromptTemplate.from_template("""
    Use the following knowledge graph triples to answer the question.

    Triples:
    {context}

    Question: {question}
    Answer:""")

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"context": context, "question": question})
