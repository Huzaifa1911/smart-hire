"""One-use organization invitation, storing only a token hash."""

import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Text,
    func,
    text,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.enums import InvitationStatus
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class TenantInvitation(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "tenant_invitations"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "invited_by_membership_id"],
            ["tenant_memberships.tenant_id", "tenant_memberships.id"],
            name="fk_invitations_inviter_membership",
        ),
        CheckConstraint("btrim(email) <> ''", name="ck_invitations_email_nonempty"),
        CheckConstraint("expires_at > created_at", name="ck_invitations_expiry"),
        CheckConstraint(
            "(status = 'accepted') = (accepted_by_user_id IS NOT NULL AND accepted_at IS NOT NULL)",
            name="ck_invitations_accepted",
        ),
        CheckConstraint(
            "status = 'accepted' OR (accepted_by_user_id IS NULL AND accepted_at IS NULL)",
            name="ck_invitations_unaccepted",
        ),
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    email: Mapped[str] = mapped_column(Text)
    invited_by_membership_id: Mapped[uuid.UUID]
    token_hash: Mapped[str] = mapped_column(Text, unique=True)
    status: Mapped[InvitationStatus] = mapped_column(
        SAEnum(
            InvitationStatus,
            name="invitation_status",
            values_callable=lambda enum: [member.value for member in enum],
            native_enum=True,
            validate_strings=True,
        ),
        default=InvitationStatus.PENDING,
        server_default=InvitationStatus.PENDING.value,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    accepted_by_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


Index(
    "invitations_pending_email_uq",
    TenantInvitation.tenant_id,
    func.lower(func.btrim(TenantInvitation.email)),
    unique=True,
    postgresql_where=text("status = 'pending'"),
)
