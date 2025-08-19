# pipeline/clean_text.py

import re

def clean_text(raw_text: str) -> str:
    """
    Cleans raw input text by removing HTML tags, special characters, and excessive whitespace.
    """
    # Remove HTML tags
    cleaned = re.sub(r"<.*?>", " ", raw_text)
    
    # Remove URLs
    cleaned = re.sub(r"http\S+|www\S+", " ", cleaned)
    
    # Remove non-informative punctuation except .,?!:;
    cleaned = re.sub(r"[^\w\s.,?!:;]", " ", cleaned)

    # Normalize whitespace
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned.strip()
