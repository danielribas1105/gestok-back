from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.modules.auth.service import ( authenticate_user, consume_refresh_token, create_access_token, create_refresh_token )
from app.modules.auth.schema import ( RefreshTokenBody, Token, LoginData )


router = APIRouter(prefix="/auth", tags=["Auth"])

""" @router.post("/login", response_model=Token)
async def login(data: LoginData):
   user = authenticate_user(data.username, data.password)
   if not user:
      raise HTTPException(status_code=401, detail="Invalid credentials")
   return login_user(user) """

@router.post("/token")
async def login_for_access_token(
   form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
   print("trying to login")
   user = await authenticate_user(form_data.username, form_data.password)
   if not user:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Incorrect username or password",
         headers={"WWW-Authenticate": "Bearer"},
      )

   access_token, expire = create_access_token(data={"sub": str(user.id)})
   refresh_token, _ = await create_refresh_token(
      user_id=str(user.id)
   )

   return Token(
      access_token=access_token,
      token_type="bearer",
      expire_at=expire,
      refresh_token=refresh_token,
   )


@router.post("/refresh")
async def refresh_token(body: RefreshTokenBody):
   data = await consume_refresh_token(body.refresh_token)

   return Token(
      access_token=data["access_token"],
      token_type="bearer",
      expire_at=data["expire"],
      refresh_token=data["refresh_token"],
   )
