from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from app.api.route import api_router
from app.db.database import init_db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
   # Executa na inicialização
   await init_db()
   print("✅ Banco de dados inicializado com sucesso.")

   yield  # <- Aqui o app roda normalmente

   # Executa no encerramento (opcional)
   print("🛑 Encerrando aplicação...")

app = FastAPI(lifespan=lifespan)

# 🔒 Configuração do CORS
app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:3000"],  # URL do seu frontend Next.js
   allow_credentials=True,
   allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
   allow_headers=["*"],  # Permite todos os headers
)

# 💾 Middleware de sessão do banco (ESSENCIAL)
app.add_middleware(
   SQLAlchemyMiddleware,
   db_url=os.getenv("DATABASE_URL"),  # exemplo: "postgresql+asyncpg://user:pass@localhost:5432/gestok"
)

# 🚀 Rotas
app.include_router(api_router)

@app.get("/")
def home():
   return {"message": "API FastAPI - Gestok - rodando com sucesso!"}

