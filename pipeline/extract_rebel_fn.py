from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re

def clean_token(t: str) -> str:
    """Remove special tokens and trim whitespace."""
    return t.replace("<s>", "").replace("</s>", "").strip()

def parse_rebel_output(decoded_text: str) -> list:
    """
    Robust parser for REBEL output: <triplet> SUBJECT <subj> OBJECT <obj> RELATION
    Tries to handle malformed patterns more gracefully.
    """
    triples = []
    decoded_text = decoded_text.replace("<s>", "").replace("</s>", "").strip()

    segments = decoded_text.split("<triplet>")
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
        try:
            if "<subj>" in segment and "<obj>" in segment:
                subj_split = segment.split("<subj>")
                subject = subj_split[0].strip()
                obj_split = subj_split[1].split("<obj>")
                object_ = obj_split[0].strip()
                relation = obj_split[1].strip()

                # Sanity check
                if subject and object_ and relation:
                    triples.append({
                        "subject": subject,
                        "relation": relation,
                        "object": object_
                    })
                else:
                    print(f"[WARN] Incomplete triple skipped: {segment}")
            else:
                print(f"[WARN] Skipping malformed segment: {segment[:100]}")
        except Exception as e:
            print(f"[ERROR] Failed to parse segment: {segment[:100]} | Reason: {e}")
    return triples



def extract_relations(cleaned_text: str, model_name="Babelscape/rebel-large") -> list:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    input_ids = tokenizer.encode(cleaned_text, add_special_tokens=True)
    input_ids = torch.tensor(input_ids, dtype=torch.long)

    chunk_size = 450
    stride = 50

    token_chunks = [input_ids[i:i + chunk_size] for i in range(0, len(input_ids), chunk_size - stride)]
    print(f"[INFO] Total token chunks: {len(token_chunks)}")

    all_triples = []
    for i, chunk in enumerate(token_chunks):
        try:
            input_tensor = chunk.unsqueeze(0).to(device)
            outputs = model.generate(input_ids=input_tensor, max_length=512)
            decoded = tokenizer.decode(outputs[0], skip_special_tokens=False)
            print(f"\n[INFO] Chunk {i + 1} decoded output:\n{decoded[:300]}...")
            triples = parse_rebel_output(decoded)
            all_triples.extend(triples)
        except Exception as e:
            print(f"[ERROR] Failed on chunk {i + 1}: {e}")

    unique_triples = [dict(t) for t in {tuple(triple.items()) for triple in all_triples}]
    print(f"\n[INFO] Extracted {len(unique_triples)} unique triples")
    return unique_triples
