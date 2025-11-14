from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.modules.clients.model import Client
from app.modules.inventory.model import Inventory, StockMovement
from app.modules.orders.model import Order, OrderItem
from app.modules.orders.schema import OrderCreate, OrderProcessResponse, OrderRead, OrdersSchema
from app.modules.orders.service import get_orders_paginated
from app.modules.products.model import Product


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=OrdersSchema)
async def get_orders(
   page: int = Query(1, ge=1),
   page_size: int = Query(20, ge=1, le=100),
   search: str | None = None,
   db: AsyncSession = Depends(get_db)
):
   """
   Recupera todos os pedidos cadastrados
   """
   return await get_orders_paginated(db=db, page=page, page_size=page_size, search=search)


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
   order: OrderCreate, 
   user_id: uuid.UUID = Query(..., description="ID do usuário que está criando o pedido"), 
   db: AsyncSession = Depends(get_db)
) -> Order:
   """
   Cria um novo pedido com seus itens.
   
   Args:
      order: Dados do pedido e itens
      user_id: ID do usuário que está criando o pedido
      db: Sessão do banco de dados
   
   Returns:
      Order: Pedido criado com todos os itens
   """
   
   # Validar se o cliente existe
   client = await db.get(Client, order.client_id)
   if not client:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=f"Cliente com ID {order.client_id} não encontrado"
      )
   
   if not client.active:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail="Cliente está inativo"
      )
   
   # Validar tipo de pedido
   if order.order_type not in ["ENTRADA", "SAIDA"]:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail="Tipo de pedido deve ser 'ENTRADA' ou 'SAIDA'"
      )
   
   # Validar se há itens no pedido
   if not order.items or len(order.items) == 0:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail="Pedido deve conter pelo menos um item"
      )
   
   # Criar o pedido
   new_order = Order(
      cod_order=order.cod_order,
      client_id=order.client_id,
      user_id=user_id,
      order_type=order.order_type,
      order_date=datetime.utcnow(),
      status="PENDENTE",
      observations=order.observations
   )
   
   db.add(new_order)
   await db.flush()  # Gera o ID do pedido sem commitar
   
   # Criar os itens do pedido
   for item in order.items:
      # Validar se o produto existe
      product = await db.get(Product, item.product_id)
      if not product:
         raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Produto com ID {item.product_id} não encontrado"
         )
      
      if not product.active:
         raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail=f"Produto {product.name} está inativo"
         )
      
      # Validar quantidade
      if item.quantity <= 0:
         raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Quantidade deve ser maior que zero"
         )
      
      # Para pedidos de SAIDA, verificar disponibilidade no estoque
      if order.order_type == "SAIDA":
         result = await db.execute(select(Inventory).where(Inventory.product_id == item.product_id))
         inventory = result.scalar_one_or_none()
         
         if inventory and inventory.available_quantity < item.quantity:
               raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail=f"Quantidade insuficiente em estoque para o produto {product.name}. "
                        f"Disponível: {inventory.available_quantity}, Solicitado: {item.quantity}"
               )
      
      # Calcular valor total do item
      total_value = item.quantity * item.unit_value
      
      # Criar item do pedido
      order_item = OrderItem(
         order_id=new_order.id,
         product_id=item.product_id,
         quantity=item.quantity,
         unit_value=item.unit_value,
         total_value=total_value
      )
      
      db.add(order_item)
      
      # Se for pedido de SAIDA, reservar quantidade no estoque
      if order.order_type == "SAIDA":
         result = await db.execute(select(Inventory).where(Inventory.product_id == item.product_id))
         inventory = result.scalar_one_or_none()
         
         if inventory:
               inventory.reserved_quantity += item.quantity
               inventory.available_quantity -= item.quantity
               inventory.last_updated = datetime.utcnow()
               db.add(inventory)
   
   await db.commit()

   # ⚠ Carregar relações antes do retorno → evita MissingGreenlet
   result = await db.execute(
      select(Order)
      .options(
         joinedload(Order.order_items).joinedload(OrderItem.product),
         joinedload(Order.client),
         joinedload(Order.user),
      )
      .where(Order.id == new_order.id)
   )
   order_with_relations = result.unique().scalar_one()

   return order_with_relations

