"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List


# ── Auth ──
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    area: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    area: Optional[str] = None
    is_admin: bool = False


# ── Taste DNA ──
class QuizAnswer(BaseModel):
    question_id: int
    answer: str

class QuizSubmission(BaseModel):
    answers: List[QuizAnswer]

class TasteProfileResponse(BaseModel):
    heat_ceiling: float
    sweet_tolerance: float
    acid_affinity: float
    umami_affinity: float
    fat_palate: float
    bitter_tolerance: float
    texture_pref: Optional[str] = None
    cuisine_scores: dict = {}
    total_ratings: int = 0
    quiz_completed: bool = False


# ── Chat ──
class ChatRequest(BaseModel):
    message: str
    area: Optional[str] = None

class DishRecommendation(BaseModel):
    dish_id: str
    dish_name: str
    restaurant_name: str
    restaurant_area: str
    score: float
    first_bite: str
    true_cost: int
    price: int
    delivery_fee: int
    platform_fee: int
    is_veg: bool
    is_community: bool
    cuisine_type: Optional[str] = None
    taste_summary: Optional[str] = None
    order_links: dict

class ChatResponse(BaseModel):
    recommendations: List[DishRecommendation]
    message: str


# ── Rating ──
class RatingRequest(BaseModel):
    dish_id: str
    restaurant_id: str
    rating: int  # 1=loved, 2=ok, 3=disliked
    platform: Optional[str] = None
    actual_cost: Optional[int] = None
    notes: Optional[str] = None


# ── Community ──
class CommunitySubmissionResponse(BaseModel):
    id: str
    spot_name: str
    spot_type: Optional[str] = None
    area: str
    description: Optional[str] = None
    must_try_dish: Optional[str] = None
    status: str
    photo_urls: List[str] = []
    created_at: Optional[str] = None


# ── Restaurant ──
class RestaurantResponse(BaseModel):
    id: str
    name: str
    area: Optional[str] = None
    cuisine_tags: list = []
    avg_cost_two: Optional[int] = None
    rating_zomato: Optional[float] = None
    is_community: bool = False
    zomato_url: Optional[str] = None
    swiggy_url: Optional[str] = None
