"""Ratings router — post-meal feedback"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.user import User
from models.taste_profile import TasteProfile
from models.dish import Dish
from models.meal_rating import MealRating
from schemas import RatingRequest
from auth import get_current_user
from services.taste_engine import update_taste_dna

router = APIRouter(tags=["ratings"])


@router.post("/ratings")
async def submit_rating(
    req: RatingRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if req.rating not in (1, 2, 3):
        raise HTTPException(status_code=400, detail="Rating must be 1, 2, or 3")

    # Save rating
    rating = MealRating(
        user_id=user.id,
        dish_id=req.dish_id,
        restaurant_id=req.restaurant_id,
        rating=req.rating,
        platform=req.platform,
        actual_cost=req.actual_cost,
        notes=req.notes,
    )
    db.add(rating)

    # Update Taste DNA
    dish_result = await db.execute(select(Dish).where(Dish.id == req.dish_id))
    dish = dish_result.scalar_one_or_none()

    profile_result = await db.execute(
        select(TasteProfile).where(TasteProfile.user_id == user.id)
    )
    profile = profile_result.scalar_one_or_none()

    taste_updated = False
    if dish and profile:
        profile = update_taste_dna(profile, dish, req.rating)
        taste_updated = True

    await db.commit()

    rating_labels = {1: "Loved it! 🎉", 2: "Noted. 📝", 3: "Got it, we'll adjust. 🔧"}

    return {
        "message": rating_labels.get(req.rating, "Thanks for the feedback!"),
        "taste_dna_updated": taste_updated,
    }
