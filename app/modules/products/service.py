from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.products.model import Product

async def get_products_paginated(
   db: AsyncSession,
   page: int = 1,
   page_size: int = 20,
   search: str | None = None
):
   query = select(Product)
   count_query = select(func.count()).select_from(Product)

   if search:
      search_filter = or_(
         Product.cod_product.ilike(f"%{search}%"),  # type: ignore
         Product.description.ilike(f"%{search}%"),  # type: ignore
      )
      query = query.where(search_filter)
      count_query = count_query.where(search_filter)

   query = query.order_by(func.lower(Product.cod_product))
   total = await db.scalar(count_query) or 0

   offset = (page - 1) * page_size
   result = await db.execute(query.offset(offset).limit(page_size))
   products = result.scalars().all()

   return {
      "products": products,
      "total": total,
      "page": page,
      "page_size": page_size,
      "total_pages": (total + page_size - 1) // page_size if total > 0 else 0,
   }