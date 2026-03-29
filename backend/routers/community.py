"""Community router — submit spots, admin approval/rejection"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.user import User
from models.community_submission import CommunitySubmission
from models.restaurant import Restaurant
from models.dish import Dish
from auth import get_current_user, require_admin
from services.community_service import infer_taste_vector, TEXTURE_TAGS
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/community", tags=["community"])


class SubmitSpotRequest(BaseModel):
    spot_name: str
    spot_type: str
    area: str
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    description: str
    must_try_dish: str
    dish_description: str
    approx_price: int
    taste_tags: List[str] = []
    zomato_url: Optional[str] = None
    swiggy_url: Optional[str] = None
    photo_urls: List[str] = []


class RejectRequest(BaseModel):
    reason: str


@router.post("/submit")
async def submit_spot(
    req: SubmitSpotRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Delhi NCR bounding box check
    if req.lat and req.lng:
        if not (28.4 <= req.lat <= 28.9 and 76.8 <= req.lng <= 77.5):
            raise HTTPException(status_code=400, detail="Location must be within Delhi NCR")

    # Check for duplicates
    existing = await db.execute(
        select(CommunitySubmission).where(
            CommunitySubmission.spot_name == req.spot_name,
            CommunitySubmission.area == req.area,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="This spot may already be in our list.")

    submission = CommunitySubmission(
        submitted_by=user.id,
        spot_name=req.spot_name,
        spot_type=req.spot_type,
        area=req.area,
        address=req.address,
        lat=req.lat,
        lng=req.lng,
        description=req.description,
        must_try_dish=req.must_try_dish,
        dish_description=req.dish_description,
        approx_price=req.approx_price,
        taste_tags=req.taste_tags,
        photo_urls=req.photo_urls,
        zomato_url=req.zomato_url,
        swiggy_url=req.swiggy_url,
        status="pending",
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    return {
        "message": "Thank you! Your spot is under review. We usually verify within 24 hours.",
        "submission_id": submission.id,
    }


@router.get("/my-submissions")
async def my_submissions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CommunitySubmission).where(
            CommunitySubmission.submitted_by == user.id
        ).order_by(CommunitySubmission.created_at.desc())
    )
    submissions = result.scalars().all()
    return {
        "submissions": [
            {
                "id": s.id,
                "spot_name": s.spot_name,
                "spot_type": s.spot_type,
                "area": s.area,
                "status": s.status,
                "must_try_dish": s.must_try_dish,
                "created_at": str(s.created_at) if s.created_at else None,
            }
            for s in submissions
        ]
    }


@router.get("/pending")
async def get_pending(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CommunitySubmission).where(
            CommunitySubmission.status == "pending"
        ).order_by(CommunitySubmission.created_at.asc())
    )
    submissions = result.scalars().all()
    return {
        "submissions": [
            {
                "id": s.id,
                "submitted_by": s.submitted_by,
                "spot_name": s.spot_name,
                "spot_type": s.spot_type,
                "area": s.area,
                "address": s.address,
                "description": s.description,
                "must_try_dish": s.must_try_dish,
                "dish_description": s.dish_description,
                "approx_price": s.approx_price,
                "taste_tags": s.taste_tags,
                "photo_urls": s.photo_urls,
                "zomato_url": s.zomato_url,
                "swiggy_url": s.swiggy_url,
                "status": s.status,
                "created_at": str(s.created_at) if s.created_at else None,
            }
            for s in submissions
        ]
    }


@router.post("/{submission_id}/approve")
async def approve_submission(
    submission_id: str,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CommunitySubmission).where(CommunitySubmission.id == submission_id)
    )
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Create restaurant record
    restaurant = Restaurant(
        name=sub.spot_name,
        area=sub.area,
        address=sub.address,
        lat=sub.lat,
        lng=sub.lng,
        cuisine_tags=sub.taste_tags or [],
        zomato_url=sub.zomato_url,
        swiggy_url=sub.swiggy_url,
        avg_cost_two=(sub.approx_price or 0) * 2,
        is_community=True,
        is_verified=True,
        source="community",
    )
    db.add(restaurant)
    await db.flush()

    # Create dish record
    dish_vector = infer_taste_vector(sub.taste_tags or [])
    texture = [t for t in (sub.taste_tags or []) if t.lower() in TEXTURE_TAGS]
    dish = Dish(
        restaurant_id=restaurant.id,
        name=sub.must_try_dish or "Signature Dish",
        price=sub.approx_price,
        taste_summary=sub.dish_description,
        texture_tags=texture,
        heat_level=dish_vector.get("heat_level", 5.0),
        sweet_level=dish_vector.get("sweet_level", 5.0),
        acid_level=dish_vector.get("acid_level", 5.0),
        umami_level=dish_vector.get("umami_level", 5.0),
        fat_level=dish_vector.get("fat_level", 5.0),
        bitter_level=dish_vector.get("bitter_level", 5.0),
    )
    db.add(dish)

    # Update submission status
    sub.status = "approved"
    sub.verified_at = datetime.utcnow()

    await db.commit()
    return {"message": "Approved and added to database", "restaurant_id": restaurant.id}


@router.post("/{submission_id}/reject")
async def reject_submission(
    submission_id: str,
    req: RejectRequest,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CommunitySubmission).where(CommunitySubmission.id == submission_id)
    )
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    sub.status = "rejected"
    sub.rejection_reason = req.reason

    await db.commit()
    return {"message": "Rejected"}
