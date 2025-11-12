from datetime import timedelta
from app.core.security import create_access_token
from app.core.config import settings

def authenticate_user(username: str, password: str):
   # Exemplo fictício
   if username == "admin" and password == "123":
      return {"username": username}
   return None

def login_user(user: dict):
   access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
   return {"access_token": token, "token_type": "bearer"}
