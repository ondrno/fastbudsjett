from fastapi import APIRouter

from app.api.api_v1.endpoints import categories, items, login, payments, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])

