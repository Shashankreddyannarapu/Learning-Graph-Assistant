# extract_llm_fn.py

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import re
import ast

llm = Ollama(model="mistral")

prompt_template = PromptTemplate.from_template("""
Extract all subject-predicate-object (SPO) triples from the following text.
Only return a list of dictionaries like:
[{{"subject": ..., "relation": ..., "object": ...}}, ...]

Text:
{text}
""")

def extract_triples_llm(text):
    prompt = prompt_template.format(text=text.strip())
    response = llm.invoke(prompt)

    # Attempt to extract valid Python list of triples from LLM response
    try:
        # Remove text before the first '[' and after the last ']'
        match = re.search(r"\[.*\]", response, re.DOTALL)
        if match:
            triples_str = match.group(0)
            triples = ast.literal_eval(triples_str)
            if isinstance(triples, list):
                return triples
    except Exception as e:
        print("Triple parsing error:", e)

    return []
