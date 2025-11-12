from fastapi import APIRouter, Depends
from app.db.database import get_db
from app.modules.clients.schema import ClientRead
from app.modules.clients.service import get_all_clients

router = APIRouter(prefix="/client")

@router.get("/", response_model=list[ClientRead])
async def list_clients(db=Depends(get_db)):
   return await get_all_clients(db)
