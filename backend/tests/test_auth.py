import pytest
from app.core.errors import ErrorCode
from app.models.users import User as UserModel
from app.auth.utils import get_password_hash

# =============================================================
#                       AUTH: REGISTER
# =============================================================


@pytest.mark.asyncio
async def test_register_empty_fields(client):
    payload = {"email": "", "password": "", "full_name": ""}
    res = await client.post("/auth/register", json=payload)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_register_password_complexity(client):
    # No uppercase, no digit, no special character
    res_simple = await client.post(
        "/auth/register",
        json={
            "email": "pass1@zoula.air",
            "password": "password",
            "full_name": "Test Pilot",
        },
    )
    assert res_simple.status_code == 422

    # Shorter than 8 characters
    res_short = await client.post(
        "/auth/register",
        json={
            "email": "pass2@zoula.air",
            "password": "Pas1!",
            "full_name": "Test Pilot",
        },
    )
    assert res_short.status_code == 422

    # No special character
    res_no_spec = await client.post(
        "/auth/register",
        json={
            "email": "pass3@zoula.air",
            "password": "Password123",
            "full_name": "Test Pilot",
        },
    )
    assert res_no_spec.status_code == 422


@pytest.mark.asyncio
async def test_email_with_spaces_and_case(client):
    email_raw = "  Pilot@Zoula.Air  "
    password = "ComplexPassword123!"

    reg_res = await client.post(
        "/auth/register",
        json={"email": email_raw, "password": password, "full_name": "Test Pilot"},
    )
    assert reg_res.status_code == 201

    login_data = {"username": "pilot@zoula.air", "password": password}
    login_res = await client.post("/auth/login", data=login_data)
    assert login_res.status_code == 200


@pytest.mark.asyncio
async def test_register_sql_injection_attempt(client):
    payload = {
        "email": "hacker'; DROP TABLE users; --",
        "password": "ComplexPassword123!",
        "full_name": "Hacker One",
    }
    res = await client.post("/auth/register", json=payload)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "email": "double@zoula.air",
        "password": "ComplexPassword123!",
        "full_name": "Test Pilot",
    }
    await client.post("/auth/register", json=payload)
    res = await client.post("/auth/register", json=payload)
    assert res.status_code == 400
    assert res.json()["detail"]["code"] == ErrorCode.EMAIL_ALREADY_EXISTS


# =============================================================
#                       AUTH: LOGIN
# =============================================================


@pytest.mark.asyncio
async def test_login_empty_fields(client):
    login_data = {"username": "", "password": ""}
    res = await client.post("/auth/login", data=login_data)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    email = "wrongpass@zoula.air"
    await client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "CorrectPassword123!",
            "full_name": "Test Pilot",
        },
    )
    login_data = {"username": email, "password": "WrongPassword!"}
    res = await client.post("/auth/login", data=login_data)
    assert res.status_code == 401
    assert "incorrect" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_wrong_mail(client):
    password = "WrongMail1!"
    await client.post(
        "/auth/register",
        json={
            "email": "wrongmail@zoula.air",
            "password": password,
            "full_name": "Test Pilot",
        },
    )
    login_data = {"username": "wrongmail2@zoula.air", "password": password}
    res = await client.post("/auth/login", data=login_data)
    assert res.status_code == 401
    assert "incorrect" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_inactive_user(client, db_session):
    email = "inactive@zoula.air"
    password = "Password123!"

    inactive_user = UserModel(
        email=email,
        full_name="Inactive Pilot",
        hashed_password=get_password_hash(password),
        roles=["user"],
        is_active=False,
    )
    db_session.add(inactive_user)
    db_session.commit()

    login_data = {"username": email, "password": password}
    res = await client.post("/auth/login", data=login_data)

    assert res.status_code == 400
    assert res.json()["detail"] == "Inactive user"


# =============================================================
#                       AUTH: TOKEN
# =============================================================


@pytest.mark.asyncio
async def test_refresh_token_success(client):
    user_payload = {
        "email": "refresh@zoula.air",
        "password": "ComplexPassword123!",
        "full_name": "Test Pilot",
    }
    await client.post("/auth/register", json=user_payload)

    login_data = {
        "username": user_payload["email"],
        "password": user_payload["password"],
    }
    login_res = await client.post("/auth/login", data=login_data)
    refresh_token = login_res.json()["refresh_token"]

    res = await client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert res.status_code == 200
    assert "access_token" in res.json()
    assert res.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_token_invalid_type(client):
    user_payload = {
        "email": "type-test@zoula.air",
        "password": "ComplexPassword123!",
        "full_name": "Test Pilot",
    }
    await client.post("/auth/register", json=user_payload)

    login_data = {
        "username": user_payload["email"],
        "password": user_payload["password"],
    }
    login_res = await client.post("/auth/login", data=login_data)
    access_token = login_res.json()["access_token"]

    # Send access_token instead of refresh_token
    res = await client.post("/auth/refresh", json={"refresh_token": access_token})

    assert res.status_code == 403
    assert "Invalid token type" in res.json()["detail"]


@pytest.mark.asyncio
async def test_refresh_token_malformed(client):
    res = await client.post("/auth/refresh", json={"refresh_token": "invalid-token"})

    assert res.status_code == 403
    assert "Could not validate credentials" in res.json()["detail"]
