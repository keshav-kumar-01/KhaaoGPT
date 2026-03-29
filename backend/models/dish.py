"""Dish model"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, JSON
from database import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_id = Column(String, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    price = Column(Integer)
    cuisine_type = Column(String(100), index=True)
    # Taste vector (0.0 to 10.0 each axis)
    heat_level = Column(Float, default=5.0)
    sweet_level = Column(Float, default=3.0)
    acid_level = Column(Float, default=3.0)
    umami_level = Column(Float, default=5.0)
    fat_level = Column(Float, default=5.0)
    bitter_level = Column(Float, default=2.0)
    texture_tags = Column(JSON, default=list)
    taste_summary = Column(Text)
    key_ingredients = Column(JSON, default=list)
    zomato_dish_url = Column(Text)
    swiggy_dish_url = Column(Text)
    is_veg = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
