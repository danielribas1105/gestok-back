from pydantic import BaseModel

class LoginData(BaseModel):
   username: str
   password: str

class Token(BaseModel):
   access_token: str
   token_type: str= "bearer"
   expire_at: int
   refresh_token: str


class TokenData(BaseModel):
   user_id: str | None = None


class RefreshTokenBody(BaseModel):
   refresh_token: str
