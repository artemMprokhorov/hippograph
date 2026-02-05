# Scripts Documentation

## Batch Skill Import

### add_skills.py

Batch import skills directly into Neural Memory database, bypassing MCP and context window limits.

**Usage:**
```bash
python3 add_skills.py skills.json [--db /path/to/memory.db]
```

**Skills JSON Format:**
```json
[
  {
    "name": "skill-name",
    "purpose": "Brief description of what this skill does",
    "category": "security-critical|development|ml-architecture",
    "intensity": 7,
    "tags": ["tag1", "tag2"],
    "when_to_use": "Optional: when to apply this skill"
  }
]
```

**Categories:**
- `security-critical` - Security-sensitive skills (intensity 8-10)
- `development` - General development skills (intensity 5-7)
- `ml-architecture` - ML/AI architecture skills (intensity 6-8)

**Features:**
- ✅ Direct SQLite write (no MCP overhead)
- ✅ Duplicate detection by skill name
- ✅ Emotional context automatically added
- ✅ Works with production database on server

**Example:**
```bash
# On server (Mac Studio)
ssh -i ~/.ssh/studio_key user@192.168.0.212
cd /Volumes/Balances/semantic-memory-v2/scripts
python3 add_skills.py /Volumes/Balances/skills/all_skills.json
```

**Output:**
```
📚 Loaded 10 skills
✅ Added: code-review-security (category: security-critical)
✅ Added: docker-optimization (category: development)
⏭️  Skipped: existing-skill (duplicate)

📊 Added: 8, Skipped: 2
✅ Done!
```

---

## Other Scripts

### export_memory.py
Export Neural Memory database to JSON format for backup/analysis.

### prune_edges.py  
Remove low-weight edges to optimize graph performance.

### backup.sh / restore.sh
Database backup and restore utilities.
