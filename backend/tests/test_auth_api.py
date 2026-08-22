"""
Integration tests for /auth/register, /auth/login, /auth/me -- real HTTP
requests through the actual FastAPI app, against the test database.
"""


def test_register_creates_a_user(client, user_credentials):
    response = client.post("/auth/register", json=user_credentials)

    assert response.status_code == 201

    body = response.json()
    assert body["email"] == user_credentials["email"]
    assert body["full_name"] == user_credentials["full_name"]
    assert "id" in body
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_rejects_a_duplicate_email(client, user_credentials):
    client.post("/auth/register", json=user_credentials)
    response = client.post("/auth/register", json=user_credentials)

    assert response.status_code == 409


def test_register_rejects_a_password_under_8_characters(client, user_credentials):
    user_credentials["password"] = "short"
    response = client.post("/auth/register", json=user_credentials)

    assert response.status_code == 422


def test_register_rejects_an_invalid_email(client, user_credentials):
    user_credentials["email"] = "not-an-email"
    response = client.post("/auth/register", json=user_credentials)

    assert response.status_code == 422


def test_login_succeeds_with_correct_credentials(
    client, registered_user, user_credentials
):
    response = client.post(
        "/auth/login",
        data={
            "username": user_credentials["email"],
            "password": user_credentials["password"],
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_fails_with_the_wrong_password(
    client, registered_user, user_credentials
):
    response = client.post(
        "/auth/login",
        data={
            "username": user_credentials["email"],
            "password": "definitely-the-wrong-password",
        },
    )

    assert response.status_code == 401


def test_login_fails_for_an_email_that_was_never_registered(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "nobody@example.com",
            "password": "whatever123",
        },
    )

    assert response.status_code == 401


def test_me_returns_the_currently_authenticated_user(
    client, auth_headers, user_credentials
):
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == user_credentials["email"]


def test_me_requires_a_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me_rejects_an_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401
