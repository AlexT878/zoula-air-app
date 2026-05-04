import asyncio
import json
import os
from datetime import datetime
from app.db.session import SessionLocal
from app.models.users import User
from app.auth.utils import get_password_hash
from app.core.config import settings
from app.constants.enums import Gender


async def seed_data():
    db = SessionLocal()
    json_path = os.path.join(os.path.dirname(__file__), "mock_data.json")

    try:
        admin_email = "admin@zoula.air"
        admin = db.query(User).filter(User.email == admin_email).first()

        if not admin:
            admin = User(
                email=admin_email,
                first_name="Zoula",
                last_name="Admin",
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                birth_date=datetime(1990, 1, 1).date(),
                gender=Gender.OTHER,
                country="N/A",
                phone_country_code="+0",
                phone_number="000000000",
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
                    birth_date_obj = datetime.strptime(
                        u["birth_date"], "%Y-%m-%d"
                    ).date()

                    new_user = User(
                        email=u["email"],
                        first_name=u["first_name"],
                        last_name=u["last_name"],
                        hashed_password=get_password_hash(u["password"]),
                        birth_date=birth_date_obj,
                        gender=Gender(u["gender"]),
                        country=u["country"],
                        phone_country_code=u["phone_country_code"],
                        phone_number=u["phone_number"],
                        roles=u.get("roles", ["user"]),
                        is_active=u.get("is_active", True),
                    )
                    db.add(new_user)

        db.commit()
        print("🚀 Database seeding complete!")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(seed_data())
