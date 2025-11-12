from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.clients.schema import ClientBase

async def get_all_clients(db: AsyncSession):
   result = await db.execute(select(ClientBase))
   return result.scalars().first()