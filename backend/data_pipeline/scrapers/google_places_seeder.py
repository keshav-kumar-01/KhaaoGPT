import asyncio
import os
import sys
from pathlib import Path

# Add backend directory to sys.path so we can import our modules
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(backend_dir))

import httpx
from dotenv import load_dotenv

from database import engine, async_session
from models.restaurant import Restaurant

load_dotenv(backend_dir / ".env")

API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# Delhi NCR areas to seed — expand from Phase 1
AREAS = [
    # South Delhi
    {"name": "Malviya Nagar Delhi",     "lat": 28.5355, "lng": 77.2100},
    {"name": "Hauz Khas Delhi",         "lat": 28.5494, "lng": 77.2001},
    {"name": "Saket Delhi",             "lat": 28.5244, "lng": 77.2090},
    {"name": "Lajpat Nagar Delhi",      "lat": 28.5677, "lng": 77.2434},
    {"name": "Greater Kailash Delhi",   "lat": 28.5441, "lng": 77.2373},
    {"name": "Vasant Kunj Delhi",       "lat": 28.5293, "lng": 77.1533},
    
    # Gurugram
    {"name": "Cyber City Gurugram",     "lat": 28.4959, "lng": 77.0882},
    {"name": "Sector 29 Gurugram",      "lat": 28.4677, "lng": 77.0631},
    {"name": "Golf Course Road Gurugram", "lat": 28.4357, "lng": 77.1066},
    
    # Central / Old Delhi
    {"name": "Connaught Place Delhi",   "lat": 28.6315, "lng": 77.2167},
    {"name": "Karol Bagh Delhi",        "lat": 28.6519, "lng": 77.1909},
    {"name": "Chandni Chowk Delhi",     "lat": 28.6505, "lng": 77.2303},
    
    # Noida
    {"name": "Sector 18 Noida",         "lat": 28.5707, "lng": 77.3271},
]

async def search_restaurants(client, lat, lng, area_name):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 1500,
        "type": "restaurant",
        "key": API_KEY
    }
    response = await client.get(url, params=params)
    data = response.json()
    if data.get("status") != "OK":
        print(f"  Google API Warning for {area_name}: {data.get('status')} - {data.get('error_message')}")
    return data.get("results", [])

async def insert_restaurant(db, place, area_name):
    name   = place.get("name", "")
    lat    = place["geometry"]["location"]["lat"]
    lng    = place["geometry"]["location"]["lng"]
    rating = place.get("rating", None)
    types  = place.get("types", [])
    address = place.get("vicinity", "")

    # Map Google types to cuisine tags logically
    cuisine_map = {
        "indian_restaurant": "north_indian",
        "restaurant": "multi_cuisine",
        "cafe": "cafe",
        "bakery": "bakery",
    }
    cuisine_tags = [cuisine_map.get(t, t) for t in types if t in cuisine_map]

    # Create new restaurant
    restaurant = Restaurant(
        name=name,
        area=area_name,
        address=address,
        lat=lat,
        lng=lng,
        cuisine_tags=cuisine_tags,
        rating_zomato=rating, # Saving as Zomato field for simplicity now
        source="google_places",
        is_community=False,
        is_verified=True,
    )
    
    # Basic check to avoid complete duplicates (very naive version)
    from sqlalchemy import select
    existing = await db.execute(select(Restaurant).where(Restaurant.name == name).where(Restaurant.area == area_name))
    if not existing.scalar_one_or_none():
        db.add(restaurant)
        await db.commit()
        return True
    return False

async def run():
    if not API_KEY or API_KEY == "your_google_api_key_here":
        print("❌ ERROR: GOOGLE_PLACES_API_KEY is not set or is empty in backend/.env")
        print("Please grab a free Google Cloud API key, add it to your .env file, and run this script again.")
        return

    print("🚀 Starting Complete Delhi NCR Google Places Seeder...")
    
    async with async_session() as db:
        async with httpx.AsyncClient() as client:
            total_added = 0
            for area in AREAS:
                print(f"📍 Scanning {area['name']}...")
                places = await search_restaurants(client, area["lat"], area["lng"], area["name"])
                print(f"  Found {len(places)} spot(s). Inserting...")
                
                added_count = 0
                for place in places:
                    if await insert_restaurant(db, place, area["name"]):
                        added_count += 1
                
                total_added += added_count
                print(f"  ✅ Added {added_count} new restaurants.")
                await asyncio.sleep(0.5) # Polite sleep for API rate limits
                
            print(f"🎉 Seeding Complete. Added {total_added} restaurants to the database.")

if __name__ == "__main__":
    asyncio.run(run())
