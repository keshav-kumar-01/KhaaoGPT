"""
Redis Client — Centralized Redis connection and caching utilities for KhaoGPT
"""
import redis.asyncio as redis
from config import REDIS_URL
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.client = None

    async def connect(self):
        """Initialize Redis connection"""
        if not REDIS_URL:
            logger.warning("REDIS_URL not found, Redis caching will be disabled.")
            return False
        
        try:
            self.client = redis.from_url(REDIS_URL, decode_responses=True)
            # Test connection
            await self.client.ping()
            logger.info("Successfully connected to Redis Cloud.")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None
            return False

    async def disconnect(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from Redis.")

    async def get(self, key: str):
        """Get value from Redis"""
        if self.client:
            return await self.client.get(key)
        return None

    async def set(self, key: str, value: str, ex: int = 3600):
        """Set value in Redis with expiration (default 1 hour)"""
        if self.client:
            await self.client.set(key, value, ex=ex)

# Global Redis instance
redis_client = RedisClient()