@router.post("/{order_id}/process", response_model=OrderProcessResponse)
async def process_order(order_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> dict:
   """
   Processa um pedido pendente, atualizando o estoque e criando movimentações.
   
   Args:
      order_id: ID do pedido a ser processado
      db: Sessão do banco de dados
   
   Returns:
      dict: Informações sobre o processamento
   """
   
   # Buscar o pedido
   order = await db.get(Order, order_id)
   if not order:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=f"Pedido com ID {order_id} não encontrado"
      )
   
   # Validar status do pedido
   if order.status != "PENDENTE":
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail=f"Pedido não pode ser processado. Status atual: {order.status}"
      )
   
   # Buscar itens do pedido
   result = await db.execute(
      select(OrderItem).where(OrderItem.order_id == order_id)
   )
   order_items = result.scalars().all()
   
   movements_created = 0
   
   # Processar cada item
   for item in order_items:
      # Criar movimentação de estoque
      movement = StockMovement(
         product_id=item.product_id,
         order_id=order.id,
         movement_type=order.order_type,
         quantity=item.quantity,
         movement_date=datetime.utcnow()
      )
      db.add(movement)
      movements_created += 1
      
      # Atualizar estoque
      result = await db.execute(
         select(Inventory).where(Inventory.product_id == item.product_id)
      )
      inventory = result.scalar_one_or_none()
      
      if order.order_type == "ENTRADA":
         # Entrada: aumenta estoque
         if inventory:
               inventory.current_quantity += item.quantity
               inventory.available_quantity += item.quantity
         else:
               # Criar registro de estoque se não existir
               inventory = Inventory(
                  product_id=item.product_id,
                  current_quantity=item.quantity,
                  reserved_quantity=0.0,
                  available_quantity=item.quantity
               )
               db.add(inventory)
      
      elif order.order_type == "SAIDA":
         # Saída: diminui estoque
         if inventory:
               inventory.current_quantity -= item.quantity
               inventory.reserved_quantity -= item.quantity
               # available_quantity já foi decrementado na criação do pedido
         else:
               raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail=f"Produto {item.product_id} não possui estoque"
               )
      
      if inventory:
         inventory.last_updated = datetime.utcnow()
         db.add(inventory)
   
   # Atualizar status do pedido
   order.status = "PROCESSADO"
   order.processed_date = datetime.utcnow()
   db.add(order)
   
   await db.commit()
   await db.refresh(order)
   
   return {
      "success": True,
      "message": "Pedido processado com sucesso",
      "order": order,
      "movements_created": movements_created
   }


@router.post("/{order_id}/cancel", response_model=OrderRead)
async def cancel_order(order_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Order:
   """
   Cancela um pedido pendente, liberando reservas de estoque.
   
   Args:
      order_id: ID do pedido a ser cancelado
      db: Sessão do banco de dados
   
   Returns:
      Order: Pedido cancelado
   """
   
   # Buscar o pedido
   order = await db.get(Order, order_id)
   if not order:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=f"Pedido com ID {order_id} não encontrado"
      )
   
   # Validar status do pedido
   if order.status != "PENDENTE":
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail=f"Apenas pedidos pendentes podem ser cancelados. Status atual: {order.status}"
      )
   
   # Se for pedido de SAIDA, liberar quantidades reservadas
   if order.order_type == "SAIDA":
      result = await db.execute(
         select(OrderItem).where(OrderItem.order_id == order_id)
      )
      order_items = result.scalars().all()
      
      for item in order_items:
         result = await db.execute(
               select(Inventory).where(Inventory.product_id == item.product_id)
         )
         inventory = result.scalar_one_or_none()
         
         if inventory:
               inventory.reserved_quantity -= item.quantity
               inventory.available_quantity += item.quantity
               inventory.last_updated = datetime.utcnow()
               db.add(inventory)
   
   # Atualizar status do pedido
   order.status = "CANCELADO"
   db.add(order)
   
   await db.commit()
   await db.refresh(order)
   
   return order