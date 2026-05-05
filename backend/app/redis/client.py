import redis

from app.core.config import settings

redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
    max_connections=10,
)

redis_client = redis.Redis(connection_pool=redis_pool)


def get_redis():
    client = redis.Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        client.close()
