from datetime import datetime
import uuid
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
   name: str
   email: EmailStr
   active: bool = True
   role: str = "user"

class UserCreate(UserBase):
   password: str

class UserRead(UserBase):
   id: uuid.UUID
   created_at: datetime
   class Config:
      from_attributes = True

class UsersSchema(BaseModel):
   users: list[UserRead]
   total: int
   page: int
   page_size: int
   total_pages: int
