"""Order Click model — analytics tracking"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from database import Base


class OrderClick(Base):
    __tablename__ = "order_clicks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String)
    dish_id = Column(String)
    restaurant_id = Column(String)
    platform = Column(String(20))
    clicked_at = Column(DateTime, default=datetime.utcnow)
