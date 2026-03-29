import asyncio
import os
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(backend_dir))

import httpx
from database import engine, async_session
from models.restaurant import Restaurant

# Complete Delhi NCR - Master List
# Covering Delhi, Gurugram, Noida, Faridabad, Greater Noida, and Ghaziabad
DELHI_NCR_REGIONS = [
    # SOUTH DELHI
    {"name": "Malviya Nagar", "lat": 28.5355, "lng": 77.2100},
    {"name": "Hauz Khas", "lat": 28.5494, "lng": 77.2001},
    {"name": "Saket", "lat": 28.5244, "lng": 77.2090},
    {"name": "Lajpat Nagar", "lat": 28.5677, "lng": 77.2434},
    {"name": "Greater Kailash", "lat": 28.5441, "lng": 77.2373},
    {"name": "Vasant Kunj", "lat": 28.5293, "lng": 77.1533},
    {"name": "Chhatarpur", "lat": 28.4950, "lng": 77.1750},
    {"name": "Green Park", "lat": 28.5589, "lng": 77.2028},
    
    # CENTRAL & OLD DELHI
    {"name": "Connaught Place", "lat": 28.6315, "lng": 77.2167},
    {"name": "Karol Bagh", "lat": 28.6519, "lng": 77.1909},
    {"name": "Chandni Chowk", "lat": 28.6505, "lng": 77.2303},
    {"name": "Paharganj", "lat": 28.6430, "lng": 77.2120},
    {"name": "Jama Masjid", "lat": 28.6507, "lng": 77.2334},
    {"name": "Rajendra Place", "lat": 28.6415, "lng": 77.1773},

    # WEST DELHI
    {"name": "Rajouri Garden", "lat": 28.6415, "lng": 77.1209},
    {"name": "Punjabi Bagh", "lat": 28.6669, "lng": 77.1293},
    {"name": "Janakpuri", "lat": 28.6219, "lng": 77.0878},
    {"name": "Tilak Nagar", "lat": 28.6365, "lng": 77.0968},
    {"name": "Paschim Vihar", "lat": 28.6692, "lng": 77.1009},

    # EAST DELHI
    {"name": "Laxmi Nagar", "lat": 28.6304, "lng": 77.2773},
    {"name": "Preet Vihar", "lat": 28.6416, "lng": 77.2952},
    {"name": "Mayur Vihar", "lat": 28.6046, "lng": 77.2953},
    {"name": "Krishna Nagar", "lat": 28.6565, "lng": 77.2762},
    
    # NORTH DELHI
    {"name": "Kamla Nagar", "lat": 28.6811, "lng": 77.2001},
    {"name": "Pitampura", "lat": 28.6981, "lng": 77.1388},
    {"name": "Rohini", "lat": 28.7366, "lng": 77.1129},
    {"name": "Model Town", "lat": 28.7180, "lng": 77.1902},

    # GURUGRAM (HARYANA)
    {"name": "Cyber City Gurugram", "lat": 28.4959, "lng": 77.0882},
    {"name": "Sector 29 Gurugram", "lat": 28.4677, "lng": 77.0631},
    {"name": "Golf Course Road", "lat": 28.4357, "lng": 77.1066},
    {"name": "Sushant Lok", "lat": 28.4554, "lng": 77.0841},
    {"name": "MG Road Gurugram", "lat": 28.4800, "lng": 77.0805},
    {"name": "Udyog Vihar", "lat": 28.5029, "lng": 77.0850},
    {"name": "Sohna Road", "lat": 28.3970, "lng": 77.0371},

    # NOIDA (UP)
    {"name": "Sector 18 Noida", "lat": 28.5707, "lng": 77.3271},
    {"name": "Sector 62 Noida", "lat": 28.6208, "lng": 77.3639},
    {"name": "Sector 50 Noida", "lat": 28.5714, "lng": 77.3655},
    {"name": "Noida City Centre", "lat": 28.5746, "lng": 77.3561},
    {"name": "Greater Noida (Pari Chowk)", "lat": 28.4628, "lng": 77.5133},

    # FARIDABAD & GHAZIABAD
    {"name": "NIT Faridabad", "lat": 28.3888, "lng": 77.3005},
    {"name": "Surajkund Faridabad", "lat": 28.4810, "lng": 77.2801},
    {"name": "Indirapuram Ghaziabad", "lat": 28.6411, "lng": 77.3716},
    {"name": "Vaishali Ghaziabad", "lat": 28.6499, "lng": 77.3400},
]

