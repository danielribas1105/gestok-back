from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.route import api_router
from app.db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
   # Executa na inicialização
   await init_db()
   print("✅ Banco de dados inicializado com sucesso.")

   yield  # <- Aqui o app roda normalmente

   # Executa no encerramento (opcional)
   print("🛑 Encerrando aplicação...")

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

@app.get("/")
def home():
   return {"message": "API FastAPI - Gestok - rodando com sucesso!"}

@app.get("/soma")
def soma(a: int, b: int):
   return {"resultado": a + b}
