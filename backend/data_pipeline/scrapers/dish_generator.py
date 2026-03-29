import asyncio
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(backend_dir))

from database import async_session
from models.restaurant import Restaurant
from models.dish import Dish
from sqlalchemy import select

# Cuisine to Signature Dishes Mapping (with Taste DNA)
CUISINE_DISH_MAP = {
    "north_indian": [
        {"name": "Butter Chicken", "price": 450, "heat": 4, "sweet": 5, "acid": 4, "umami": 9, "fat": 9, "bitter": 1, "is_veg": False},
        {"name": "Dal Makhani", "price": 320, "heat": 3, "sweet": 3, "acid": 2, "umami": 8, "fat": 8, "bitter": 1, "is_veg": True},
        {"name": "Paneer Tikka", "price": 380, "heat": 6, "sweet": 1, "acid": 4, "umami": 7, "fat": 6, "bitter": 1, "is_veg": True},
    ],
    "south_indian": [
        {"name": "Masala Dosa", "price": 180, "heat": 5, "sweet": 1, "acid": 5, "umami": 6, "fat": 4, "bitter": 1, "is_veg": True},
        {"name": "Medu Vada", "price": 120, "heat": 3, "sweet": 1, "acid": 2, "umami": 5, "fat": 7, "bitter": 1, "is_veg": True},
        {"name": "Filter Coffee", "price": 80, "heat": 0, "sweet": 4, "acid": 2, "umami": 3, "fat": 4, "bitter": 7, "is_veg": True},
    ],
    "chinese": [
        {"name": "Veg Manchurian", "price": 280, "heat": 7, "sweet": 4, "acid": 6, "umami": 8, "fat": 5, "bitter": 2, "is_veg": True},
        {"name": "Chilli Chicken", "price": 350, "heat": 8, "sweet": 3, "acid": 5, "umami": 9, "fat": 6, "bitter": 1, "is_veg": False},
        {"name": "Hakka Noodles", "price": 240, "heat": 4, "sweet": 1, "acid": 3, "umami": 6, "fat": 5, "bitter": 1, "is_veg": True},
    ],
    "street_food": [
        {"name": "Gol Gappa (Pani Puri)", "price": 60, "heat": 8, "sweet": 5, "acid": 9, "umami": 4, "fat": 1, "bitter": 1, "is_veg": True},
        {"name": "Aloo Tikki", "price": 80, "heat": 5, "sweet": 3, "acid": 6, "umami": 6, "fat": 7, "bitter": 1, "is_veg": True},
        {"name": "Pav Bhaji", "price": 150, "heat": 6, "sweet": 2, "acid": 5, "umami": 8, "fat": 8, "bitter": 1, "is_veg": True},
    ],
    "mughlai": [
        {"name": "Chicken Biryani", "price": 350, "heat": 6, "sweet": 2, "acid": 3, "umami": 9, "fat": 7, "bitter": 1, "is_veg": False},
        {"name": "Mutton Seekh Kebab", "price": 420, "heat": 7, "sweet": 1, "acid": 2, "umami": 9, "fat": 8, "bitter": 2, "is_veg": False},
        {"name": "Nihari", "price": 380, "heat": 7, "sweet": 1, "acid": 2, "umami": 10, "fat": 9, "bitter": 1, "is_veg": False},
    ],
    "italian": [
        {"name": "Margherita Pizza", "price": 450, "heat": 2, "sweet": 3, "acid": 5, "umami": 8, "fat": 7, "bitter": 1, "is_veg": True},
        {"name": "Penne Alfredo", "price": 380, "heat": 1, "sweet": 2, "acid": 1, "umami": 7, "fat": 9, "bitter": 1, "is_veg": True},
    ],
    "desserts": [
        {"name": "Gulab Jamun", "price": 100, "heat": 0, "sweet": 10, "acid": 0, "umami": 2, "fat": 7, "bitter": 0, "is_veg": True},
        {"name": "Chocolate Lava Cake", "price": 250, "heat": 0, "sweet": 9, "acid": 1, "umami": 3, "fat": 8, "bitter": 4, "is_veg": True},
    ],
    "cafe": [
        {"name": "Cold Coffee with Ice Cream", "price": 180, "heat": 0, "sweet": 8, "acid": 1, "umami": 3, "fat": 7, "bitter": 5, "is_veg": True},
        {"name": "Grilled Chicken Sandwich", "price": 280, "heat": 3, "sweet": 1, "acid": 3, "umami": 7, "fat": 6, "bitter": 1, "is_veg": False},
    ]
}

DEFAULT_DISHES = [
    {"name": "Signature Platter", "price": 500, "heat": 5, "sweet": 3, "acid": 4, "umami": 7, "fat": 6, "bitter": 2, "is_veg": True},
]

async def generate_dishes_for_all():
    print("Starting Menu Generation (Signature Dishes)...")
    
    async with async_session() as db:
        # Get all restaurants that don't have dishes yet
        stmt = select(Restaurant)
        result = await db.execute(stmt)
        restaurants = result.scalars().all()
        
        print(f"Processing {len(restaurants)} restaurants...")
        
        batch_size = 50
        added_count = 0
        
        for i, rest in enumerate(restaurants):
            # Check if restaurant already has dishes
            dish_check = await db.execute(select(Dish).where(Dish.restaurant_id == rest.id).limit(1))
            if dish_check.scalar_one_or_none():
                continue
            
            # Match dishes based on cuisine tags
            possible_dishes = []
            if rest.cuisine_tags:
                for tag in rest.cuisine_tags:
                    tag_clean = tag.lower().strip().replace(" ", "_")
                    if tag_clean in CUISINE_DISH_MAP:
                        possible_dishes.extend(CUISINE_DISH_MAP[tag_clean])
            
            # Fallback to default if no match
            if not possible_dishes:
                possible_dishes = DEFAULT_DISHES
            
            # Limit to 3 unique dishes
            unique_dishes = {d['name']: d for d in possible_dishes}.values()
            selected_dishes = list(unique_dishes)[:3]
            
            for d in selected_dishes:
                dish = Dish(
                    restaurant_id=rest.id,
                    name=d['name'],
                    price=d['price'],
                    heat_level=float(d['heat']),
                    sweet_level=float(d['sweet']),
                    acid_level=float(d['acid']),
                    umami_level=float(d['umami']),
                    fat_level=float(d['fat']),
                    bitter_level=float(d['bitter']),
                    is_veg=d['is_veg'],
                    taste_summary=f"A popular {d['name']} with a balanced taste profile."
                )
                db.add(dish)
            
            added_count += len(selected_dishes)
            
            # Commit in batches
            if (i + 1) % batch_size == 0:
                await db.commit()
                print(f"Processed {i+1}/{len(restaurants)} restaurants...")
        
        await db.commit()
        print(f"Finished! Total dishes added: {added_count}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(generate_dishes_for_all())