# We use Overpass API (OpenStreetMap)
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

async def search_osm_restaurants(client, lat, lng, radius_meters=3000):
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"~"restaurant|cafe|fast_food|food_court"](around:{radius_meters},{lat},{lng});
    );
    out body;
    """
    try:
        response = await client.post(OVERPASS_URL, data=query, timeout=30.0)
        data = response.json()
        return data.get("elements", [])
    except Exception as e:
        print(f"  Failed to fetch from OSM: {e}")
        return []

async def insert_osm_restaurant(db, element, area_name):
    tags = element.get("tags", {})
    name = tags.get("name")
    
    if not name:
        return False  # Skip unknown places
        
    lat = element.get("lat")
    lng = element.get("lon")
    amenity = tags.get("amenity", "restaurant")
    cuisine = tags.get("cuisine", "")
    
    address = " ".join(filter(None, [
        tags.get("addr:housenumber", ""),
        tags.get("addr:street", ""),
        tags.get("addr:suburb", ""),
        tags.get("addr:city", "")
    ]))

    # Logic to classify cuisine based on OSM tags
    cuisine_tags = []
    if "indian" in cuisine.lower():
        cuisine_tags.append("north_indian")
    elif "pizza" in cuisine.lower() or "italian" in cuisine.lower():
        cuisine_tags.append("italian")
    elif "chinese" in cuisine.lower():
        cuisine_tags.append("chinese")
    elif amenity == "cafe":
        cuisine_tags.append("cafe")
    elif amenity == "fast_food":
        cuisine_tags.append("fast_food")
    else:
        cuisine_tags.append("multi_cuisine")

    restaurant = Restaurant(
        name=name,
        area=area_name,
        address=address if address else f"{name}, {area_name}",
        lat=lat,
        lng=lng,
        cuisine_tags=cuisine_tags,
        is_community=False,
        is_verified=True,
        source="openstreetmap",
    )
    
    # Prevent exact duplicates (same name and area)
    from sqlalchemy import select
    existing = await db.execute(select(Restaurant).where(Restaurant.name == name).where(Restaurant.area == area_name))
    if not existing.scalar_one_or_none():
        db.add(restaurant)
        await db.commit()
        return True
    return False

async def run():
    print("Starting Complete Delhi NCR OpenStreetMap Seeder...")
    print(f"Scanning {len(DELHI_NCR_REGIONS)} major zones...")
    
    async with async_session() as db:
        async with httpx.AsyncClient() as client:
            total_added = 0
            for idx, area in enumerate(DELHI_NCR_REGIONS):
                print(f"[{idx+1}/{len(DELHI_NCR_REGIONS)}] Scanning {area['name']} (3km radius)...")
                elements = await search_osm_restaurants(client, area["lat"], area["lng"], 3000)
                print(f"  Found {len(elements)} spots. Inserting...")
                
                added_count = 0
                for el in elements:
                    if await insert_osm_restaurant(db, el, area["name"]):
                        added_count += 1
                
                total_added += added_count
                print(f"  Added {added_count} new restaurants.")
                
                # Overpass has heavy rate-limiting. Be a good citizen.
                await asyncio.sleep(2) 
                
            print(f"Complete! Successfully added {total_added} entirely free restaurant locations to KhaoGPT from OSM.")

if __name__ == "__main__":
    asyncio.run(run())
