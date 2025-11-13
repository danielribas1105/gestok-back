from pydantic_settings import BaseSettings


class Settings(BaseSettings):
   APP_NAME: str = "Back Gestok App"
   DATABASE_URL: str
   SECRET_KEY: str
   ALGORITHM: str = "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
   REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200

   class Config:
      env_file = '.env'
      env_file_encoding = 'utf-8'

settings = Settings()