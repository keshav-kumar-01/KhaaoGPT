"""
KhaoGPT Configuration — Environment variables and settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./khaogpt.db")

# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "khaogpt-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 72

# Redis (optional for MVP — fallback to in-memory)
REDIS_URL = os.getenv("REDIS_URL", "")

# Cloudinary (free tier)
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

# Google Places API
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")

# Delhi NCR bounding box
DELHI_NCR_BOUNDS = {
    "lat_min": 28.4,
    "lat_max": 28.9,
    "lng_min": 76.8,
    "lng_max": 77.5,
}

# App settings
APP_NAME = "KhaoGPT"
APP_VERSION = "1.0.0"
CORS_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]
