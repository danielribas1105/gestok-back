from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import asc, func, or_
from app.modules.users.schema import User

async def get_user_by_username(db: AsyncSession, username: str):
   result = await db.execute(select(User).where(User.username == username))
   return result.scalars().first()


async def get_users_paginated(
   db: AsyncSession,
   page: int = 1,
   page_size: int = 20,
   search: str | None = None
):
   query = select(User).order_by(asc(func.lower(User.name)))
   count_query = select(func.count()).select_from(User)

   if search:
      search_filter = or_(
         User.name.ilike(f"%{search}%"), # type: ignore
         User.email.ilike(f"%{search}%") # type: ignore
      )
      query = query.where(search_filter)
      count_query = count_query.where(search_filter)

   offset = (page - 1) * page_size
   query = query.offset(offset).limit(page_size)
   
   result = await db.session.execute(query)
   users = [data[0] for data in result.unique().all()]
   
   total = await db.session.scalar(count_query) or 0

   return {
      "users": users,
      "total": total,
      "page": page,
      "page_size": page_size,
      "total_pages": (total + page_size - 1) // page_size if total > 0 else 0
   }