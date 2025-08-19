# pipeline/graph_memory.py

import json
import os

class GraphMemory:
    def __init__(self, memory_path="graph_memory.json"):
        self.memory_path = memory_path
        self.triples = []
        self.load()

    def add_triples(self, new_triples):
        for t in new_triples:
            if t not in self.triples:
                self.triples.append(t)
        self.save()

    def get_all_triples(self):
        return self.triples

    def save(self):
        try:
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(self.triples, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Failed to save graph memory: {e}")

    def load(self):
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    self.triples = json.load(f)
            except Exception as e:
                print(f"[WARN] Failed to load existing memory: {e}")
