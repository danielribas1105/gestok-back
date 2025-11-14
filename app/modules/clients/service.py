from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.clients.model import Client

async def get_clients_paginated(
   db: AsyncSession,
   page: int = 1,
   page_size: int = 20,
   search: str | None = None
):
   query = select(Client)
   count_query = select(func.count()).select_from(Client)

   if search:
      search_filter = or_(
         Client.cod_client.ilike(f"%{search}%"),  # type: ignore
         Client.client.ilike(f"%{search}%"),  # type: ignore
      )
      query = query.where(search_filter)
      count_query = count_query.where(search_filter)

   query = query.order_by(func.lower(Client.cod_client))
   total = await db.scalar(count_query) or 0

   offset = (page - 1) * page_size
   result = await db.execute(query.offset(offset).limit(page_size))
   clients = result.scalars().all()

   return {
      "clients": clients,
      "total": total,
      "page": page,
      "page_size": page_size,
      "total_pages": (total + page_size - 1) // page_size if total > 0 else 0,
   }