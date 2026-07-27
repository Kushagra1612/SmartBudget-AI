from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.exceptions.auth_exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
)


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        user: UserCreate,
    ) -> User:

        # Normalize email
        email = user.email.strip().lower()

        stmt = select(User).where(
            User.email == email,
            User.is_deleted == False,
        )

        existing_user = db.execute(stmt).scalar_one_or_none()

        if existing_user:
            raise UserAlreadyExistsError(
                "Email already registered."
            )

        new_user = User(
            full_name=user.full_name.strip(),
            email=email,
            hashed_password=hash_password(user.password),
        )

        try:

            db.add(new_user)

            db.commit()

            db.refresh(new_user)

            return new_user

        except Exception:

            db.rollback()

            raise

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str,
    ) -> User:

        email = email.strip().lower()

        stmt = select(User).where(
            User.email == email,
            User.is_deleted == False,
        )

        user = db.execute(stmt).scalar_one_or_none()

        if user is None:
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        return user

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ) -> Token:

        user = AuthService.authenticate_user(
            db,
            email,
            password,
        )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )