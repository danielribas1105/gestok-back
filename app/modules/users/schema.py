from typing import Optional
import uuid

from pydantic import BaseModel


class SimplifiedUser(BaseModel):
   id: uuid.UUID
   name: str
   email: str


class SimplifiedUserWithRole(SimplifiedUser):
   role: str


class UserUnsafeBase(BaseModel):
   name: str
   email: str


class UserBase(UserUnsafeBase):
   active: bool = True
   role: str = "user"


class UserCreate(UserBase):
   password: str


class UserUpdateName(BaseModel):
   user_id: uuid.UUID
   name: Optional[str] = None
   email: Optional[str] = None


class UserUpdate(UserBase):
   user_id: uuid.UUID
   name: Optional[str] = None
   email: Optional[str] = None
   role: Optional[str] = None
   ative: Optional[bool] = None


class User(UserBase):
   id: uuid.UUID


class UserRegister(UserUnsafeBase):
   password: str


class UserRead(UserBase):
   id: uuid.UUID
   class Config:
      orm_mode = True


class UserEdit(BaseModel):
   email: str | None = None
   name: str | None = None
   role: str | None = None
   password: str | None = None


class UserEditPasswordSchema(BaseModel):
   user_id: uuid.UUID
   password: str
   confirm_password: str


class UsersSchema(BaseModel):
   users: list[User]
   total: int
   page: int
   page_size: int
   total_pages: int
