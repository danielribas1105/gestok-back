import uuid
from pydantic import BaseModel

class ProductBase(BaseModel):
   cod_client: str
   client: str
   trade_name: str

class ProductCreate(ProductBase):
   pass

class ProductRead(ProductBase):
   id: uuid.UUID
   class Config:
      from_attributes = True

class ProductSchema(BaseModel):
   products: list[ProductRead]
   total: int
   page: int
   page_size: int
   total_pages: int