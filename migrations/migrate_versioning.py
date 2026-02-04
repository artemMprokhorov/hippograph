#!/usr/bin/env python3
"""
Migration: Add note_versions table for version history
Date: 2026-02-03
"""

import sqlite3
import sys

def migrate_up(db_path):
    """Add note_versions table"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create versions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS note_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            version_number INTEGER NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            importance TEXT NOT NULL,
            emotional_tone TEXT,
            emotional_intensity INTEGER,
            emotional_reflection TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (note_id) REFERENCES nodes(id) ON DELETE CASCADE,
            UNIQUE(note_id, version_number)
        )
    """)
    
    # Create index for faster version lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_note_versions_note_id 
        ON note_versions(note_id)
    """)
    
    conn.commit()
    conn.close()
    print("✅ Migration complete: note_versions table created")

def migrate_down(db_path):
    """Remove note_versions table"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS note_versions")
    cursor.execute("DROP INDEX IF EXISTS idx_note_versions_note_id")
    
    conn.commit()
    conn.close()
    print("✅ Rollback complete: note_versions table removed")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python migrate_versioning.py <db_path> [up|down]")
        sys.exit(1)
    
    db_path = sys.argv[1]
    direction = sys.argv[2] if len(sys.argv) > 2 else "up"
    
    if direction == "up":
        migrate_up(db_path)
    elif direction == "down":
        migrate_down(db_path)
    else:
        print(f"Unknown direction: {direction}")
        sys.exit(1)
