from fastapi import APIRouter, Query
from app.modules.users.schema import UsersSchema
from app.modules.users.service import ( get_users_paginated )

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/", response_model=UsersSchema)
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None
):
    return await get_users_paginated(page=page, page_size=page_size, search=search)