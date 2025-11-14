from datetime import datetime
from typing import List, Optional
import uuid

from sqlalchemy import text
from sqlmodel import Field, Relationship, SQLModel

from app.modules.clients.model import Client
from app.modules.products.model import Product
from app.modules.users.model import User


class Order(SQLModel, table=True):
   __tablename__= "orders"
   id: uuid.UUID = Field(
      default_factory=uuid.uuid4,
      primary_key=True,
      sa_column_kwargs={"server_default": text("gen_random_uuid()")},
   )
   cod_order: str = Field(sa_column_kwargs={"unique": True, "index": True})
   
   # Foreign Key
   client_id: uuid.UUID = Field(foreign_key="clients.id")
   user_id: uuid.UUID = Field(foreign_key="users.id")
   
   order_type: str = Field()  # ENTRADA ou SAIDA
   order_date: datetime = Field(default_factory=datetime.utcnow)
   processed_date: Optional[datetime] = Field(default=None)
   status: str = Field(default="PENDENTE")  # PENDENTE, PROCESSADO, CANCELADO
   observations: Optional[str] = Field(default=None)
   
   # Relationship
   client: Client = Relationship(back_populates="orders")
   user: User = Relationship(back_populates="orders")
   order_items: List["OrderItem"] = Relationship(back_populates="order")
   stock_movements: List["StockMovement"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
   __tablename__ = "order_items"
   id: uuid.UUID = Field(
      default_factory=uuid.uuid4,
      primary_key=True,
      sa_column_kwargs={"server_default": text("gen_random_uuid()")},
   )
   
   # Foreign Key
   order_id: uuid.UUID = Field(foreign_key="orders.id")
   product_id: uuid.UUID = Field(foreign_key="products.id")
   
   quantity: float = Field()
   unit_value: float = Field()
   total_value: float = Field()
   
   # Relationship
   order: Order = Relationship(back_populates="order_items")
   product: Product = Relationship(back_populates="order_items")