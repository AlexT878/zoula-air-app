from datetime import datetime

import pytest
from app.constants.enums import Gender
from app.core.config import settings
from app.models.users import User as UserModel
from app.auth.utils import get_password_hash


def get_valid_user_payload(email="test@zoula.air", password="ComplexPassword123!"):
    return {
        "email": email,
        "password": password,
        "first_name": "Test",
        "last_name": "Pilot",
        "birth_date": "1990-01-01",
        "gender": "male",
        "country": "Romania",
        "phone_country_code": "+40",
        "phone_number": "722123456",
    }


# ==========================================
#              USERS: /me
# ==========================================


@pytest.mark.asyncio
async def test_read_users_me_success(client):
    user_payload = get_valid_user_payload()
    await client.post("/auth/register", json=user_payload)

    login_res = await client.post(
        "/auth/login",
        data={"username": user_payload["email"], "password": user_payload["password"]},
    )
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    res = await client.get("/users/me", headers=headers)

    assert res.status_code == 200
    assert res.json()["email"] == user_payload["email"]
    assert res.json()["first_name"] == user_payload["first_name"]


@pytest.mark.asyncio
async def test_read_users_me_unauthorized(client):
    res = await client.get("/users/me")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_read_users_me_not_found(client, db_session):
    user_payload = get_valid_user_payload(email="ghost@zoula.air")
    user_email = user_payload["email"]
    user_pass = user_payload["password"]

    await client.post("/auth/register", json=user_payload)

    login_res = await client.post(
        "/auth/login", data={"username": user_email, "password": user_pass}
    )
    token = login_res.json()["access_token"]

    db_session.query(UserModel).filter(UserModel.email == user_email).delete()
    db_session.commit()

    headers = {"Authorization": f"Bearer {token}"}
    res = await client.get("/users/me", headers=headers)

    assert res.status_code == 404
    assert res.json()["detail"] == "User not found in database"


# ==========================================
#          USERS: / (Admin Only)
# ==========================================


@pytest.mark.asyncio
async def test_read_all_users_as_admin(client, db_session):
    admin_email = "admin@zoula.air"
    admin_pass = settings.ADMIN_PASSWORD

    admin_user = UserModel(
        email=admin_email,
        first_name="Zoula",
        last_name="Admin",
        hashed_password=get_password_hash(admin_pass),
        birth_date=datetime(1990, 1, 1).date(),
        gender=Gender.OTHER,
        country="N/A",
        phone_country_code="+0",
        phone_number="000000000",
        roles=["admin"],
        is_active=True,
    )
    db_session.add(admin_user)
    db_session.commit()

    login_res = await client.post(
        "/auth/login", data={"username": admin_email, "password": admin_pass}
    )
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    res = await client.get("/users/", headers=headers)

    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert any(u["email"] == admin_email for u in res.json())


@pytest.mark.asyncio
async def test_read_all_users_forbidden_for_regular_user(client, db_session):
    user_payload = get_valid_user_payload()
    await client.post("/auth/register", json=user_payload)

    login_res = await client.post(
        "/auth/login",
        data={"username": user_payload["email"], "password": user_payload["password"]},
    )
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    res = await client.get("/users/", headers=headers)

    assert res.status_code == 403
