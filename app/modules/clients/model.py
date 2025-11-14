from datetime import datetime
from typing import List
import uuid

from sqlalchemy import text
from sqlmodel import Field, Relationship, SQLModel


class Client(SQLModel, table=True):
   __tablename__= "clients"
   id: uuid.UUID = Field(
      default_factory=uuid.uuid4,
      primary_key=True,
      sa_column_kwargs={"server_default": text("gen_random_uuid()")},
   )
   cod_client: str = Field(sa_column_kwargs={"unique": True, "index": True})
   client: str = Field()
   active: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
   created_at: datetime = Field(default_factory=datetime.utcnow)

   # Relationship
   orders: List["Order"] = Relationship(back_populates="client")
