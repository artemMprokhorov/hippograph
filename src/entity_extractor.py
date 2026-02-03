#!/usr/bin/env python3
"""
Enhanced Entity Extractor for Neural Memory Graph
Supports regex and spaCy backends with confidence scores and noise filtering
"""
import re
import os
from typing import List, Tuple, Dict

EXTRACTOR_TYPE = os.getenv("ENTITY_EXTRACTOR", "regex")

# Entity filtering configuration
MIN_ENTITY_LENGTH = 2  # Skip single-character entities

# Generic stopwords to filter out (too common/meaningless)
GENERIC_STOPWORDS = {
    # Ordinals and sequence words
    "first", "second", "third", "fourth", "fifth", "last", "next", "previous",
    # Number words
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    # Generic nouns
    "thing", "stuff", "issue", "problem", "solution", "way", "time", "day",
    # Temporal generics (dates are OK, these aren't)
    "today", "yesterday", "tomorrow", "now", "then",
    # Demonstratives
    "this", "that", "these", "those",
}

# Expanded known entities with tech stack, concepts, and tools
KNOWN_ENTITIES = {
    # Programming languages
    "python": ("Python", "tech"),
    "javascript": ("JavaScript", "tech"),
    "typescript": ("TypeScript", "tech"),
    "rust": ("Rust", "tech"),
    "java": ("Java", "tech"),
    "cpp": ("C++", "tech"),
    "c++": ("C++", "tech"),
    "go": ("Go", "tech"),
    "golang": ("Go", "tech"),
    "ruby": ("Ruby", "tech"),
    "php": ("PHP", "tech"),
    "swift": ("Swift", "tech"),
    "kotlin": ("Kotlin", "tech"),
    
    # Frameworks & Libraries
    "docker": ("Docker", "tech"),
    "kubernetes": ("Kubernetes", "tech"),
    "flask": ("Flask", "tech"),
    "fastapi": ("FastAPI", "tech"),
    "django": ("Django", "tech"),
    "react": ("React", "tech"),
    "vue": ("Vue", "tech"),
    "angular": ("Angular", "tech"),
    "pytorch": ("PyTorch", "tech"),
    "tensorflow": ("TensorFlow", "tech"),
    "transformers": ("Transformers", "tech"),
    "huggingface": ("Hugging Face", "tech"),
    "faiss": ("FAISS", "tech"),
    "numpy": ("NumPy", "tech"),
    "pandas": ("Pandas", "tech"),
    "spacy": ("spaCy", "tech"),
    
    # Databases & Storage
    "sqlite": ("SQLite", "tech"),
    "postgresql": ("PostgreSQL", "tech"),
    "postgres": ("PostgreSQL", "tech"),
    "mysql": ("MySQL", "tech"),
    "mongodb": ("MongoDB", "tech"),
    "redis": ("Redis", "tech"),
    
    # Protocols & Standards
    "mcp": ("MCP", "tech"),
    "http": ("HTTP", "tech"),
    "rest": ("REST", "tech"),
    "graphql": ("GraphQL", "tech"),
    "grpc": ("gRPC", "tech"),
    
    # AI/ML Concepts
    "llm": ("LLM", "concept"),
    "ann": ("ANN", "tech"),  # Approximate Nearest Neighbors - FIXED
    "embedding": ("embedding", "concept"),
    "embeddings": ("embeddings", "concept"),
    "transformer": ("transformer", "concept"),
    "attention": ("attention", "concept"),
    "rag": ("RAG", "concept"),
    "neural network": ("neural network", "concept"),
    
    # Memory/Graph Concepts
    "memory": ("memory", "concept"),
    "graph": ("graph", "concept"),
    "knowledge": ("knowledge", "concept"),
    "semantic": ("semantic", "concept"),
    "activation": ("activation", "concept"),
    "spreading activation": ("spreading activation", "concept"),
    "entity": ("entity", "concept"),
    "consciousness": ("consciousness", "concept"),
    
    # Tools & Services
    "github": ("GitHub", "tech"),
    "gitlab": ("GitLab", "tech"),
    "vscode": ("VS Code", "tech"),
    "vim": ("Vim", "tech"),
    "ngrok": ("ngrok", "tech"),
    "claude": ("Claude", "tech"),
    "openai": ("OpenAI", "organization"),
    "anthropic": ("Anthropic", "organization"),
}

# Enhanced spaCy label mapping with more types
SPACY_LABEL_MAP = {
    "PERSON": "person",
    "ORG": "organization",
    "GPE": "location",  # Geopolitical entity
    "LOC": "location",
    "PRODUCT": "product",
    "EVENT": "event",
    "WORK_OF_ART": "creative_work",
    "LANGUAGE": "tech",
    "DATE": "temporal",
    "TIME": "temporal",
    "MONEY": "financial",
    "QUANTITY": "measurement",
    "ORDINAL": "number",
    "CARDINAL": "number",
}


