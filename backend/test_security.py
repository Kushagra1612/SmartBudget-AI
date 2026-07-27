from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

password = "Password123"

print("=" * 50)

hashed = hash_password(password)

print("Original Password:")
print(password)

print()

print("Hashed Password:")
print(hashed)

print()

print("Password Verification:")
print(
    verify_password(
        password,
        hashed,
    )
)

print()

token = create_access_token(
    {
        "sub": "abc@gmail.com"
    }
)

print("JWT Token:")
print(token)

print()

print("Decoded JWT:")
print(
    decode_access_token(
        token
    )
)

print("=" * 50)