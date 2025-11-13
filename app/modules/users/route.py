from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.modules.auth.service import get_password_hash
from app.modules.users.model import User
from app.modules.users.schema import UserCreate, UsersSchema, UserRead
from app.modules.users.service import get_users_paginated

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=UsersSchema)
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Recupera todos os usuários da aplicação
    """
    return await get_users_paginated(db=db, page=page, page_size=page_size, search=search)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Verifica se já existe email cadastrado
    existing = await db.execute(select(User).where(User.email == user.email))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role or "user",
        active=True,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
