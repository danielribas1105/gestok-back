from datetime import datetime
from typing import List, Optional
import uuid

from sqlalchemy import text
from sqlmodel import Field, Relationship, SQLModel

class Product(SQLModel, table=True):
   __tablename__= "products"
   id: uuid.UUID = Field(
      default_factory=uuid.uuid4,
      primary_key=True,
      sa_column_kwargs={"server_default": text("gen_random_uuid()")},
   )
   cod_product: str = Field(sa_column_kwargs={"unique": True, "index": True})
   description: str = Field()
   unit: str = Field()
   value: float
   active: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
   created_at: datetime = Field(default_factory=datetime.utcnow)

   # Relacionamentos
   order_items: List["OrderItem"] = Relationship(back_populates="product")
   inventory: Optional["Inventory"] = Relationship(back_populates="product")
   stock_movements: List["StockMovement"] = Relationship(back_populates="product")
