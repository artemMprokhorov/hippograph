#!/usr/bin/env python3
"""
Entity Extractor for Neural Memory Graph
Extracts entities from text for automatic graph linking
"""

import re
import os
from typing import List, Tuple

EXTRACTOR_TYPE = os.getenv("ENTITY_EXTRACTOR", "regex")

# Known entities dictionary - customize for your domain
# Format: "lowercase_key": ("Display Name", "entity_type")
KNOWN_ENTITIES = {
    # Programming languages & frameworks
    "python": ("Python", "tech"),
    "javascript": ("JavaScript", "tech"),
    "typescript": ("TypeScript", "tech"),
    "rust": ("Rust", "tech"),
    "kotlin": ("Kotlin", "tech"),
    "java": ("Java", "tech"),
    
    # Frameworks & tools
    "docker": ("Docker", "tech"),
    "flask": ("Flask", "tech"),
    "fastapi": ("FastAPI", "tech"),
    "sqlite": ("SQLite", "tech"),
    "postgresql": ("PostgreSQL", "tech"),
    "redis": ("Redis", "tech"),
    "react": ("React", "tech"),
    "vue": ("Vue", "tech"),
    
    # AI/ML
    "mcp": ("MCP", "tech"),
    "llm": ("LLM", "concept"),
    "embedding": ("embedding", "concept"),
    "transformer": ("transformer", "concept"),
    "neural network": ("neural network", "concept"),
    
    # Concepts
    "memory": ("memory", "concept"),
    "graph": ("graph", "concept"),
    "knowledge": ("knowledge", "concept"),
    "semantic": ("semantic", "concept"),
    
    # Add your own entities here
    # "project_name": ("Project Name", "project"),
    # "person_name": ("Person Name", "person"),
}


def extract_entities_regex(text: str) -> List[Tuple[str, str]]:
    """Extract entities using regex patterns and known dictionary"""
    entities = []
    text_lower = text.lower()
    
    # 1. Match known entities from dictionary
    for key, (name, etype) in KNOWN_ENTITIES.items():
        if key in text_lower:
            entities.append((name, etype))
    
    # 2. Extract CamelCase words (likely class/project names)
    camel_pattern = r"\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b"
    for match in re.findall(camel_pattern, text):
        if match.lower() not in [e[0].lower() for e in entities]:
            entities.append((match, "concept"))
    
    # 3. Extract @mentions
    mention_pattern = r"@(\w+)"
    for match in re.findall(mention_pattern, text):
        entities.append((match, "person"))
    
    # 4. Extract #hashtags
    hashtag_pattern = r"#(\w+)"
    for match in re.findall(hashtag_pattern, text):
        entities.append((match, "tag"))
    
    # 5. Extract URLs as entities
    url_pattern = r"https?://(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+)"
    for match in re.findall(url_pattern, text):
        entities.append((match, "url"))
    
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for e in entities:
        key = e[0].lower()
        if key not in seen:
            seen.add(key)
            unique.append(e)
    
    return unique


def extract_entities(text: str) -> List[Tuple[str, str]]:
    """Main entry point for entity extraction"""
    if EXTRACTOR_TYPE == "spacy":
        # TODO: Implement spacy-based extraction
        return extract_entities_regex(text)
    elif EXTRACTOR_TYPE == "llm":
        # TODO: Implement LLM-based extraction
        return extract_entities_regex(text)
    else:
        return extract_entities_regex(text)


if __name__ == "__main__":
    # Test entity extraction
    test_texts = [
        "Building a knowledge graph with Python and SQLite",
        "Working on MyProject using Docker and Flask",
        "Check out @username's work on #machinelearning",
        "Interesting paper at https://arxiv.org/paper",
    ]
    
    for text in test_texts:
        print(f"\nText: {text}")
        entities = extract_entities(text)
        print(f"Entities: {entities}")
