"""IAM endpoint declarations; business logic is intentionally unimplemented."""

from fastapi import Query

from app.core.exceptions import AppError
from app.schemas.users import UserUpdateRequest


async def get_current_user():
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def update_current_user(body: UserUpdateRequest):
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def enable_candidate_access():
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def list_current_memberships(
    offset: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)
):
    raise AppError("This endpoint is not implemented yet", status_code=501)
