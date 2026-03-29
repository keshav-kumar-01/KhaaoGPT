"""
Intent Parser — Extract structured intent from natural language food requests
Simple keyword-based parser (no LLM needed for MVP)
"""
import re

AREA_KEYWORDS = {
    "malviya nagar": "Malviya Nagar",
    "hauz khas": "Hauz Khas",
    "saket": "Saket",
    "lajpat nagar": "Lajpat Nagar",
    "connaught place": "Connaught Place",
    "cp": "Connaught Place",
    "karol bagh": "Karol Bagh",
    "cyber city": "Cyber City",
    "sector 29": "Sector 29",
    "gurgaon": "Gurugram",
    "gurugram": "Gurugram",
    "noida": "Noida",
    "dwarka": "Dwarka",
    "gk": "Greater Kailash",
    "greater kailash": "Greater Kailash",
    "old delhi": "Old Delhi",
    "chandni chowk": "Chandni Chowk",
    "south delhi": "South Delhi",
    "rajouri garden": "Rajouri Garden",
    "pitampura": "Pitampura",
    "defence colony": "Defence Colony",
}

MOOD_KEYWORDS = {
    "spicy": "spicy",
    "hot": "spicy",
    "mild": "mild",
    "sweet": "sweet",
    "tangy": "tangy",
    "sour": "tangy",
    "rich": "rich",
    "light": "light",
    "healthy": "light",
    "comfort": "rich",
    "crispy": "crispy",
    "crunchy": "crispy",
    "creamy": "rich",
    "cheesy": "rich",
}

CUISINE_KEYWORDS = {
    "chinese": "chinese",
    "italian": "italian",
    "pizza": "italian",
    "pasta": "italian",
    "north indian": "north_indian",
    "south indian": "south_indian",
    "dosa": "south_indian",
    "idli": "south_indian",
    "mughlai": "mughlai",
    "biryani": "mughlai",
    "kebab": "mughlai",
    "street food": "street_food",
    "chaat": "street_food",
    "momos": "street_food",
    "burger": "fast_food",
    "fries": "fast_food",
    "thai": "thai",
    "japanese": "japanese",
    "sushi": "japanese",
    "korean": "korean",
    "bengali": "bengali",
    "punjabi": "punjabi",
    "mexican": "mexican",
    "continental": "continental",
    "cafe": "cafe",
    "bakery": "bakery",
    "dessert": "dessert",
}


def parse_intent(message: str) -> dict:
    """
    Parse a natural language food request into structured intent.
    """
    text = message.lower().strip()
    intent = {
        "area": None,
        "budget_max": None,
        "mood": None,
        "cuisine": None,
        "is_veg": None,
        "include_community": False,
        "raw_message": message,
    }

    # Area detection
    for keyword, area_name in AREA_KEYWORDS.items():
        if keyword in text:
            intent["area"] = area_name
            break

    # Budget detection (e.g., "under 300", "below 500", "within 200")
    budget_match = re.search(r'(?:under|below|within|max|budget)\s*(?:rs\.?|₹)?\s*(\d+)', text)
    if budget_match:
        intent["budget_max"] = int(budget_match.group(1))
    else:
        # Also check "₹300" pattern
        price_match = re.search(r'[₹]\s*(\d+)', text)
        if price_match:
            intent["budget_max"] = int(price_match.group(1))

    # Mood detection
    for keyword, mood in MOOD_KEYWORDS.items():
        if keyword in text:
            intent["mood"] = mood
            break

    # Cuisine detection
    for keyword, cuisine in CUISINE_KEYWORDS.items():
        if keyword in text:
            intent["cuisine"] = cuisine
            break

    # Veg detection
    if "veg" in text and "non" not in text:
        intent["is_veg"] = True
    elif "non-veg" in text or "non veg" in text or "nonveg" in text:
        intent["is_veg"] = False

    # Community / local / street food detection
    if any(w in text for w in ["local", "street", "dhaba", "hidden", "community", "stall"]):
        intent["include_community"] = True

    return intent
