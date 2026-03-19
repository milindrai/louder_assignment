"""
Venue Proposal Service
Provides venue recommendations using Gemini, OpenAI, or Groq based on available API keys.
Includes a local fallback heuristic generator if APIs are unavailable.
"""

import os
import json
import re

# ─── Prompt shared by both providers ────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert corporate event planner. Given a natural language description of a corporate event, analyze it and return a JSON object with the following fields:

{
  "venue_name": "Name of a real or realistic venue",
  "location": "City, State/Country",
  "estimated_cost": "$X,XXX",
  "capacity": "Number of people it can accommodate",
  "duration": "Recommended duration",
  "why_it_fits": "A 2-3 sentence justification of why this venue is perfect for the described event",
  "amenities": ["list", "of", "key", "amenities"],
  "event_type": "Type of event (retreat, conference, team-building, etc.)"
}

Rules:
- Always return ONLY valid JSON, no markdown fences, no extra text.
- Make the venue realistic and the cost reasonable for the described budget.
- If no budget is mentioned, suggest a mid-range option and note the estimated cost.
- The "why_it_fits" field should reference specific details from the user's description.
"""


def _parse_json_response(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown fences."""
    text = text.strip()
    # Remove markdown code fences if present
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)


def _generate_with_gemini(user_input: str) -> dict:
    """Call Google Gemini API."""
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        f"{SYSTEM_PROMPT}\n\nUser request: {user_input}"
    )
    return _parse_json_response(response.text)


def _generate_with_openai(user_input: str) -> dict:
    """Call OpenAI API."""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,
    )
    return _parse_json_response(response.choices[0].message.content)


def _generate_with_groq(user_input: str) -> dict:
    """Call Groq API (free tier, uses Llama 3)."""
    from groq import Groq

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,
    )
    return _parse_json_response(response.choices[0].message.content)


_PLACEHOLDER_KEYS = {
    "your_gemini_api_key_here",
    "your_openai_api_key_here",
    "your_groq_api_key_here",
}


def _is_valid_key(key: str) -> bool:
    """Check if an API key looks real (not a placeholder)."""
    return bool(key) and key not in _PLACEHOLDER_KEYS


def _generate_fallback_proposal(user_input: str) -> dict:
    """
    Fallback heuristic generator when all external providers are unavailable.
    Produces realistic proposals based on keyword pattern matching.
    """
    import random

    text = user_input.lower()

    # Extract rough budget
    budget = "$3,500"
    for word in text.split():
        cleaned = word.strip("$,.")
        if cleaned.replace("k", "000").isdigit():
            num = int(cleaned.replace("k", "000"))
            budget = f"${num:,}"

    # Detect team size
    capacity = "10-15 people"
    for word in text.split():
        if word.isdigit() and int(word) < 500:
            capacity = f"{word} people"

    # Pick venue based on keywords
    venues = [
        {
            "keywords": ["mountain", "retreat", "nature", "hiking", "outdoor"],
            "venue_name": "Summit Ridge Mountain Lodge",
            "location": "Aspen, Colorado",
            "amenities": ["Private meeting rooms", "Mountain views", "Hiking trails", "Spa & wellness center", "Farm-to-table dining"],
            "event_type": "Leadership Retreat",
        },
        {
            "keywords": ["beach", "coast", "ocean", "tropical", "island"],
            "venue_name": "Azure Bay Resort & Conference Center",
            "location": "Maui, Hawaii",
            "amenities": ["Oceanfront meeting spaces", "Team-building activities", "Snorkeling", "Rooftop lounge", "Catered meals"],
            "event_type": "Corporate Retreat",
        },
        {
            "keywords": ["city", "urban", "downtown", "conference", "tech"],
            "venue_name": "The Loft at Innovation Square",
            "location": "San Francisco, California",
            "amenities": ["AV-equipped conference rooms", "High-speed WiFi", "Rooftop terrace", "On-site catering", "Breakout spaces"],
            "event_type": "Conference",
        },
        {
            "keywords": ["team", "build", "fun", "activity", "bond"],
            "venue_name": "Pinewood Team Experience Center",
            "location": "Lake Tahoe, California",
            "amenities": ["Adventure courses", "Group cabins", "Bonfire area", "Kayaking", "Team workshops"],
            "event_type": "Team Building",
        },
    ]

    # Default venue
    chosen = {
        "venue_name": "The Grand Horizon Event Center",
        "location": "Austin, Texas",
        "amenities": ["Modern conference hall", "Breakout rooms", "On-site catering", "AV equipment", "Networking lounge"],
        "event_type": "Corporate Offsite",
    }

    for venue in venues:
        if any(kw in text for kw in venue["keywords"]):
            chosen = venue
            break

    duration = "3 days"
    for word in text.split():
        if word.isdigit() and 1 <= int(word) <= 14:
            for ctx in ["day", "night"]:
                if ctx in text:
                    duration = f"{word} {'days' if int(word) > 1 else 'day'}"
                    break

    return {
        "venue_name": chosen["venue_name"],
        "location": chosen["location"],
        "estimated_cost": budget,
        "capacity": capacity,
        "duration": duration,
        "why_it_fits": f"This venue is an excellent match for your described event. "
                       f"It comfortably accommodates {capacity} and offers a curated "
                       f"experience designed for {chosen['event_type'].lower()} events. "
                       f"The facilities and location align well with your requirements "
                       f"while staying within the {budget} budget range.",
        "amenities": chosen["amenities"],
        "event_type": chosen["event_type"]
    }


def generate_venue_proposal(user_input: str) -> dict:
    """
    Generate a structured venue proposal from a natural language event description.
    Tries providers in order: Gemini → OpenAI → Groq (free) → demo mode.
    """
    keys = {
        "gemini": _is_valid_key(os.getenv("GEMINI_API_KEY", "").strip()),
        "openai": _is_valid_key(os.getenv("OPENAI_API_KEY", "").strip()),
        "groq": _is_valid_key(os.getenv("GROQ_API_KEY", "").strip()),
    }

    # Build ordered list of providers to try
    providers = []
    if keys["gemini"]:
        providers.append(("Gemini", _generate_with_gemini))
    if keys["openai"]:
        providers.append(("OpenAI", _generate_with_openai))
    if keys["groq"]:
        providers.append(("Groq", _generate_with_groq))

    for name, fn in providers:
        try:
            result = fn(user_input)
            return result
        except Exception:
            # Silently continue to next provider
            pass

    # All external providers failed (or none configured)
    return _generate_fallback_proposal(user_input)
