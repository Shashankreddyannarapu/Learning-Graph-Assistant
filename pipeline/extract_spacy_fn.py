import spacy
from spacy.matcher import Matcher

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def spacy_extract_triples(text: str):
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)

    # Patterns to detect constructs like:
    # "X is the opposite of Y"
    matcher.add("is_the_relation_of", [
        [{"POS": "NOUN", "OP": "+"}, {"LEMMA": "be"}, {"LOWER": "the"}, {"POS": "NOUN", "OP": "+"}, {"LOWER": "of"}, {"POS": "NOUN", "OP": "+"}]
    ])

    # Patterns like:
    # "X depends on Y"
    matcher.add("verb_prep_relation", [
        [{"POS": "NOUN", "OP": "+"}, {"POS": "VERB"}, {"POS": "ADP"}, {"POS": "NOUN", "OP": "+"}]
    ])

    triples = []

    for sent in doc.sents:
        span_doc = nlp(sent.text)
        matches = matcher(span_doc)

        for match_id, start, end in matches:
            span = span_doc[start:end]
            words = [token.text for token in span]

            # Handle patterns like "Quantum computing is the opposite of classical computers"
            if "of" in words:
                of_index = words.index("of")
                subj = " ".join(words[:start + 1])
                rel = " ".join(words[start + 2:of_index])
                obj = " ".join(words[of_index + 1:])
                triples.append({
                    "subject": span[0].text,
                    "relation": rel.strip(),
                    "object": span[-1].text
                })
                continue

            # Handle verb-preposition patterns like "X depends on Y"
            for token in span:
                if token.pos_ == "VERB":
                    verb = token
                    subj = [w for w in span[:token.i - span.start] if w.pos_ in ("NOUN", "PROPN")]
                    obj = [w for w in span[token.i - span.start + 1:] if w.pos_ in ("NOUN", "PROPN")]
                    if subj and obj:
                        triples.append({
                            "subject": subj[0].text,
                            "relation": verb.text,
                            "object": obj[0].text
                        })
                    break

    return triples
