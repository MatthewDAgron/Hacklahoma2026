"""
Database helpers for posture/slouch event storage and retrieval.
Uses MONGODB_URI from .env.
"""
import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

URI = os.getenv("MONGODB_URI")
DB_NAME = "posture_db"
COLLECTION_USERS = "users"
COLLECTION_EVENTS = "posture_events"


def get_client():
    """Return a MongoDB client."""
    return MongoClient(URI, server_api=ServerApi("1"))


def get_or_create_user(username: str, extra: dict = None) -> dict:
    """
    Get user by username. Create if not exists.
    Returns the user document (includes _id).
    """
    client = get_client()
    coll = client[DB_NAME][COLLECTION_USERS]
    user = coll.find_one({"username": username})
    if user:
        client.close()
        return user
    doc = {"username": username, "createdAt": datetime.utcnow()}
    if extra:
        doc.update(extra)
    result = coll.insert_one(doc)
    user = coll.find_one({"_id": result.inserted_id})
    client.close()
    return user


def get_user_by_username(username: str):
    """Get user by username. Returns None if not found."""
    client = get_client()
    user = client[DB_NAME][COLLECTION_USERS].find_one({"username": username})
    client.close()
    return user


def insert_posture_event(user_id: str, slouch_severity: float, duration_seconds: float, posture_data: dict = None) -> str:
    """
    Insert a single posture/slouch event.
    user_id: username (linked to users.username).
    Returns the inserted document _id.
    """
    client = get_client()
    coll = client[DB_NAME][COLLECTION_EVENTS]
    doc = {
        "userId": user_id,
        "timestamp": datetime.utcnow(),
        "slouchSeverity": slouch_severity,
        "durationSeconds": duration_seconds,
    }
    if posture_data:
        doc["postureData"] = posture_data
    result = coll.insert_one(doc)
    client.close()
    return str(result.inserted_id)


def get_posture_events(user_id: str, start_date=None, end_date=None, limit: int = 100):
    """
    Get posture events for a user, optionally filtered by date range.
    Returns a list of documents.
    """
    client = get_client()
    coll = client[DB_NAME][COLLECTION_EVENTS]
    query = {"userId": user_id}
    if start_date:
        query["timestamp"] = {"$gte": start_date}
    if end_date:
        query.setdefault("timestamp", {})["$lte"] = end_date
    cursor = coll.find(query).sort("timestamp", -1).limit(limit)
    events = list(cursor)
    client.close()
    return events


def get_weekly_metrics(user_id: str, week_start: datetime):
    """
    Aggregate posture metrics for a user for a given week.
    week_start: start of the week (e.g. Monday 00:00:00 UTC).
    """
    from datetime import timedelta
    client = get_client()
    coll = client[DB_NAME][COLLECTION_EVENTS]
    week_end = week_start + timedelta(days=7)
    pipeline = [
        {"$match": {"userId": user_id, "timestamp": {"$gte": week_start, "$lt": week_end}}},
        {"$group": {
            "_id": None,
            "totalEvents": {"$sum": 1},
            "totalMinutes": {"$sum": {"$divide": ["$durationSeconds", 60]}},
            "avgSeverity": {"$avg": "$slouchSeverity"},
        }},
    ]
    result = list(coll.aggregate(pipeline))
    client.close()
    return result[0] if result else {"totalEvents": 0, "totalMinutes": 0, "avgSeverity": 0}


def get_user_with_posture_summary(username: str, event_limit: int = 10):
    """
    Get user plus their recent posture events and weekly metrics.
    Links users collection to posture_events. Returns None if user not found.
    """
    user = get_user_by_username(username)
    if not user:
        return None
    user_id = user["username"]
    events = get_posture_events(user_id, limit=event_limit)
    from datetime import timedelta
    week_start = datetime.utcnow().replace(hour=0, minute=0, second=0) - timedelta(days=7)
    metrics = get_weekly_metrics(user_id, week_start)
    return {"user": user, "recentEvents": events, "weeklyMetrics": metrics}
