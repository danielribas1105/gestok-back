import uuid

from sqlalchemy import text
from sqlmodel import Field, SQLModel


class Client(SQLModel, table=True):
   __table__= "clients"
   id: uuid.UUID = Field(
      default_factory=uuid.uuid4,
      primary_key=True,
      sa_column_kwargs={"server_default": text("gen_random_uuid()")},
   )
   cod_client: str = Field(sa_column_kwargs={"unique": True, "index": True})
   client: str = Field()
   trade_name: str = Field()
   address: str = Field()
   city: str = Field()
   state: str = Field()
   zip_code: str = Field()
   contact: str = Field()
   cnpj: str = Field(sa_column_kwargs={"unique": True })
   state_register: str = Field(sa_column_kwargs={"unique": True })
   active: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
