"""
KhaoGPT — Taste Intelligence. Food Discovery. Delhi NCR.
Main Vercel Gateway entry point.
"""
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# This is critical for Vercel Monorepo: Add backend root to path
# so that modules from backend/ folder can be imported properly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db
from config import APP_NAME, APP_VERSION
from routers.auth_router import router as auth_router
from routers.taste_dna import router as taste_dna_router
from routers.chat import router as chat_router
from routers.ratings import router as ratings_router
from routers.community import router as community_router
from routers.restaurants import router as restaurants_router
from redis_client import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    await init_db()
    # Connect to Redis
    await redis_client.connect()
    yield
    # Shutdown
    await redis_client.disconnect()


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Taste-intelligent food discovery for Delhi NCR",
    lifespan=lifespan,
)

# CORS — User Requested Fix
origins = [
    "https://khaao-gpt-web.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",  # Adding Vite default too
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Included routers
app.include_router(auth_router)
app.include_router(taste_dna_router)
app.include_router(chat_router)
app.include_router(ratings_router)
app.include_router(community_router)
app.include_router(restaurants_router)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {APP_NAME} v{APP_VERSION}",
        "status": "online",
        "region": "Delhi NCR"
    }


@app.get("/health")
async def health():
    return {"status": "ok", "message": "Backend connections healthy"}
