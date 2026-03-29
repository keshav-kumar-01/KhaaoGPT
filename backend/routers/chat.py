"""Chat router — main conversation endpoint"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.user import User
from models.taste_profile import TasteProfile
from models.restaurant import Restaurant
from models.dish import Dish
from schemas import ChatRequest
from auth import get_current_user
from services.taste_engine import score_dish_for_user
from services.first_bite import generate_first_bite
from services.order_bridge import build_order_links
from services.intent_parser import parse_intent

router = APIRouter(tags=["chat"])


@router.post("/chat")
async def chat(
    request: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # 1. Parse intent
    intent = parse_intent(request.message)

    # 2. Fetch user taste profile
    result = await db.execute(
        select(TasteProfile).where(TasteProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        return {
            "recommendations": [],
            "message": "Please take the Taste DNA quiz first to get personalised recommendations!"
        }

    # 3. Build restaurant query (Fuzzy search for area)
    query = select(Restaurant).where(Restaurant.is_active == True)
    if intent["area"]:
        query = query.where(Restaurant.area.ilike(f"%{intent['area']}%"))
    elif request.area:
        query = query.where(Restaurant.area.ilike(f"%{request.area}%"))

    if not intent.get("include_community"):
        query = query.where(Restaurant.is_verified == True)

    result = await db.execute(query)
    restaurants = result.scalars().all()

    if not restaurants:
        return {
            "recommendations": [],
            "message": f"No restaurants found{' in ' + (intent['area'] or request.area or '') if (intent['area'] or request.area) else ''}. Try a different area!"
        }

    # 4. Score all dishes across candidate restaurants
    scored_dishes = []
    for restaurant in restaurants:
        dish_result = await db.execute(
            select(Dish).where(
                Dish.restaurant_id == restaurant.id,
                Dish.is_available == True,
            )
        )
        dishes = dish_result.scalars().all()

        for dish in dishes:
            # Veg filter
            if intent["is_veg"] is True and not dish.is_veg:
                continue
            if intent["is_veg"] is False and dish.is_veg:
                continue

            # Cuisine filter
            if intent["cuisine"] and dish.cuisine_type and dish.cuisine_type != intent["cuisine"]:
                continue

            # Budget: true cost check
            true_cost = (dish.price or 0) + (restaurant.avg_delivery_fee or 0) + (restaurant.platform_fee_est or 0)
            if intent["budget_max"] and true_cost > intent["budget_max"]:
                continue

            score = score_dish_for_user(dish, profile)

            # Mood bonus
            if intent["mood"]:
                mood_map = {
                    "spicy": ("heat_level", 7),
                    "mild": ("heat_level", 2),
                    "sweet": ("sweet_level", 7),
                    "tangy": ("acid_level", 7),
                    "rich": ("fat_level", 7),
                    "light": ("fat_level", 2),
                    "crispy": ("texture", "crispy"),
                }
                if intent["mood"] in mood_map:
                    axis, target = mood_map[intent["mood"]]
                    if axis == "texture":
                        if target in (dish.texture_tags or []):
                            score += 10
                    else:
                        dish_val = getattr(dish, axis, 5.0)
                        if isinstance(target, int) and dish_val >= target:
                            score += 10

            first_bite = generate_first_bite(dish, profile)
            links = build_order_links(restaurant)

            scored_dishes.append({
                "dish_id": dish.id,
                "dish_name": dish.name,
                "restaurant_name": restaurant.name,
                "restaurant_area": restaurant.area or "",
                "score": round(min(100, max(0, score)), 1),
                "first_bite": first_bite,
                "true_cost": true_cost,
                "price": dish.price or 0,
                "delivery_fee": restaurant.avg_delivery_fee or 0,
                "platform_fee": restaurant.platform_fee_est or 0,
                "is_veg": dish.is_veg,
                "is_community": restaurant.is_community,
                "cuisine_type": dish.cuisine_type,
                "taste_summary": dish.taste_summary,
                "order_links": links,
            })

    # 5. Sort by score, return top 5
    top = sorted(scored_dishes, key=lambda x: x["score"], reverse=True)[:5]

    if not top:
        return {
            "recommendations": [],
            "message": "No matching dishes found for your request. Try adjusting your filters!"
        }

    # Build conversational message
    msg = f"Found {len(top)} dishes that match your taste! "
    if intent["mood"]:
        msg += f"Focused on {intent['mood']} options. "
    if intent["area"]:
        msg += f"In {intent['area']}. "

    return {
        "recommendations": top,
        "message": msg.strip(),
    }
