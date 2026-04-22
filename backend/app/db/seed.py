import asyncio
import json
import os
from app.db.session import SessionLocal
from app.models.users import User
from app.auth.utils import get_password_hash
from app.core.config import settings


async def seed_data():
    db = SessionLocal()
    json_path = os.path.join(os.path.dirname(__file__), "mock_data.json")

    try:
        admin_email = "admin@zoula.air"
        admin = db.query(User).filter(User.email == admin_email).first()

        if not admin:
            admin = User(
                email=admin_email,
                full_name="Zoula Admin",
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                roles=["admin"],
                is_active=True,
            )
            db.add(admin)

        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for u in data.get("test_users", []):
                exists = db.query(User).filter(User.email == u["email"]).first()
                if not exists:
                    new_user = User(
                        email=u["email"],
                        full_name=u["full_name"],
                        hashed_password=get_password_hash(u["password"]),
                        roles=u["roles"],
                        is_active=True,
                    )
                    db.add(new_user)
                    print(f"➕ Added mock user: {u['email']}")

        db.commit()
        print("🚀 Database seeding complete!")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(seed_data())