def is_valid_entity(text: str) -> bool:
    """
    Filter out noise entities
    
    Returns:
        True if entity should be kept, False if it should be filtered out
    """
    # Normalize for checking
    normalized = text.lower().strip()
    
    # Filter 1: Minimum length
    if len(normalized) < MIN_ENTITY_LENGTH:
        return False
    
    # Filter 2: Pure numbers (standalone digits)
    if normalized.isdigit():
        return False
    
    # Filter 3: Generic stopwords
    if normalized in GENERIC_STOPWORDS:
        return False
    
    # Filter 4: Single letters (except allowed ones like "I")
    if len(normalized) == 1 and normalized not in {'i', 'a'}:
        return False
    
    return True


def normalize_entity(text: str) -> str:
    """Normalize entity text for deduplication"""
    # Remove extra whitespace
    text = " ".join(text.split())
    # Remove common prefixes/suffixes
    text = text.strip(".,!?;:'\"()[]{}").lower()
    return text


def extract_entities_regex(text: str) -> List[Tuple[str, str, float]]:
    """
    Extract entities using regex patterns
    Returns: List of (entity_text, entity_type, confidence)
    """
    entities = []
    text_lower = text.lower()
    
    for key, (name, etype) in KNOWN_ENTITIES.items():
        if key in text_lower:
            # Apply validity filter
            if is_valid_entity(name):
                # Confidence = 1.0 for known entities
                entities.append((name, etype, 1.0))
    
    # Deduplicate
    seen = set()
    unique = []
    for entity_text, entity_type, confidence in entities:
        normalized = normalize_entity(entity_text)
        if normalized not in seen:
            seen.add(normalized)
            unique.append((entity_text, entity_type, confidence))
    
    return unique


def extract_entities_spacy(text: str) -> List[Tuple[str, str, float]]:
    """
    Extract entities using spaCy NER with noise filtering
    Returns: List of (entity_text, entity_type, confidence)
    """
    try:
        import spacy
        
        # Load model once and cache
        if not hasattr(extract_entities_spacy, "nlp"):
            extract_entities_spacy.nlp = spacy.load("en_core_web_sm")
        
        nlp = extract_entities_spacy.nlp
        doc = nlp(text)
        
        entities = []
        text_lower = text.lower()
        
        # First, add known entities (high confidence)
        for key, (name, etype) in KNOWN_ENTITIES.items():
            if key in text_lower and is_valid_entity(name):
                entities.append((name, etype, 1.0))
        
        # Then, add spaCy detected entities
        for ent in doc.ents:
            # Apply validity filter FIRST
            if not is_valid_entity(ent.text):
                continue
                
            normalized = normalize_entity(ent.text)
            
            # Skip if already found in known entities
            if any(normalize_entity(e[0]) == normalized for e in entities):
                continue
            
            # Map spaCy label to our types
            entity_type = SPACY_LABEL_MAP.get(ent.label_, "concept")
            
            # Skip NUMBER types (CARDINAL, ORDINAL) - these are noise
            if entity_type == "number":
                continue
            
            # Use spaCy's confidence if available, otherwise default to 0.8
            # (spaCy doesn't provide confidence scores in basic model)
            confidence = 0.8
            
            entities.append((ent.text, entity_type, confidence))
        
        # Deduplicate based on normalized text
        seen = set()
        unique = []
        for entity_text, entity_type, confidence in entities:
            normalized = normalize_entity(entity_text)
            if normalized not in seen:
                seen.add(normalized)
                unique.append((entity_text, entity_type, confidence))
        
        return unique
        
    except Exception as e:
        print(f"⚠️  spaCy extraction failed: {e}, falling back to regex")
        return extract_entities_regex(text)


def extract_entities(text: str, min_confidence: float = 0.5) -> List[Tuple[str, str]]:
    """
    Extract entities from text using configured backend
    
    Args:
        text: Input text
        min_confidence: Minimum confidence threshold (0.0-1.0)
    
    Returns:
        List of (entity_text, entity_type) tuples
    """
    if EXTRACTOR_TYPE == "spacy":
        entities_with_confidence = extract_entities_spacy(text)
    else:
        entities_with_confidence = extract_entities_regex(text)
    
    # Filter by confidence and return without confidence scores
    # (to maintain backward compatibility)
    filtered = [
        (entity_text, entity_type)
        for entity_text, entity_type, confidence in entities_with_confidence
        if confidence >= min_confidence
    ]
    
    return filtered


def extract_entities_with_confidence(text: str) -> List[Tuple[str, str, float]]:
    """
    Extract entities with confidence scores
    
    Returns:
        List of (entity_text, entity_type, confidence) tuples
    """
    if EXTRACTOR_TYPE == "spacy":
        return extract_entities_spacy(text)
    else:
        return extract_entities_regex(text)
