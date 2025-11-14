from datetime import datetime
import uuid
from pydantic import BaseModel

class ProductBase(BaseModel):
   cod_product: str
   description: str
   unit: str
   value: float
   active: bool = True

class ProductCreate(ProductBase):
   pass

class ProductRead(ProductBase):
   id: uuid.UUID
   created_at: datetime
   class Config:
      from_attributes = True

class ProductSchema(BaseModel):
   products: list[ProductRead]
   total: int
   page: int
   page_size: int
   total_pages: int