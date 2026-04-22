import pytest
from app.models.users import User as UserModel
from app.auth.utils import get_password_hash

# ==========================================
#              USERS: /me
# ==========================================


@pytest.mark.asyncio
async def test_read_users_me_success(client):
    user_payload = {
        "email": "me@zoula.air",
        "password": "ComplexPassword123!",
        "full_name": "Test Pilot",
    }
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
    assert res.json()["full_name"] == user_payload["full_name"]


@pytest.mark.asyncio
async def test_read_users_me_unauthorized(client):
    res = await client.get("/users/me")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_read_users_me_not_found(client, db_session):
    user_email = "ghost@zoula.air"
    user_pass = "Boo12345!"

    await client.post(
        "/auth/register",
        json={"email": user_email, "password": user_pass, "full_name": "Ghost"},
    )
    login_res = await client.post(
        "/auth/login", data={"username": user_email, "password": user_pass}
    )
    token = login_res.json()["access_token"]

    # Delete user
    db_session.query(UserModel).filter(UserModel.email == user_email).delete()
    db_session.commit()

    # Trying to access /me with a token that is technically still valid as a signature
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
    admin_pass = "AdminPassword123!"

    admin_user = UserModel(
        email=admin_email,
        full_name="System Admin",
        hashed_password=get_password_hash(admin_pass),
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
    user_email = "pilot@zoula.air"
    user_pass = "PilotPassword123!"

    regular_user = UserModel(
        email=user_email,
        full_name="Regular Pilot",
        hashed_password=get_password_hash(user_pass),
        roles=["user"],
        is_active=True,
    )
    db_session.add(regular_user)
    db_session.commit()

    login_res = await client.post(
        "/auth/login", data={"username": user_email, "password": user_pass}
    )
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    res = await client.get("/users/", headers=headers)

    assert res.status_code == 403
