from datetime import datetime
from typing import List
import uuid

from sqlalchemy import text
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
   __tablename__ = "users"
   id: uuid.UUID = Field(
      default_factory=uuid.uuid4,
      primary_key=True,
      sa_column_kwargs={"server_default": text("gen_random_uuid()")},
   )
   name: str = Field()
   email: str = Field(sa_column_kwargs={"unique": True, "index": True})
   password: str
   active: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
   role: str = Field(default="user")
   created_at: datetime = Field(default_factory=datetime.utcnow)

   # Relationship
   orders: List["Order"] = Relationship(back_populates="user")
   