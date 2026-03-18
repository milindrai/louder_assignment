"""
MongoDB connection and helper functions using pymongo.
"""

from pymongo import MongoClient
from django.conf import settings

_client = None
_db = None


def get_db():
    """Return the MongoDB database instance (lazy singleton)."""
    global _client, _db
    if _db is None:
        _client = MongoClient(settings.MONGODB_URI)
        _db = _client[settings.MONGODB_NAME]
    return _db


def get_events_collection():
    """Return the 'events' collection."""
    return get_db()["events"]
