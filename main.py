"""
generate_index.py — Auto-generate meta.json + index.json from data/ folder

Usage:
    1. Put your .txt cookie files in the data/ folder
    2. Run: python generate_index.py
    3. Commit & push to GitHub

Files are sorted alphabetically, each .txt file becomes 1 item in the index.
Label is derived from filename (without extension).
"""

import os
import json
from datetime import datetime

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(REPO_DIR, "data")
META_FILE = os.path.join(REPO_DIR, "meta.json")
INDEX_FILE = os.path.join(REPO_DIR, "index.json")


def main():
    # Ensure data/ exists
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
        print(f"Created {DATA_DIR}/ — drop your .txt files here and re-run.")
        return

    # Scan for .txt files
    files = sorted([
        f for f in os.listdir(DATA_DIR)
        if f.endswith(".txt") and os.path.isfile(os.path.join(DATA_DIR, f))
    ])

    if not files:
        print("No .txt files found in data/ — nothing to index.")
        return

    # Build items list
    items = []
    for i, filename in enumerate(files):
        file_id = f"{i + 1:03d}"
        label = os.path.splitext(filename)[0]  # Filename without .txt
        items.append({
            "id": file_id,
            "label": label,
            "path": f"data/{filename}",
            "addedAt": datetime.now().strftime("%Y-%m-%d")
        })

    # Read current version (if exists)
    version = 1
    if os.path.isfile(META_FILE):
        try:
            with open(META_FILE, "r", encoding="utf-8") as f:
                old_meta = json.load(f)
                version = old_meta.get("version", 0) + 1
        except Exception:
            version = 1

    # Write meta.json
    meta = {
        "version": version,
        "updatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "indexUrl": "index.json"
    }
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    # Write index.json
    index = {
        "schemaVersion": 1,
        "items": items
    }
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated index with {len(items)} items (version {version})")
    print(f"   meta.json  → version: {version}")
    print(f"   index.json → {len(items)} items")
    for item in items:
        print(f"     - [{item['id']}] {item['label']} → {item['path']}")

    print(f"\n🚀 Now commit & push:")
    print(f"   git add .")
    print(f"   git commit -m \"Update {len(items)} items\"")
    print(f"   git push")


if __name__ == "__main__":
    main()
