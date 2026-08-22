from .ai import router as ai_router
from .anomaly import router as anomaly_router
from .auth import router as auth_router
from .budget import router as budget_router
from .dashboard import router as dashboard_router
from .goal import router as goal_router
from .transactions import router as transactions_router
from .upload import router as upload_router

__all__ = [
    "ai_router",
    "anomaly_router",
    "auth_router",
    "budget_router",
    "dashboard_router",
    "goal_router",
    "transactions_router",
    "upload_router",
]