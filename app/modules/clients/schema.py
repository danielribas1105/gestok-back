import uuid
from pydantic import BaseModel

class ClientBase(BaseModel):
   cod_client: str
   client: str
   trade_name: str

class ClientCreate(ClientBase):
   pass

class ClientRead(ClientBase):
   id: uuid.UUID
   class Config:
      from_attributes = True

class ClientsSchema(BaseModel):
   clients: list[ClientRead]
   total: int
   page: int
   page_size: int
   total_pages: int