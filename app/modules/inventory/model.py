from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import text
from sqlmodel import Field, Relationship, SQLModel

from app.modules.orders.model import Order
from app.modules.products.model import Product

class Inventory(SQLModel, table=True):
   __tablename__= "inventory"
   id: uuid.UUID = Field(
      default_factory=uuid.uuid4,
      primary_key=True,
      sa_column_kwargs={"server_default": text("gen_random_uuid()")},
   )

   # Foreign Key
   product_id: uuid.UUID = Field(foreign_key="products.id", unique=True)
   
   current_quantity: float = Field(default=0.0)
   reserved_quantity: float = Field(default=0.0)
   available_quantity: float = Field(default=0.0)
   last_updated: datetime = Field(default_factory=datetime.utcnow)
   
   # Relationship
   product: Product = Relationship(back_populates="inventory")
   

class StockMovement(SQLModel, table=True):
   __tablename__ = "stock_movements"
   id: uuid.UUID = Field(
      default_factory=uuid.uuid4,
      primary_key=True,
      sa_column_kwargs={"server_default": text("gen_random_uuid()")},
   )
   
   # Foreign Key
   product_id: uuid.UUID = Field(foreign_key="products.id")
   order_id: uuid.UUID = Field(foreign_key="orders.id")
   
   movement_type: str = Field()  # ENTRADA ou SAIDA
   quantity: float = Field()
   movement_date: datetime = Field(default_factory=datetime.utcnow)
   observations: Optional[str] = Field(default=None)
   
   # Relationship
   product: Product = Relationship(back_populates="stock_movements")
   order: Order = Relationship(back_populates="stock_movements")