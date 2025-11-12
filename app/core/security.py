import jwt
from datetime import datetime, timedelta
from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta | None = None):
   to_encode = data.copy()
   expire = datetime.utcnow() + (
      expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   )
   to_encode.update({"exp": expire})
   return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
