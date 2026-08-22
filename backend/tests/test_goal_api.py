"""
Integration tests for /goals -- full CRUD.
"""

from datetime import date, timedelta


def _goal_payload(**overrides):
    payload = {
        "title": "Emergency Fund",
        "target_amount": "50000",
        "target_date": str(date.today() + timedelta(days=180)),
    }
    payload.update(overrides)
    return payload


def test_requires_authentication(client):
    response = client.post("/goals", json=_goal_payload())
    assert response.status_code == 401


def test_create_goal(client, auth_headers):
    response = client.post("/goals", json=_goal_payload(), headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Emergency Fund"
    assert float(body["target_amount"]) == 50000
    assert float(body["current_amount"]) == 0


def test_create_goal_rejects_a_non_positive_target_amount(client, auth_headers):
    response = client.post(
        "/goals",
        json=_goal_payload(target_amount="0"),
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_list_goals_returns_only_the_current_users_goals(
    client, auth_headers, user_credentials
):
    client.post("/goals", json=_goal_payload(title="My Goal"), headers=auth_headers)

    other_credentials = dict(user_credentials, email="other_goal_user@example.com")
    client.post("/auth/register", json=other_credentials)
    other_login = client.post(
        "/auth/login",
        data={
            "username": other_credentials["email"],
            "password": other_credentials["password"],
        },
    )
    other_headers = {
        "Authorization": f"Bearer {other_login.json()['access_token']}"
    }
    client.post(
        "/goals", json=_goal_payload(title="Someone Else's Goal"), headers=other_headers
    )

    response = client.get("/goals", headers=auth_headers)

    assert response.status_code == 200
    titles = [g["title"] for g in response.json()]
    assert titles == ["My Goal"]


def test_get_a_single_goal(client, auth_headers):
    created = client.post(
        "/goals", json=_goal_payload(), headers=auth_headers
    ).json()

    response = client.get(f"/goals/{created['id']}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_a_nonexistent_goal_returns_404(client, auth_headers):
    import uuid

    response = client.get(f"/goals/{uuid.uuid4()}", headers=auth_headers)
    assert response.status_code == 404


def test_update_goal_progress(client, auth_headers):
    created = client.post(
        "/goals", json=_goal_payload(), headers=auth_headers
    ).json()

    response = client.put(
        f"/goals/{created['id']}",
        json={"current_amount": "15000"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert float(response.json()["current_amount"]) == 15000


def test_delete_goal(client, auth_headers):
    created = client.post(
        "/goals", json=_goal_payload(), headers=auth_headers
    ).json()

    delete_response = client.delete(f"/goals/{created['id']}", headers=auth_headers)
    assert delete_response.status_code == 200

    get_response = client.get(f"/goals/{created['id']}", headers=auth_headers)
    assert get_response.status_code == 404
