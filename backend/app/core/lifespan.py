import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import SessionLocal
from app.db.base import Base
from app.db.session import engine
from app.redis.client import redis_client

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("\n" + "=" * 50)
    logger.info("STARTING ZOULA AIR BACKEND")
    print("=" * 50 + "\n")
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        logger.info("✅ Postgres: Connected successfully!")
    except Exception as e:
        logger.error(f"❌ Postgres: Connection failed: {e}")
    finally:
        db.close()

    try:
        if redis_client.ping():
            logger.info("✅ Redis: Connected successfully!")
    except Exception as e:
        logger.error(f"❌ Redis: Connection failed: {e}")
    finally:
        pass

    yield

    logger.info("🛑 Stopping Zoula Air backend systems...")
