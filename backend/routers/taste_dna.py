"""Taste DNA router — quiz questions, submit answers, get profile"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.taste_profile import TasteProfile
from models.user import User
from schemas import QuizSubmission, TasteProfileResponse
from auth import get_current_user
from services.taste_engine import process_quiz_answers

router = APIRouter(prefix="/taste-dna", tags=["taste-dna"])

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "You're eating chips. Do you go for:",
        "options": ["Plain", "Masala", "Most extreme flavour in the bag"],
        "maps_to": "heat_ceiling + intensity",
    },
    {
        "id": 2,
        "question": "Does lemon/imli on food feel like:",
        "options": ["Brightness", "Neutral", "Sharp and annoying"],
        "maps_to": "acid_affinity",
    },
    {
        "id": 3,
        "question": "Rate your relationship with bitterness (coffee, dark chocolate, karela):",
        "options": ["Love it", "Fine", "Avoid it"],
        "maps_to": "bitter_tolerance",
    },
    {
        "id": 4,
        "question": "Do you prefer food that feels:",
        "options": ["Light and clean", "Balanced", "Rich and filling"],
        "maps_to": "fat_palate + umami",
    },
    {
        "id": 5,
        "question": "Pick your most-eaten cuisine:",
        "options": [
            "North Indian", "South Indian", "Chinese", "Italian",
            "Street Food", "Mughlai", "Punjabi", "Bengali",
            "Korean", "Mexican"
        ],
        "maps_to": "cuisine_scores baseline",
    },
]


@router.get("/quiz")
async def get_quiz():
    return {"questions": QUIZ_QUESTIONS}


@router.post("/quiz")
async def submit_quiz(
    submission: QuizSubmission,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TasteProfile).where(TasteProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        profile = TasteProfile(user_id=user.id)
        db.add(profile)

    # Process quiz answers
    answers_data = [{"question_id": a.question_id, "answer": a.answer} for a in submission.answers]
    profile_values = process_quiz_answers(answers_data)

    # Update profile
    profile.heat_ceiling = profile_values["heat_ceiling"]
    profile.sweet_tolerance = profile_values["sweet_tolerance"]
    profile.acid_affinity = profile_values["acid_affinity"]
    profile.umami_affinity = profile_values["umami_affinity"]
    profile.fat_palate = profile_values["fat_palate"]
    profile.bitter_tolerance = profile_values["bitter_tolerance"]
    profile.texture_pref = profile_values["texture_pref"]
    profile.cuisine_scores = profile_values["cuisine_scores"]
    profile.quiz_completed = True

    await db.commit()
    await db.refresh(profile)

    return {
        "message": "Taste DNA created!",
        "profile": {
            "heat_ceiling": profile.heat_ceiling,
            "sweet_tolerance": profile.sweet_tolerance,
            "acid_affinity": profile.acid_affinity,
            "umami_affinity": profile.umami_affinity,
            "fat_palate": profile.fat_palate,
            "bitter_tolerance": profile.bitter_tolerance,
            "texture_pref": profile.texture_pref,
            "cuisine_scores": profile.cuisine_scores,
            "quiz_completed": profile.quiz_completed,
        }
    }


@router.get("/profile")
async def get_profile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TasteProfile).where(TasteProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Taste profile not found. Take the quiz first!")

    return {
        "heat_ceiling": profile.heat_ceiling,
        "sweet_tolerance": profile.sweet_tolerance,
        "acid_affinity": profile.acid_affinity,
        "umami_affinity": profile.umami_affinity,
        "fat_palate": profile.fat_palate,
        "bitter_tolerance": profile.bitter_tolerance,
        "texture_pref": profile.texture_pref,
        "cuisine_scores": profile.cuisine_scores,
        "total_ratings": profile.total_ratings,
        "quiz_completed": profile.quiz_completed,
    }
