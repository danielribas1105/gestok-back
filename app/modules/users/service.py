import uuid
from fastapi_async_sqlalchemy import db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import func, or_
from app.modules.users.model import User

async def get_user_by_id(id: uuid.UUID | str | None):
   return await db.session.get(User, id)

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

""" async def get_user_by_email(email) -> User | None:
   print("get_user_by_email")
   print(email)
   print("Sessão ativa?", db.session)
   result = (await db.session.execute(select(User).where(User.email == email))).first()
   print("result")
   print(result)

   return result[0] if result is not None else None """

async def get_user_by_email(email) -> User | None:
   print(f"🔍 Buscando usuário com email={email}")
   session = db.session
   print(f"Sessão ativa: {session}")

   stmt = select(User).where(User.email == email)
   print(f"SQL gerado: {stmt}")

   result = await session.execute(stmt)
   user = result.scalars().first()

   print(f"Resultado da query: {user}")
   return user