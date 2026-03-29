"""Meal Rating model — post-order feedback"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, SmallInteger, Integer, Text, DateTime
from database import Base


class MealRating(Base):
    __tablename__ = "meal_ratings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    dish_id = Column(String)
    restaurant_id = Column(String)
    rating = Column(SmallInteger)  # 1=loved, 2=ok, 3=disliked
    platform = Column(String(20))
    actual_cost = Column(Integer)
    notes = Column(Text)
    rated_at = Column(DateTime, default=datetime.utcnow)
