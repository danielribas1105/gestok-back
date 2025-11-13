from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel import SQLModel
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def init_db():
   print(f"🔗 Conectado a: {engine.url}")
   from app.modules.users.model import User

   async with engine.begin() as conn:
      print("📦 Criando tabelas (se não existirem)...")
      await conn.run_sync(SQLModel.metadata.create_all)
      
   print("✅ Banco de dados inicializado com sucesso.")

async def get_db():
   async with AsyncSessionLocal() as session:
      yield session
