from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.orders.model import Order


async def get_orders_paginated(
   db: AsyncSession,
   page: int = 1,
   page_size: int = 20,
   search: str | None = None
):
   query = select(Order)
   count_query = select(func.count()).select_from(Order)

   if search:
      search_filter = or_(
         Order.id.ilike(f"%{search}%"),  # type: ignore
         Order.cod_order.ilike(f"%{search}%")  # type: ignore
      )
      query = query.where(search_filter)
      count_query = count_query.where(search_filter)

   query = query.order_by(func.lower(Order.cod_order))
   total = await db.scalar(count_query) or 0

   offset = (page - 1) * page_size
   result = await db.execute(query.offset(offset).limit(page_size))
   orders = result.scalars().all()

   return {
      "orders": orders,
      "total": total,
      "page": page,
      "page_size": page_size,
      "total_pages": (total + page_size - 1) // page_size if total > 0 else 0,
   }
