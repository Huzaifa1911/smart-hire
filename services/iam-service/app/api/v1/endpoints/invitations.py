"""IAM endpoint declarations; business logic is intentionally unimplemented."""

from app.core.exceptions import AppError
from app.schemas.invitations import InvitationAcceptRequest


async def accept_invitation(body: InvitationAcceptRequest):
    raise AppError("This endpoint is not implemented yet", status_code=501)
