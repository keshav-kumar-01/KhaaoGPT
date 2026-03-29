"""Taste Profile model — one row per user"""
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, JSON
from database import Base


class TasteProfile(Base):
    __tablename__ = "taste_profiles"

    user_id = Column(String, primary_key=True)
    heat_ceiling = Column(Float, default=5.0)
    sweet_tolerance = Column(Float, default=5.0)
    acid_affinity = Column(Float, default=5.0)
    umami_affinity = Column(Float, default=5.0)
    fat_palate = Column(Float, default=5.0)
    bitter_tolerance = Column(Float, default=5.0)
    texture_pref = Column(String(50))
    cuisine_scores = Column(JSON, default=dict)
    total_ratings = Column(Integer, default=0)
    quiz_completed = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
