import pytest
from app.constants.enums import Gender
from app.core.errors import ErrorCode
from app.models.users import User as UserModel
from app.auth.utils import get_password_hash
from datetime import date


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


# =============================================================
#                       AUTH: REGISTER
# =============================================================


@pytest.mark.asyncio
async def test_register_empty_fields(client):
    res = await client.post("/auth/register", json={})
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_register_password_complexity(client):
    payload = get_valid_user_payload()

    payload["password"] = "simplepass"
    res_simple = await client.post("/auth/register", json=payload)
    assert res_simple.status_code == 422

    payload["password"] = "Short1!"
    res_short = await client.post("/auth/register", json=payload)
    assert res_short.status_code == 422


@pytest.mark.asyncio
async def test_register_age_validation(client):
    payload = get_valid_user_payload()

    payload["birth_date"] = str(date.today().replace(year=date.today().year - 10))
    res_young = await client.post("/auth/register", json=payload)
    assert res_young.status_code == 422

    payload["birth_date"] = "1850-01-01"
    res_old = await client.post("/auth/register", json=payload)
    assert res_old.status_code == 422


@pytest.mark.asyncio
async def test_register_name_validation(client):
    payload = get_valid_user_payload()

    payload["first_name"] = "Ion123"
    res = await client.post("/auth/register", json=payload)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_register_phone_validation(client):
    payload = get_valid_user_payload()

    payload["phone_country_code"] = "40"
    res_no_plus = await client.post("/auth/register", json=payload)
    assert res_no_plus.status_code == 422

    payload["phone_country_code"] = "+40"
    payload["phone_number"] = "abc12345"
    res_invalid_chars = await client.post("/auth/register", json=payload)
    assert res_invalid_chars.status_code == 422


@pytest.mark.asyncio
async def test_email_normalization(client):
    payload = get_valid_user_payload(email="  User@Zoula.Air  ")
    password = payload["password"]

    res = await client.post("/auth/register", json=payload)
    assert res.status_code == 201

    login_data = {"username": "user@zoula.air", "password": password}
    login_res = await client.post("/auth/login", data=login_data)
    assert login_res.status_code == 200


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = get_valid_user_payload(email="duplicate@zoula.air")
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
        first_name="Inactive",
        last_name="Pilot",
        birth_date=date(1990, 1, 1),
        gender=Gender.MALE,
        country="Romania",
        phone_country_code="+40",
        phone_number="722000000",
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
    user_payload = get_valid_user_payload()
    await client.post("/auth/register", json=user_payload)

    login_data = {
        "username": user_payload["email"],
        "password": user_payload["password"],
    }
    login_res = await client.post("/auth/login", data=login_data)
    assert login_res.status_code == 200

    res = await client.post("/auth/refresh")

    assert res.status_code == 200
    assert "access_token" in res.json()
    assert res.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_token_invalid_type(client):
    user_payload = get_valid_user_payload()
    await client.post("/auth/register", json=user_payload)

    login_data = {
        "username": user_payload["email"],
        "password": user_payload["password"],
    }
    login_res = await client.post("/auth/login", data=login_data)
    access_token = login_res.json()["access_token"]

    # Send access_token instead of refresh_token
    client.cookies.update({"refresh_token": access_token})
    res = await client.post("/auth/refresh")

    assert res.status_code == 403
    assert "Invalid token type" in res.json()["detail"]


@pytest.mark.asyncio
async def test_refresh_token_malformed(client):
    client.cookies.update({"refresh_token": "invalid-token"})
    res = await client.post("/auth/refresh")

    assert res.status_code == 403
    assert "Could not validate credentials" in res.json()["detail"]
