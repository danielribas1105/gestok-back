from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.modules.inventory.schema import InventorySchema
from app.modules.inventory.service import get_inventory_paginated
from app.modules.orders.schema import OrdersSchema
from app.modules.orders.service import get_orders_paginated


router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/", response_model=InventorySchema)
async def get_inventory(
   page: int = Query(1, ge=1),
   page_size: int = Query(20, ge=1, le=100),
   search: str | None = None,
   db: AsyncSession = Depends(get_db)
):
   """
   Recupera produtos em estoque
   """
   return await get_inventory_paginated(db=db, page=page, page_size=page_size, search=search)
