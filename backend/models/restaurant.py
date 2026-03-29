"""Restaurant model"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, JSON
from database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    area = Column(String(100), index=True)
    address = Column(Text)
    lat = Column(Float)
    lng = Column(Float)
    cuisine_tags = Column(JSON, default=list)
    zomato_url = Column(Text)
    swiggy_url = Column(Text)
    google_maps_url = Column(Text)
    avg_cost_two = Column(Integer)
    avg_delivery_fee = Column(Integer, default=30)
    platform_fee_est = Column(Integer, default=15)
    rating_zomato = Column(Float)
    rating_swiggy = Column(Float)
    is_community = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=True)
    source = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
