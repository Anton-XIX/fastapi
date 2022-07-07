from fastapi import APIRouter

from app.auth.routes import router as auth_router
from app.statistics.routes import router as stat_router
from app.user_profile.routes import router as user_profile_router
from app.users.routes import router as user_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(
    user_profile_router, prefix="/user_profile", tags=["user_profile"]
)
router.include_router(stat_router, prefix="/statistics", tags=["statistics"])
