from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel

from app.modules.products.schema import ProductRead


# ==================== STOCK MOVEMENT SCHEMAS ====================

class StockMovementBase(BaseModel):
   product_id: uuid.UUID
   order_id: uuid.UUID
   movement_type: str  # ENTRADA ou SAIDA
   quantity: float
   observations: Optional[str] = None


class StockMovementCreate(StockMovementBase):
   pass


class StockMovementRead(StockMovementBase):
   id: uuid.UUID
   movement_date: datetime
   product: Optional[ProductRead] = None

   class Config:
      from_attributes = True


class StockMovementsSchema(BaseModel):
   movements: List[StockMovementRead]
   total: int
   page: int
   page_size: int
   total_pages: int


# ==================== INVENTORY SCHEMAS ====================

class InventoryBase(BaseModel):
   product_id: uuid.UUID
   current_quantity: float
   reserved_quantity: float
   available_quantity: float


class InventoryRead(InventoryBase):
   id: uuid.UUID
   last_updated: datetime
   product: Optional[ProductRead] = None

   class Config:
      from_attributes = True


class InventorySchema(BaseModel):
   inventory: List[InventoryRead]
   total: int
   page: int
   page_size: int
   total_pages: int