"""IAM endpoint declarations; business logic is intentionally unimplemented."""

from app.core.exceptions import AppError
from app.schemas.auth import (
    CandidateSignupRequest,
    LoginRequest,
    OrganizationSignupRequest,
)


async def candidate_signup(body: CandidateSignupRequest):
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def organization_signup(body: OrganizationSignupRequest):
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def login(body: LoginRequest):
    raise AppError("This endpoint is not implemented yet", status_code=501)
