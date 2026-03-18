"""
API views for the Event Concierge.
"""

from datetime import datetime, timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .db import get_events_collection
from .services import generate_venue_proposal


@api_view(["GET", "POST"])
def events_view(request):
    """
    GET  /api/events/  → list all past event searches (newest first)
    POST /api/events/  → submit a new event description for AI processing
    """
    collection = get_events_collection()

    if request.method == "GET":
        events = list(collection.find().sort("created_at", -1))
        # Convert ObjectId to string for JSON serialization
        for event in events:
            event["_id"] = str(event["_id"])
        return Response(events)

    # POST
    description = request.data.get("description", "").strip()
    if not description:
        return Response(
            {"error": "Please provide an event description."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        proposal = generate_venue_proposal(description)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response(
            {"error": f"AI service error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    doc = {
        "description": description,
        "proposal": proposal,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    result = collection.insert_one(doc)
    doc["_id"] = str(result.inserted_id)

    return Response(doc, status=status.HTTP_201_CREATED)
