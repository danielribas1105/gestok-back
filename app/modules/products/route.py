from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.modules.products.model import Product
from app.modules.products.schema import ProductCreate, ProductRead, ProductSchema
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

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
   # Verifica se produto já existe
   existing = await db.execute(select(Product).where(Product.cod_product == product.cod_product))
   if existing.scalars().first():
      raise HTTPException(status_code=400, detail="Cliente já cadastrado")

   new_product = Product(
      cod_product=product.cod_product,
      description=product.description,
      unit=product.unit,
      value=product.value,
      active=True,
   )
   db.add(new_product)
   await db.commit()
   await db.refresh(new_product)
   return new_product