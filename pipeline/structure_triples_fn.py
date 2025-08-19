def structure_triples(raw_triples):
    structured = []
    for triple in raw_triples:
        if not triple or not isinstance(triple, dict):
            continue
        subj = triple.get("subject")
        rel = triple.get("relation")
        obj = triple.get("object")

        if not subj or not rel or not obj:
            continue  # Skip malformed or incomplete triples

        structured.append({
            "subject": subj.strip(),
            "relation": rel.strip(),
            "object": obj.strip()
        })
    return structured

