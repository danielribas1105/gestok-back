import uuid

from sqlalchemy import text
from sqlmodel import Field, SQLModel


class Order(SQLModel, table=True):
   __tablename__= "orders"
   id: uuid.UUID = Field(
      default_factory=uuid.uuid4,
      primary_key=True,
      sa_column_kwargs={"server_default": text("gen_random_uuid()")},
   )
   cod_order: str = Field(sa_column_kwargs={"unique": True, "index": True})
   data: str = Field()
   type: str = Field()
   unit: str = Field()
   amount: int
   value: float
   route: str = Field()
