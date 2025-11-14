from fastapi import APIRouter
from app.api.status import router as status_router
from app.modules.users.route import router as users_router
from app.modules.clients.route import router as clients_router
from app.modules.products.route import router as products_router
from app.modules.auth.route import router as auth_router
from app.modules.orders.route import router as orders_router
from app.modules.inventory.route import router as inventory_router

api_router = APIRouter()

api_router.include_router(status_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(clients_router)
api_router.include_router(products_router)
api_router.include_router(orders_router)
api_router.include_router(inventory_router)
