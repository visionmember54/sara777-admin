from __future__ import annotations

import logging
from datetime import date, datetime, time
from typing import Any
from pymongo import MongoClient
from sqlalchemy import event, inspect
from sqlalchemy.orm import Session

from app.core.config import get_settings

logger = logging.getLogger("app.mongo")
_mongo_client: MongoClient | None = None


def get_mongo_client() -> MongoClient | None:
    global _mongo_client
    if _mongo_client is None:
        settings = get_settings()
        if not settings.MONGODB_URL:
            logger.warning("MONGODB_URL is not set in environment or .env")
            return None
        _mongo_client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=10000)
    return _mongo_client


def get_mongo_db():
    settings = get_settings()
    client = get_mongo_client()
    if client is None:
        return None
    return client[settings.MONGODB_DB_NAME]


def _serialize_val(val: Any) -> Any:
    if isinstance(val, (datetime, date, time)):
        return val.isoformat()
    return val


def _deserialize_row(row_dict: dict[str, Any], table) -> dict[str, Any]:
    cleaned = {}
    for col in table.columns:
        col_name = col.name
        if col_name in row_dict:
            val = row_dict[col_name]
            # Convert ISO string to time or date if needed by SQLite
            if val is not None:
                python_type = getattr(col.type, "python_type", None)
                if python_type is time and isinstance(val, str):
                    try:
                        val = time.fromisoformat(val)
                    except Exception:
                        pass
                elif python_type is date and isinstance(val, str):
                    try:
                        val = date.fromisoformat(val)
                    except Exception:
                        pass
                elif python_type is datetime and isinstance(val, str):
                    try:
                        val = datetime.fromisoformat(val)
                    except Exception:
                        pass
            cleaned[col_name] = val
    return cleaned


def sync_from_mongo(engine) -> None:
    """Restores local database cache from MongoDB Atlas on startup."""
    try:
        from app.db.base import Base
        Base.metadata.create_all(bind=engine)
        
        db = get_mongo_db()
        if db is None:
            logger.info("MONGODB_URL not provided; skipping initial MongoDB sync.")
            return
        # Test connection ping
        db.command("ping")
        logger.info("Connected to MongoDB Atlas successfully.")

        with engine.begin() as conn:
            for table in Base.metadata.sorted_tables:
                col_name = table.name
                if col_name.startswith("sqlite_") or col_name.startswith("alembic_"):
                    continue
                
                collection = db[col_name]
                cursor = collection.find({})
                docs = list(cursor)
                if not docs:
                    continue

                # Clear local table and populate from MongoDB
                conn.execute(table.delete())
                rows = []
                for doc in docs:
                    doc.pop("_id", None)
                    cleaned = _deserialize_row(doc, table)
                    if cleaned:
                        rows.append(cleaned)
                
                if rows:
                    conn.execute(table.insert(), rows)
                    logger.info(f"Loaded {len(rows)} records from MongoDB into '{col_name}'")

        logger.info("Database cache populated from MongoDB Atlas.")
    except Exception as exc:
        logger.warning(f"Could not sync from MongoDB Atlas (will proceed with local SQLite): {exc}")


def setup_mongo_mirroring(session_factory) -> None:
    """Attaches SQLAlchemy event listener to mirror all mutations to MongoDB Atlas."""

    @event.listens_for(session_factory, "after_flush")
    def after_flush_sync(session: Session, flush_context) -> None:
        try:
            db = get_mongo_db()
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB in after_flush: {e}")
            return

        # Handle Inserts and Updates
        for obj in list(session.new) + list(session.dirty):
            table = getattr(obj, "__tablename__", None)
            if not table:
                continue

            try:
                mapper = inspect(obj)
                data = {}
                for col in mapper.attrs:
                    val = getattr(obj, col.key, None)
                    data[col.key] = _serialize_val(val)

                # Primary key identifier
                pk_val = getattr(obj, "id", None)
                if pk_val is not None:
                    db[table].replace_one({"id": pk_val}, data, upsert=True)
                else:
                    # Table without id column (e.g. association tables)
                    db[table].insert_one(data)
            except Exception as e:
                logger.error(f"Failed to mirror write to MongoDB for table '{table}': {e}")

        # Handle Deletes
        for obj in list(session.deleted):
            table = getattr(obj, "__tablename__", None)
            if not table:
                continue

            try:
                pk_val = getattr(obj, "id", None)
                if pk_val is not None:
                    db[table].delete_one({"id": pk_val})
            except Exception as e:
                logger.error(f"Failed to mirror delete to MongoDB for table '{table}': {e}")
