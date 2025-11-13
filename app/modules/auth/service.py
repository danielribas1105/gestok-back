from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta, timezone
from math import floor
from uuid import UUID
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi_async_sqlalchemy import db
from app.core.security import create_access_token
from app.core.config import settings
from app.modules.auth.model import UserSession
from app.modules.auth.schema import TokenData
from app.modules.users.service import get_user_by_email, get_user_by_id


SECRET_KEY: str = settings.SECRET_KEY
ALGORITHM: str = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
   return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
   # TODO: Add salt
   return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
   to_encode = data.copy()
   if expires_delta:
      expire = datetime.now(timezone.utc) + expires_delta
   else:
      expire = datetime.now(timezone.utc) + timedelta(
         minutes=ACCESS_TOKEN_EXPIRE_MINUTES
      )

   to_encode.update({"exp": expire})
   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   return encoded_jwt, floor(expire.timestamp())

async def authenticate_user(email: str, password: str):
   print(f"🔍 Autenticando: {email}")
   user = await get_user_by_email(email)
   print(f"🧩 Usuário encontrado: {user}")
   
   if not user:
      print("❌ Nenhum usuário encontrado.")
      return False

   print(f"🔑 Senha digitada: {password}")
   print(f"🔐 Hash armazenado: {user.password}")

   is_valid = verify_password(password, user.password)
   print(f"✅ Senha válida? {is_valid}")

   if not is_valid:
      print("❌ Senha incorreta.")
      return False

   print("✅ Usuário autenticado com sucesso!")
   return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
   credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
   )
   try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

      user_id: str = payload.get("sub")

      if user_id is None:
         raise credentials_exception

      token_data = TokenData(user_id=user_id)
   except:
      raise credentials_exception

   user = await get_user_by_id(token_data.user_id)
   if user is None:
      raise credentials_exception

   if user.active is False:
      raise HTTPException(status_code=400, detail="Inactive user")

   return user

async def create_refresh_token(user_id: str, expires_delta: timedelta | None = None):
   if expires_delta:
      expire = datetime.now(timezone.utc) + expires_delta
   else:
      expire = datetime.now(timezone.utc) + timedelta(
         minutes=REFRESH_TOKEN_EXPIRE_MINUTES
      )

   new_session = UserSession(user_id=UUID(user_id), expires_at=expire)

   db.session.add(new_session)
   await db.session.commit()
   await db.session.refresh(new_session)

   to_encode = {"sub": user_id, "jti": str(new_session.id)}

   return create_access_token(
      data=to_encode,
      expires_delta=(
         expires_delta
         if expires_delta
         else timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
      ),
   )


async def consume_refresh_token(refresh_token: str):
   credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
   )

   try:
      refresh_token_data = jwt.decode(
         refresh_token, SECRET_KEY, algorithms=[ALGORITHM]
      )
      if not refresh_token_data["jti"] or not refresh_token_data["sub"]:
         raise credentials_exception

      session = await db.session.get(UserSession, refresh_token_data["jti"])

      if session is None:
         raise credentials_exception

      if session.expires_at < datetime.now(timezone.utc):
         raise credentials_exception

      access_token, expire = create_access_token(
         data={"sub": refresh_token_data["sub"]}
      )

      await db.session.delete(session)
      await db.session.commit()

      refresh_token, _ = await create_refresh_token(user_id=str(session.user_id))

      return {
         "access_token": access_token,
         "expire": expire,
         "refresh_token": refresh_token,
      }
   except Exception as e:
      raise credentials_exception
