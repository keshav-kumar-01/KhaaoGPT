"""Community Submission model"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, JSON
from database import Base


class CommunitySubmission(Base):
    __tablename__ = "community_submissions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    submitted_by = Column(String)
    spot_name = Column(String(200), nullable=False)
    spot_type = Column(String(50))
    address = Column(Text)
    area = Column(String(100))
    lat = Column(Float)
    lng = Column(Float)
    description = Column(Text)
    must_try_dish = Column(String(200))
    dish_description = Column(Text)
    taste_tags = Column(JSON, default=list)
    approx_price = Column(Integer)
    photo_urls = Column(JSON, default=list)
    zomato_url = Column(Text)
    swiggy_url = Column(Text)
    status = Column(String(20), default="pending", index=True)
    rejection_reason = Column(Text)
    verified_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
