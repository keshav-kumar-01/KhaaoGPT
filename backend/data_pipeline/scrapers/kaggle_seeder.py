import asyncio
import csv
import json
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(backend_dir))

from database import engine, async_session
from models.restaurant import Restaurant

CSV_FILE_PATH = Path(__file__).parent.parent / "kaggle_data" / "DelhiNCR Restaurants.csv"

def parse_float(val):
    if not val or val.lower() in ("nan", "new", "-", "none"):
        return None
    try:
        return float(val)
    except ValueError:
        return None

async def seed_from_kaggle():
    if not CSV_FILE_PATH.exists():
        print(f"Error: Could not find {CSV_FILE_PATH}")
        print("Please make sure you have unzipped archive.zip into backend/data_pipeline/kaggle_data")
        return

    print("Starting Kaggle Zomato Delhi NCR Seeder...")
    print(f"Reading from: {CSV_FILE_PATH.name}")

    inserted_count = 0
    duplicate_count = 0
    error_count = 0

    async with async_session() as db:
        with open(CSV_FILE_PATH, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                name = row.get("Restaurant_Name", "").strip()
                locality = row.get("Locality", "").strip()
                
                # Minimum viable required fields
                if not name or not locality:
                    continue
                
                # Parse Latitude/Longitude carefully
                lat = parse_float(row.get("Latitude"))
                lng = parse_float(row.get("Longitude"))
                if lat is None or lng is None:
                    continue  # Missing GPS maps are useless for our discovery logic
                
                # Parse Rating
                rating = parse_float(row.get("Dining_Rating"))
                
                # Parse Cuisine
                categories = row.get("Category", "")
                cuisine_tags = [cat.strip().lower().replace(" ", "_") for cat in categories.split(",") if cat.strip() and cat.strip() != "NaN"]
                
                address = row.get("Address", "Delhi NCR")
                zomato_url = row.get("Website", "")
                
                if zomato_url.lower() == "nan": zomato_url = None
                
                # Create Restaurant Instance
                restaurant = Restaurant(
                    name=name,
                    area=locality,
                    address=address,
                    lat=lat,
                    lng=lng,
                    cuisine_tags=cuisine_tags,
                    rating_zomato=rating,
                    zomato_url=zomato_url,
                    source="kaggle_zomato",
                    is_community=False,
                    is_verified=True
                )
                
                # Naive duplicate check cache (checks db via explicit query)
                # Note: We use execute to check if the combination of name and area already exists.
                # To speed up 2000+ line insertions we will do it sequentially but it could be optimized.
                from sqlalchemy import select
                stmt = select(Restaurant).where(Restaurant.name == name).where(Restaurant.area == locality)
                existing = await db.execute(stmt)
                
                if not existing.scalars().first():
                    try:
                        db.add(restaurant)
                        await db.commit()
                        inserted_count += 1
                        
                        # Just to show progress nicely
                        if inserted_count % 100 == 0:
                            print(f"[ Progress: inserted {inserted_count} restaurants ]")
                            
                    except Exception as e:
                        print(f"Failed on row: {name} - Error: {e}")
                        await db.rollback()
                        error_count += 1
                else:
                    duplicate_count += 1
                    
    print("\nKaggle Seeding Complete!")
    print(f"New Restaurants Added: {inserted_count}")
    print(f"Skipped Duplicates: {duplicate_count}")
    print(f"Errors Encountered: {error_count}")

if __name__ == "__main__":
    # Windows event loop fix for Python 3.8+ if needed
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_from_kaggle())
