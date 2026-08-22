from app.database.base import Base
from app.database.database import engine

# Import every model so SQLAlchemy knows about every table before
# create_all(). Delegated to app.models (the single source of truth for
# "every model that exists") instead of listing classes here separately --
# two lists of "every model" drift out of sync with each other over time.
from app import models  # noqa: F401


def init_db():
    """
    Create database tables.
    """

    Base.metadata.create_all(bind=engine)