"""Restaurants & Dishes router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.user import User
from models.restaurant import Restaurant
from models.dish import Dish
from models.order_click import OrderClick
from auth import get_current_user
from services.order_bridge import build_order_links

router = APIRouter(tags=["restaurants"])


@router.get("/restaurants")
async def list_restaurants(
    area: str = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Restaurant).where(Restaurant.is_active == True)
    if area:
        query = query.where(Restaurant.area == area)
    query = query.limit(50)

    result = await db.execute(query)
    restaurants = result.scalars().all()

    return {
        "restaurants": [
            {
                "id": r.id,
                "name": r.name,
                "area": r.area,
                "cuisine_tags": r.cuisine_tags or [],
                "avg_cost_two": r.avg_cost_two,
                "rating_zomato": r.rating_zomato,
                "is_community": r.is_community,
            }
            for r in restaurants
        ]
    }


@router.get("/restaurants/{restaurant_id}")
async def get_restaurant(
    restaurant_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    r = result.scalar_one_or_none()
    if not r:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Get dishes
    dishes_result = await db.execute(
        select(Dish).where(Dish.restaurant_id == restaurant_id)
    )
    dishes = dishes_result.scalars().all()

    links = build_order_links(r)

    return {
        "restaurant": {
            "id": r.id,
            "name": r.name,
            "area": r.area,
            "address": r.address,
            "cuisine_tags": r.cuisine_tags or [],
            "avg_cost_two": r.avg_cost_two,
            "rating_zomato": r.rating_zomato,
            "is_community": r.is_community,
            "order_links": links,
        },
        "dishes": [
            {
                "id": d.id,
                "name": d.name,
                "price": d.price,
                "cuisine_type": d.cuisine_type,
                "is_veg": d.is_veg,
                "taste_summary": d.taste_summary,
            }
            for d in dishes
        ],
    }


@router.get("/order-links/{restaurant_id}")
async def get_order_links(
    restaurant_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    r = result.scalar_one_or_none()
    if not r:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return build_order_links(r)


@router.post("/order-click")
async def track_order_click(
    dish_id: str,
    restaurant_id: str,
    platform: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    click = OrderClick(
        user_id=user.id,
        dish_id=dish_id,
        restaurant_id=restaurant_id,
        platform=platform,
    )
    db.add(click)
    await db.commit()

    # Return the redirect URL
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    r = result.scalar_one_or_none()
    if r:
        links = build_order_links(r)
        return {"redirect_url": links.get(platform, links.get("google_maps"))}

    return {"redirect_url": None}
