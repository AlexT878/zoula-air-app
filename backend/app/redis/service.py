from fastapi import Depends
from redis import Redis

from app.redis.client import get_redis


class RedisService:
    def __init__(self, client: Redis):
        self.client = client

    def save_refresh_token(self, user_id: str, token: str, expire_days: int = 7):
        ttl = expire_days * 24 * 60 * 60
        self.client.setex(f"refresh_token:{user_id}", ttl, token)

    def get_refresh_token(self, user_id: str):
        return self.client.get(f"refresh_token:{user_id}")

    def delete_refresh_token(self, user_id: str):
        self.client.delete(f"refresh_token:{user_id}")


def get_redis_service(client: Redis = Depends(get_redis)):
    return RedisService(client)
