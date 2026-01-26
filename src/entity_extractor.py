#!/usr/bin/env python3
"""Entity Extractor for Neural Memory Graph"""
import re
import os
from typing import List, Tuple

EXTRACTOR_TYPE = os.getenv("ENTITY_EXTRACTOR", "regex")

KNOWN_ENTITIES = {
    "python": ("Python", "tech"),
    "javascript": ("JavaScript", "tech"),
    "typescript": ("TypeScript", "tech"),
    "rust": ("Rust", "tech"),
    "docker": ("Docker", "tech"),
    "flask": ("Flask", "tech"),
    "fastapi": ("FastAPI", "tech"),
    "sqlite": ("SQLite", "tech"),
    "postgresql": ("PostgreSQL", "tech"),
    "mcp": ("MCP", "tech"),
    "memory": ("memory", "concept"),
    "graph": ("graph", "concept"),
    "knowledge": ("knowledge", "concept"),
}

SPACY_LABEL_MAP = {
    "PERSON": "person",
    "ORG": "organization",
    "GPE": "location",
    "LOC": "location",
    "PRODUCT": "product",
    "EVENT": "event",
    "LANGUAGE": "tech",
    "DATE": "temporal",
}

def extract_entities_regex(text: str) -> List[Tuple[str, str]]:
    entities = []
    text_lower = text.lower()
    for key, (name, etype) in KNOWN_ENTITIES.items():
        if key in text_lower:
            entities.append((name, etype))
    seen = set()
    unique = []
    for e in entities:
        if e[0].lower() not in seen:
            seen.add(e[0].lower())
            unique.append(e)
    return unique

def extract_entities_spacy(text: str) -> List[Tuple[str, str]]:
    try:
        import spacy
        if not hasattr(extract_entities_spacy, "nlp"):
            extract_entities_spacy.nlp = spacy.load("en_core_web_sm")
        nlp = extract_entities_spacy.nlp
        doc = nlp(text)
        entities = []
        text_lower = text.lower()
        for key, (name, etype) in KNOWN_ENTITIES.items():
            if key in text_lower:
                entities.append((name, etype))
        for ent in doc.ents:
            if ent.text.lower() not in [e[0].lower() for e in entities]:
                entity_type = SPACY_LABEL_MAP.get(ent.label_, "concept")
                entities.append((ent.text, entity_type))
        seen = set()
        unique = []
        for e in entities:
            if e[0].lower() not in seen:
                seen.add(e[0].lower())
                unique.append(e)
        return unique
    except:
        return extract_entities_regex(text)

def extract_entities(text: str) -> List[Tuple[str, str]]:
    if EXTRACTOR_TYPE == "spacy":
        return extract_entities_spacy(text)
    else:
        return extract_entities_regex(text)
