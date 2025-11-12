from fastapi import APIRouter, HTTPException
from modules.auth.service import ( authenticate_user, login_user )
from modules.auth.schema import ( Token )


router = APIRouter(prefix="/auth")

@router.post("/login", response_model=Token)
async def login(data: schemas.LoginData):
   user = authenticate_user(data.username, data.password)
   if not user:
      raise HTTPException(status_code=401, detail="Invalid credentials")
   return login_user(user)