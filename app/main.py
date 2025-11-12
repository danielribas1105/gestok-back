from fastapi import FastAPI
from app.api.route import api_router
from app.db.database import init_db

app = FastAPI()

app.include_router(api_router)

@app.on_event("startup")
async def on_startup():
   await init_db()

@app.get("/")
def home():
   return {"message": "API FastAPI rodando com sucesso!"}

@app.get("/soma")
def soma(a: int, b: int):
   return {"resultado": a + b}
