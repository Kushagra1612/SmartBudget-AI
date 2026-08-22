"""
Unit tests for app/utils/security.py. Pure functions -- no database, no
app, no fixtures needed beyond what's built in.

This replaces eyeballing the output of the old manual test_security.py
script with actual pass/fail assertions.
"""

from app.utils.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_does_not_return_the_plain_password():
    hashed = hash_password("Password123")

    assert hashed != "Password123"
    assert len(hashed) > 20  # bcrypt hashes land around 60 chars


def test_hash_password_salts_each_call_differently():
    # Same input, hashed twice, must produce two different hashes --
    # otherwise bcrypt isn't salting and two users with the same
    # password would have identical hashed_password values in the DB.
    assert hash_password("Password123") != hash_password("Password123")


def test_verify_password_accepts_the_correct_password():
    hashed = hash_password("Password123")

    assert verify_password("Password123", hashed) is True


def test_verify_password_rejects_the_wrong_password():
    hashed = hash_password("Password123")

    assert verify_password("WrongPassword", hashed) is False


def test_access_token_round_trips_its_claims():
    token = create_access_token({"sub": "abc@example.com"})
    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "abc@example.com"
    assert "exp" in payload  # expiry claim gets added automatically


def test_decode_access_token_rejects_garbage_input():
    assert decode_access_token("not.a.real.token") is None


def test_decode_access_token_rejects_a_tampered_signature():
    token = create_access_token({"sub": "abc@example.com"})
    tampered = token[:-4] + "abcd"  # corrupt just the signature portion

    assert decode_access_token(tampered) is None
