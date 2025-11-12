from fastapi import APIRouter, Depends, Query
from app.db.database import get_db
from app.modules.users.schema import UsersSchema, UserRead
from app.modules.users.service import ( get_users_paginated )

router = APIRouter(prefix="/user")

""" @router.get("/", response_model=list[UserRead])
async def list_users(db=Depends(get_db)):
    return await get_all_users(db) """

@router.get("/", response_model=UsersSchema)
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None
):
    return await get_users_paginated(page=page, page_size=page_size, search=search)