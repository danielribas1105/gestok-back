from fastapi import APIRouter
from sqlalchemy import text
from app.db.database import engine
from sqlalchemy.ext.asyncio import AsyncConnection
from datetime import datetime, timezone

router = APIRouter()

@router.get("/status", tags=["Status"])
async def get_status():
   try:
      async with engine.begin() as conn:  # type: AsyncConnection
         await conn.execute(text("SELECT 1"))
      return {
         "status": "online",
         "timestamp": datetime.now(timezone.utc).isoformat()
      }
   except Exception as e:
      print("❌ Erro ao verificar o banco:", e)
      return {
         "status": "offline",
         "error": str(e),
         "timestamp": datetime.now(timezone.utc).isoformat()
      }
