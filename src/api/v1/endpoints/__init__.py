from .weather import router as weather_router
from .auth import router as auth_router
from .history import router as history_router

__all__ = ["weather_router", "auth_router", "history_router"]
