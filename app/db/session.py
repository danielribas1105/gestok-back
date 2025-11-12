from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL  # Ex: postgresql+asyncpg://user:pass@localhost/dbname

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = sessionmaker(
   bind=engine,
   class_=AsyncSession,
   expire_on_commit=False,
)

# ✅ Criação das tabelas
async def init_db():
   from app.modules.users.model import User
   async with engine.begin() as conn:
      print("📦 Criando tabelas (se não existirem)...")
      await conn.run_sync(SQLModel.metadata.create_all)
   print("✅ Banco de dados inicializado com sucesso.")

# ✅ Dependência para FastAPI
async def get_db():
   async with AsyncSessionLocal() as session:
      yield session
