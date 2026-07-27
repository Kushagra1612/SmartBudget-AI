from app.database.base import Base
from app.database.database import engine

# Import every model here.
# These imports are REQUIRED so SQLAlchemy
# knows about every table before create_all().

from app.models.user import User
from app.models.transaction import Transaction
from app.models.budget import Budget
from app.models.anomaly import Anomaly
from app.models.chat_history import ChatHistory


def init_db():
    """
    Create database tables.
    """

    Base.metadata.create_all(bind=engine)