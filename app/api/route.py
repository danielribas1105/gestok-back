from fastapi import APIRouter
from modules.users.route import router as users_router
from modules.clients.route import router as clients_router
from modules.products.route import router as products_router
from modules.auth.route import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(clients_router, prefix="/clients", tags=["Clients"])
api_router.include_router(products_router, prefix="/products", tags=["Products"])
