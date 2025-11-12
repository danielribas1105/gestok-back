from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import func, or_
from app.modules.users.model import User

async def get_users_paginated(
   db: AsyncSession,
   page: int = 1,
   page_size: int = 20,
   search: str | None = None
):
   query = select(User)
   count_query = select(func.count()).select_from(User)

   if search:
      search_filter = or_(
         User.name.ilike(f"%{search}%"),  # type: ignore
         User.email.ilike(f"%{search}%")  # type: ignore
      )
      query = query.where(search_filter)
      count_query = count_query.where(search_filter)

   query = query.order_by(func.lower(User.name))
   total = await db.scalar(count_query) or 0

   offset = (page - 1) * page_size
   result = await db.execute(query.offset(offset).limit(page_size))
   users = result.scalars().all()

   return {
      "users": users,
      "total": total,
      "page": page,
      "page_size": page_size,
      "total_pages": (total + page_size - 1) // page_size if total > 0 else 0,
   }
