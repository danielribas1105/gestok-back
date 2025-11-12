from fastapi import APIRouter, HTTPException
from app.modules.auth.service import ( authenticate_user, login_user )
from app.modules.auth.schema import ( Token, LoginData )


router = APIRouter(prefix="/auth")

@router.post("/login", response_model=Token)
async def login(data: LoginData):
   user = authenticate_user(data.username, data.password)
   if not user:
      raise HTTPException(status_code=401, detail="Invalid credentials")
   return login_user(user)