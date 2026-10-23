from __future__ import annotations

import json
import os
import sqlite3
import sys
from pymongo import MongoClient

from app.core.config import get_settings


def migrate_sqlite_to_mongo():
    settings = get_settings()
    mongo_url = settings.MONGODB_URL
    db_name = settings.MONGODB_DB_NAME
    sqlite_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "bet_admin.db")

    if not os.path.exists(sqlite_path):
        print(f"SQLite file not found at: {sqlite_path}")
        return

    print(f"Connecting to MongoDB Atlas at {mongo_url[:35]}...")
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=10000)
    db = client[db_name]

    print(f"Reading SQLite database from {sqlite_path}...")
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    tables = [
        r[0]
        for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        if not r[0].startswith("sqlite_") and not r[0].startswith("alembic_")
    ]

    stats = {}
    for table in tables:
        rows = cur.execute(f"SELECT * FROM {table}").fetchall()
        docs = []
        for row in rows:
            d = dict(row)
            for k, v in d.items():
                if isinstance(v, str) and (v.startswith("{") or v.startswith("[")):
                    try:
                        d[k] = json.loads(v)
                    except Exception:
                        pass
            docs.append(d)

        collection = db[table]
        collection.delete_many({})
        if docs:
            collection.insert_many(docs)
        stats[table] = len(docs)
        print(f"Migrated table '{table}': {len(docs)} records into MongoDB collection '{table}'")

    conn.close()
    client.close()
    print("Migration finished successfully! Summary:", stats)


if __name__ == "__main__":
    migrate_sqlite_to_mongo()
