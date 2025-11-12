from pydantic import BaseSettings


class Settings(BaseSettings):
   APP_NAME: str = "Back Gestok App"
   DATABASE_URL: str
   SECRET_KEY: str
   ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


   class Config:
      env_file = '.env'

settings = Settings()