from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel

from app.modules.clients.schema import ClientRead
from app.modules.products.schema import ProductRead
from app.modules.users.schema import UserRead


# ==================== ORDER ITEM SCHEMAS ====================

class OrderItemBase(BaseModel):
   product_id: uuid.UUID
   quantity: float
   unit_value: float


class OrderItemCreate(OrderItemBase):
   pass


class OrderItemRead(OrderItemBase):
   id: uuid.UUID
   order_id: uuid.UUID
   total_value: float
   product: Optional[ProductRead] = None

   class Config:
      from_attributes = True


# ==================== ORDER SCHEMAS ====================

class OrderBase(BaseModel):
   cod_order: str
   client_id: uuid.UUID
   order_type: str  # ENTRADA ou SAIDA
   observations: Optional[str] = None


class OrderCreate(OrderBase):
   items: List[OrderItemCreate]        # Cria pedido + itens de uma vez    


class OrderUpdate(BaseModel):
   status: Optional[str] = None
   observations: Optional[str] = None


class OrderRead(OrderBase):
   id: uuid.UUID
   user_id: uuid.UUID
   order_date: datetime
   processed_date: Optional[datetime] = None
   status: str
   client: Optional[ClientRead] = None       # Cliente relacionado
   user: Optional[UserRead] = None           # Usuário que registrou
   order_items: List[OrderItemRead] = []     # Itens do pedido

   class Config:
      from_attributes = True


class OrdersSchema(BaseModel):
   orders: List[OrderRead]
   total: int
   page: int
   page_size: int
   total_pages: int


# ==================== PROCESS ORDER SCHEMA ====================

class OrderProcessRequest(BaseModel):
      order_id: uuid.UUID


class OrderProcessResponse(BaseModel):
   success: bool
   message: str
   order: OrderRead
   movements_created: int
