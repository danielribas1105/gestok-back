from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.modules.clients.schema import ClientsSchema
from app.modules.clients.service import get_clients_paginated

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=ClientsSchema)
async def get_clients(
   page: int = Query(1, ge=1),
   page_size: int = Query(20, ge=1, le=100),
   search: str | None = None,
   db: AsyncSession = Depends(get_db)
):
   """
   Recupera todos os clientes cadastrados
   """
   return await get_clients_paginated(db=db, page=page, page_size=page_size, search=search)