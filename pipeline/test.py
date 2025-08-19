from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "Shashank@1234"))
print("Connected ✅")
