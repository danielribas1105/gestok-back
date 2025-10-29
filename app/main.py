from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
   return {"message": "API FastAPI rodando com sucesso!"}

@app.get("/soma")
def soma(a: int, b: int):
   return {"resultado": a + b}
