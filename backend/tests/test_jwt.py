import pytest
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


@pytest.mark.asyncio
async def test_token_expired(client):
    # Generating a token that expired an hour ago
    expire = datetime.now(timezone.utc) - timedelta(hours=1)
    to_encode = {"sub": "123", "exp": expire, "roles": ["user"]}
    expired_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Trying to access a protected route
    headers = {"Authorization": f"Bearer {expired_token}"}
    res = await client.get("/users/me", headers=headers)

    assert res.status_code == 401
    assert res.json()["detail"] == "Token has expired"


@pytest.mark.asyncio
async def test_token_missing_subject(client):
    to_encode = {
        "roles": ["user"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
    }
    token_no_sub = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    headers = {"Authorization": f"Bearer {token_no_sub}"}
    res = await client.get("/users/me", headers=headers)

    assert res.status_code == 401
    assert res.json()["detail"] == "Token is missing subject (user ID)"


@pytest.mark.asyncio
async def test_token_invalid_signature(client):
    to_encode = {"sub": "123", "roles": ["user"]}
    invalid_token = jwt.encode(to_encode, "CHEIE_GRESITA_123", algorithm=ALGORITHM)

    headers = {"Authorization": f"Bearer {invalid_token}"}
    res = await client.get("/users/me", headers=headers)

    assert res.status_code == 403
    assert res.json()["detail"] == "Could not validate credentials"


@pytest.mark.asyncio
async def test_token_malformed_json(client):
    headers = {"Authorization": "Bearer not-a-jwt-at-all"}
    res = await client.get("/users/me", headers=headers)

    assert res.status_code == 403
    assert res.json()["detail"] == "Could not validate credentials"
