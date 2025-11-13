from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.modules.products.schema import ProductSchema
from app.modules.products.service import get_products_paginated

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=ProductSchema)
async def get_products(
   page: int = Query(1, ge=1),
   page_size: int = Query(20, ge=1, le=100),
   search: str | None = None,
   db: AsyncSession = Depends(get_db)
):
   """
   Recupera todos os produtos cadastrados
   """
   return await get_products_paginated(db=db, page=page, page_size=page_size, search=search)