from sqlalchemy.orm import sessionmaker

from app.database.database import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db():
    """
    FastAPI dependency.

    Usage:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()